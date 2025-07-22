from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from luffyapi.settings.constants import CREDIT_MONEY
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # 增加想要加到token中的信息
        token['username'] = user.username
        token['email'] = user.email
        return token

    def validate(self, attrs):
        """
        重写验证方法以自定义返回的数据结构。

        本方法旨在为登录成功后的用户生成一个特定格式的数据字典，
        包含用户ID、用户名、刷新令牌和访问令牌等信息。

        参数:
        - attrs: 包含用户输入的原始数据，例如用户名和密码。

        返回:
        - data: 包含用户信息和令牌的字典，用于登录成功后返回给客户端。
        """

        # 调用父类的validate方法进行基本验证并获取原始数据
        old_data = super().validate(attrs)

        # 生成刷新令牌
        refresh = self.get_token(self.user)

        # 构造返回给客户端的数据结构
        data = {
            'id': self.user.id,  # 用户ID
            'msg': '登录成功成功',  # 登录成功消息
            'username': self.user.username,  # 用户名
            'credit_to_money':CREDIT_MONEY,
            'user_credit':self.user.credit,
            'refresh': str(refresh),  # 刷新令牌
            'access': str(refresh.access_token)  # 访问令牌
        }

        # 返回构造的数据
        return data


from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from .models import User

import re


def get_account_by_mobile(account):
    """
    根据手机号或用户名获取用户账户信息。

    首先尝试根据输入的账户信息判断其是否为手机号（通过正则表达式验证），
    如果是手机号，则通过mobile字段查询User模型以获取用户信息；
    如果不是手机号，则通过username字段查询User模型以获取用户信息。
    如果查询不到对应的用户信息，则返回None。

    参数:
    account (str): 用户输入的账户信息，可以是手机号或用户名。

    返回:
    User or None: 返回查询到的用户对象，如果查询不到则返回None。
    """
    try:
        user = User.objects.filter(Q(username=account) | Q(mobile=account)).first()

        """
        上面的可以替换成,虽然还是会有问题，大概逻辑是下面这样的
        # 判断输入的账户信息是否符合手机号格式
        if re.match('1[3-9]\d{9}$', account):
            # 如果是手机号，通过mobile字段查询用户信息
            user = User.objects.get(mobile=account)
        else:
            # 如果不是手机号，通过username字段查询用户信息
            user = User.objects.get(username=account)
        """
    except User.DoesNotExist:
        # 如果查询不到对应的用户信息，返回None
        return None
    else:
        # 如果成功查询到用户信息，返回用户对象
        return user


class UsernameMobileAuthBackend(ModelBackend):
    """
    自定义用户认证后端，支持用户名或手机号码登录
    继承自Django的ModelBackend，重写了authenticate方法
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        用户认证方法
        :param request: HttpRequest对象，用于获取登录上下文（本例中未使用）
        :param username: 用户输入的用户名或手机号码
        :param password: 用户输入的密码
        :param kwargs: 其他额外的关键字参数
        :return: 返回通过认证的用户对象，如果认证失败则返回None
        """
        # 尝试通过用户名或手机号码获取用户对象
        user = get_account_by_mobile(username)

        # 检查用户是否存在、密码正确且用户已通过身份验证
        if user is not None and user.check_password(password) and user.is_authenticated:
            return user
        else:
            return None

