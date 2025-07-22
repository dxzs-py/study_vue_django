from datetime import datetime

from alipay import AliPay
from django.db import transaction, models
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from alipay.utils import AliPayConfig
from django.conf import settings
from order.models import Order
from rest_framework import status
from coupon.models import UserCoupon
from user_login.models import UserCourse
from course.models import CourseExpire
import logging

log = logging.getLogger("django")


class AlipayApiView(APIView):
    def get(self, request, *args, **kwargs):
        """获取支付宝的支付地址"""
        # 获取订单号
        order_number = request.query_params.get("order_number")
        # 判断订单是否存在
        try:
            order = Order.objects.get(order_number=order_number, is_show=True, is_deleted=False)
        except Order.DoesNotExist:
            return Response({"message": "订单不存在"}, status=status.HTTP_400_BAD_REQUEST)
        # 初始化支付对象
        alipay = AliPay(
            appid=settings.ALIAPY_CONFIG["appid"],
            app_notify_url=settings.ALIAPY_CONFIG["app_notify_url"],  # 默认回调 url
            app_private_key_string=open(settings.ALIAPY_CONFIG["app_private_key_path"]).read(),
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=open(settings.ALIAPY_CONFIG["alipay_public_key_path"]).read(),

            sign_type=settings.ALIAPY_CONFIG["sign_type"],  # RSA 或者 RSA2
            debug=settings.ALIAPY_CONFIG["debug"],  # 默认 False
            config=AliPayConfig(timeout=15)  # 可选，请求超时时间
        )

        # 调用接口
        # 电脑网站支付，需要跳转到：https://openapi-sandbox.dl.alipaydev.com/gateway.do？ + order_string
        order_string = alipay.api_alipay_trade_page_pay(
            # https://open.alipay.com/api/apiDebug点击看
            out_trade_no=order.order_number,  # 商户订单号
            total_amount=float(order.real_price),  # 订单总金额，单位为元，精确到小数点后两位
            subject=order.order_title,  # 订单标题
            return_url=settings.ALIAPY_CONFIG["return_url"],  # 可选，回跳地址
            notify_url=settings.ALIAPY_CONFIG["notify_url"]  # 可选，不填则使用默认 notify url
        )

        url = settings.ALIAPY_CONFIG["gateway_url"] + "?" + order_string

        return Response({"url": url})


class AliPayResultAPIView(APIView):
    def get(self, request, *args, **kwargs):
        """处理支付宝的同步通知结果"""
        # 初始化支付对象
        alipay = AliPay(
            appid=settings.ALIAPY_CONFIG["appid"],
            app_notify_url=settings.ALIAPY_CONFIG["app_notify_url"],  # 默认回调 url
            app_private_key_string=open(settings.ALIAPY_CONFIG["app_private_key_path"]).read(),
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=open(settings.ALIAPY_CONFIG["alipay_public_key_path"]).read(),

            sign_type=settings.ALIAPY_CONFIG["sign_type"],  # RSA 或者 RSA2
            debug=settings.ALIAPY_CONFIG["debug"],  # 默认 False
            config=AliPayConfig(timeout=15)  # 可选，请求超时时间
        )

        # 验证
        data = request.query_params.dict()
        signature = data.pop("sign")
        success = alipay.verify(data, signature)
        if success:
            return self.change_order_status(data)
        return Response({"message": "对不起，当前订单支付失败！"})

    def post(self, request, *args, **kwargs):
        """处理支付宝的异步通知结果"""  # 获取支付宝的异步通知结果
        # 初始化支付对象
        alipay = AliPay(
            appid=settings.ALIAPY_CONFIG["appid"],
            app_notify_url=settings.ALIAPY_CONFIG["app_notify_url"],  # 默认回调 url
            app_private_key_string=open(settings.ALIAPY_CONFIG["app_private_key_path"]).read(),
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=open(settings.ALIAPY_CONFIG["alipay_public_key_path"]).read(),

            sign_type=settings.ALIAPY_CONFIG["sign_type"],  # RSA 或者 RSA2
            debug=settings.ALIAPY_CONFIG["debug"],  # 默认 False
        )

        data = request.data
        # 验证
        signature = data.pop("sign")
        success = alipay.verify(data, signature)
        if success and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
            response = self.change_order_status(data)
            if "credit" in response.data:
                return HttpResponse("success")  # 支付宝要求如果成功只能传success

        return Response({"message": "对不起，当前订单支付失败！"})

    def change_order_status(self, data):
        # 支付成功以后的代码
        order_number = data.get("out_trade_no")
        try:
            order = Order.objects.get(order_number=order_number, is_show=True, is_deleted=False,
                                      order_status=Order.status_choices[0][0])
        except Order.DoesNotExist:
            return Response({"message": "对不起，支付结果查询失败！订单不存在"}, status=status.HTTP_400_BAD_REQUEST)
        with transaction.atomic():
            save_id = transaction.savepoint()
            try:
                # 更新订单状态、记录支付时间
                order.pay_time = datetime.now()
                order.order_status = Order.status_choices[1][0]
                order.save()

                # 如果有使用优惠价、积分，则修改优惠价的使用状态和扣除积分
                user_coupon_id = order.coupon
                if user_coupon_id > 0:
                    UserCoupon.objects.filter(
                        pk=user_coupon_id,
                        is_show=True,
                        is_deleted=False,
                        is_use=False
                    ).update(is_use=True)
                credit = order.credit
                if credit > 0:
                    user = order.user
                    user.credit -= credit
                    user.save()  # 没使用F()函数并发的话会出现并发问题

                # 记录用户成功购买课程的记录，增加课程的购买人数
                order_details = order.order_courses.all()  # 获取订单详情
                course_list = []
                for detail in order_details:
                    course = detail.course
                    course.students = models.F('students') + 1  # 使用F表达式避免并发问题
                    course.save(update_fields=['students'])  # 指定更新字段

                    pay_timestamp = order.pay_time.timestamp()
                    if detail.expire > 0:
                        # 有效期间购买
                        expire = CourseExpire.objects.get(pk=detail.expire)
                        expire_timestamp = expire.expire_time * 24 * 60 * 60
                        out_time = datetime.fromtimestamp(pay_timestamp + expire_timestamp)
                    else:
                        # 永久购买
                        out_time = None

                    UserCourse.objects.create(
                        user_id=user.id,
                        course_id=course.id,
                        trade_no=data.get("trade_no"),
                        buy_type=1,
                        pay_time=order.pay_time,
                        out_time=out_time
                    )
                    course_list.append({
                        "id": course.id,
                        "name": course.name
                    })
            except:
                log.error("订单结果处理出现故障!无法修改订单相关记录的状态！")
                transaction.savepoint_rollback(save_id)
                return Response({"message": "对不起，更新订单相关记录失败！"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({
            "message": "支付成功！",
            "credit": user.credit,
            "pay_time": order.pay_time,
            "real_price": order.real_price,
            "course_list": course_list
        })
