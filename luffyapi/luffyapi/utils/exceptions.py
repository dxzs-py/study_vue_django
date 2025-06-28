from rest_framework.views import exception_handler
from django.db import DatabaseError
import logging
from rest_framework.response import Response
from rest_framework import status
from redis import RedisError
from django.http.response import HttpResponse

logger = logging.getLogger("django")


def custom_exception_handler(exc, context):
    """
    自定义异常处理
    :param exc: 异常类（本次请求发生的异常信息）
    :param context: 抛出异常的上下文[本次请求的request对象，异常发送的时间，信号等]
    :return: Response响应对象
    """
    # 调用drf框架原生的异常处理方法
    response = exception_handler(exc, context)
    if response is None:
        """来到这里就两中情况：要么程序没出错，要么是出错了但是Django或者restframework不识别"""
        view = context['view']
        if isinstance(exc, DatabaseError) or isinstance(exc,RedisError):
            # 数据库异常
            logger.error('[%s] %s' % (view, exc))
            response = Response({'message': '服务器内部错误'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)
        """ 也可以单独写出来
            if isinstance(exc, RedisError):
            # redis异常
            logger.error('[%s] %s' % (view, exc))
            response = Response({'message': 'redis数据库异常'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)
        """

    return response