from django.contrib.auth.hashers import make_password
from django_redis import get_redis_connection
class UserModelSerializer(serializers.ModelSerializer):
    # 定义短信验证码字段，用于反序列化时接收客户端提交的数据
    # write_only=True 表示该字段只在反序列化（即接收客户端提交的数据）时使用，在序列化（即返回给客户端的数据）时会被忽略。
    # allow_blank=False 表示不允许此字段为空
    # label="短信验证码" 表示字段的标签，用于在返回的JSON中显示字段的名称
    # error_messages 定义了各种错误情况下的错误提示信息
    sms_code = serializers.CharField(max_length=4, min_length=4, required=True, allow_blank=False,
                                     help_text="短信验证码",
                                     error_messages={
                                         "blank": "请输入短信验证码",
                                         "required": "请输入短信验证码",
                                         "max_length": "验证码格式错误",
                                         "min_length": "验证码格式错误",
                                     },
                                     write_only=True, label="短信验证码")
    # token字段用于返回客户端的token，该字段只在序列化（即返回给客户端的数据）时使用，在反序列化（即接收客户端提交的数据）时会被忽略。
    token = serializers.CharField(max_length=1024, read_only=True, help_text="token认证字符串")   # 存在于fields列表中

    class Meta:
        # 指定序列化器关联的模型类
        model = User
        # 定义需要序列化和反序列化的字段
        fields = ['id', 'username', 'password', 'token', 'mobile', 'sms_code']

        # 额外定义字段的参数
        # 因为后端不需要提供数据给客户端，但是一开始的models并没有加入write_only=True，所以这里需要加入一个extra_kwargs，进行额外字段声明
        extra_kwargs = {
            'mobile': {
                # 字段只在反序列化时使用，在序列化时忽略
                "write_only": True,
                # 设置手机号字段的最小长度和最大长度
                'min_length': 11,
                'max_length': 11,
                # 定义手机号字段的错误提示信息
                'error_messages': {
                    'min_length': '手机号长度错误',
                    'max_length': '手机号长度错误',
                }
            },
            "id": {
                "read_only": True
            },
            "username": {
                "read_only": True
            },
            "password": {
                "write_only": True
            },
        }

    def validate(self, attrs):
        """
        验证短信验证码
        :param attrs: 验证的数据
        :return: 验证后的数据
        """
        sms_code = attrs.get('sms_code')
        mobile = attrs.get('mobile')
        password = attrs.get('password')
        # 验证手机号码的格式
        if not re.match("^1[3-9]\d{9}$", mobile):
            raise serializers.ValidationError("您输入的手机号格式错误!")

        # 验证手机号是否已经被注释过了
        reg = get_account_by_mobile(mobile)
        if reg is not None:
            raise serializers.ValidationError("对不起，该手机号已经被注册!")

        # 验证短信验证码是否正确
        redis_conn = get_redis_connection("sms_code")
        real_sms_code = redis_conn.get("sms_%s" % mobile)

        # 本次验证以后，直接删除当前验证码，防止出现恶意暴力破解
        redis_conn.delete("sms_%s" % mobile)

        if real_sms_code is None:
            raise serializers.ValidationError("短信验证码不存在或已过期!")
        if real_sms_code.decode() != sms_code:
            raise serializers.ValidationError("短信验证码错误!，本次验证码已失效!，请重新发送")

        return attrs

    def create(self, validated_data):
        """保存用户数据"""
        validated_data.pop('sms_code')  # 因为数据库中没有sms_code字段，所以需要先删除该字段，否则会报错，而且该字段没有保存意义

        # 对密码进行加密
        raw_password = validated_data.get('password')
        hash_password = make_password(raw_password)  # 对密码进行加密
        mobile = validated_data.get('mobile')
        # 对用户名设置一个默认值
        username = validated_data.get('mobile')  # 默认用户名就是手机号
        # 调用序列化器提供的create方法，创建用户对象
        new_User = User.objects.create(
            mobile=mobile,
            username=username,
            password=hash_password,
        ) # 将用户数据保存到数据库中  xxx.objects.create()的参数必须是模型类中实际存在的字段

        # 生成JWT Token
        refresh = RefreshToken.for_user(new_User)
        # 将Token添加到返回的数据中
        new_User.token = str(refresh.access_token) # 动态添加了token属性到new_User实例，这是Python特性
        # 这只是在内存中为new_User实例添加了一个临时属性，并不会修改数据库表结构，也不会将token存入数据库

        return new_User  # 会传递给序列化器的序列化阶段这个实例会被序列化器用来生成最终的响应数据

from order.models import Order
class UserOrderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'order_number', 'order_status','create_time', 'course_list']
