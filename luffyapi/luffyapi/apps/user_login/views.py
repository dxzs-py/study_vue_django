from .serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyObtainTokenPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer  # 只需修改其序列化器为刚刚自定义的即可


from luffyapi.libs.geetest import GeetestLib
from rest_framework.response import Response
from .serializers import get_account_by_mobile
from rest_framework import status as http_status
from rest_framework.views import APIView

# 请在官网申请ID使用，示例ID不可使用
pc_geetest_id = "6386fee5f38474b4d6bb30209dfbcde3"
pc_geetest_key = "9aa2e3aec4b8e94e4145926a07d58a91"


class CaptchaAPIView(APIView):
    """验证视图类"""
    status = False
    user_id = None

    def get(self, request):
        """获取验证码"""
        username = request.query_params.get("username")
        user = get_account_by_mobile(username)
        if user is None:
            return Response({"message": "对不起，用户不存在！"}, status=http_status.HTTP_400_BAD_REQUEST)
        self.user_id = user.id
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        self.status = gt.pre_process(self.user_id)
        # todo 后面增加status和user_id保存到redis数据库中
        response_str = gt.get_response_str()
        return Response(response_str)  # 返回验证码但是是字符串类型，需要转成json类型，在客户端实现

    def post(self, request):
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        if self.status:
            result = gt.success_validate(challenge, validate, seccode, self.user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        result = {"status": "success"} if result else {"status": "fail"}
        return Response(result)


from rest_framework.generics import CreateAPIView
from .models import User
from .serializers import UserModelSerializer


class UserAPIView(CreateAPIView):
    """用户信息视图"""
    queryset = User.objects.all()
    serializer_class = UserModelSerializer


import re
from rest_framework import serializers

"""
GET /user/mobile/<mobile>/
"""


class MobileAPIView(APIView):
    """手机号验证视图"""

    def get(self, request, mobile):
        # 验证手机号是否已经被注释过了
        if re.search("/", mobile):
            mobile = mobile.replace("/", "")
        reg = get_account_by_mobile(mobile)
        if reg is not None:
            return Response({"message": "手机号已经被注册"}, status=http_status.HTTP_400_BAD_REQUEST)
        return Response({"message": "改手机号未被注册，可以进行注册"}, status=http_status.HTTP_200_OK)


import random
from django_redis import get_redis_connection
from luffyapi.settings import constants
from luffyapi.libs.yuntongxun.sms import CCP
import logging

log = logging.getLogger("django")


class SmSAPIView(APIView):
    """短信验证码视图"""

    def get(self, request, mobile):
        """短信发送"""
        # 1.判断手机号是否在60秒内曾经发送过短信
        if re.search("/", mobile):
            mobile = mobile.replace("/", "")
        redis_conn = get_redis_connection("sms_code")
        ret = redis_conn.get("mobile_%s" % mobile)
        if ret is not None:
            return Response({"message": "短信60秒内发送过，请耐心等待"}, status=http_status.HTTP_400_BAD_REQUEST)

        # 2.生成短信验证码
        sms_code = "%04d" % random.randint(1000, 9999)  # 方案1
        # sms_code = f"{random.randint(1000, 9999):04}"  # 方案2
        # sms_code = "{:04}".format(random.randint(1000, 9999))  # 方案3

        # 3.保存短信验证码到redis数据库中[使用事务把多条命令集中发送给redis]
        pipe = redis_conn.pipeline()  # 创建管道对象
        pipe.multi()  # 开启事务【事务无法管理数据库的读取数据操作】
        # 把事务中要完成的所有操作，写入到管道中
        pipe.setex("sms_%s" % mobile, constants.SMS_EXPIRE_TIME, sms_code)
        pipe.setex("mobile_%s" % mobile, constants.SMS_INTERVAL_TIME, "_")
        pipe.execute()  # 执行事dfsaw务
        # redis_conn = t_redis_connection("sms_code") # 最原始的写法
        # redis_conn.setex("sms_%s" % mobile, constants.SMS_EXPIRE_TIME, sms_code)
        # redis_conn.setex("mobile_%s" % mobile, constants.SMS_INTERVAL_TIME, "_")

        # 4.调用短信sdk,发送短信验证码
        try:
            # 1. 声明一个和celery一模一样的任务函数，但是我们可以导包来解决
            from my_celery.sms.tasks import send_sms
            send_sms.delay(mobile,sms_code)
        except:
            return Response({"message": "短信发送失败"}, status=http_status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 5.响应发送短信的结果
        return Response({"message": "短信发送成功"}, status=http_status.HTTP_200_OK)
