# Create your views here.

from rest_framework.generics import ListAPIView
from .models import CourseCategory
from .serializers import CourseCategoryModelSerializer


class CourseCategoryListAPIView(ListAPIView):
    """
    课程分类
    """
    queryset = CourseCategory.objects.filter(is_show=True, is_deleted=False).order_by("order", "-id")
    serializer_class = CourseCategoryModelSerializer


from .paginations import CustomPageNumberPagination
from .models import Course
from .serializers import CourseModelSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


class CourseListAPIView(ListAPIView):
    """课程列表"""
    queryset = Course.objects.filter(is_show=True, is_deleted=False).order_by("-id", "order")
    serializer_class = CourseModelSerializer  # 序列化器类
    # 指定过滤器类，DjangoFilterBackend是基于模型字段的过滤器
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["course_category"]  # 指定过滤字段，用户在 url中通过?course_category==xx指定过滤字段
    ordering_fields = ["id", "price", "students"]  # 指定排序字段，在url通过?ordering=xx指定排序字段
    pagination_class = CustomPageNumberPagination  # 指定分页器类 在url中通过传入?page=xx参数指定页码。还有很多参数


from rest_framework.generics import RetrieveAPIView
from .serializers import CourseRetrieveModelSerializer


class CourseRetrieveAPIView(RetrieveAPIView):
    queryset = Course.objects.filter(is_show=True, is_deleted=False).order_by("-id", "order")
    serializer_class = CourseRetrieveModelSerializer  # 序列化器类


from .models import CourseChapter
from .serializers import CourseChapterModelSerializer


class CourseChapterListAPIView(ListAPIView):
    queryset = CourseChapter.objects.filter(is_show=True, is_deleted=False).order_by("id", "order")
    serializer_class = CourseChapterModelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["course"]


"""2025/7/29"""
from luffyapi.libs.polyv import PolyvPlayer
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class PolyvPlayerAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """获取视频播放的token"""
        userId = settings.POLYV_CONFIG.get("userId")
        secretkey = settings.POLYV_CONFIG.get("secretkey")
        tokenUrl = settings.POLYV_CONFIG.get("tokenUrl")
        polyv = PolyvPlayer(userId, secretkey, tokenUrl)
        vid = request.query_params.get("vid")
        user_ip = request.META.get("REMOTE_ADDR")  # 用户的IP
        user_id = request.user.id  # 用户ID
        user_name = request.user.username  # 用户名

        result = polyv.get_video_token(vid, user_ip, user_id, user_name)
        return Response(result.get("token"))
