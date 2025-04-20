from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView
from .models import CourseCategory
from .serializers import CourseCategoryModelSerializer
class CourseCategoryListAPIView(ListAPIView):
    """
    课程分类
    """
    queryset = CourseCategory.objects.filter(is_show=True, is_deleted=False).order_by("order","-id")
    serializer_class = CourseCategoryModelSerializer


from .paginations import CustomPageNumberPagination
from .models import Course
from .serializers import CourseModelSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
class CourseListAPIView(ListAPIView):
    """课程列表"""
    queryset = Course.objects.filter(is_show=True, is_deleted=False).order_by("-id","order")
    serializer_class = CourseModelSerializer  # 序列化器类
    # 指定过滤器类，DjangoFilterBackend是基于模型字段的过滤器
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_fields = ["course_category"]    # 指定过滤字段，用户在 url中通过?course_category==xx指定过滤字段
    ordering_fields = ["id","price","students"]  # 指定排序字段，在url通过?ordering=xx指定排序字段
    pagination_class = CustomPageNumberPagination  # 指定分页器类 在url中通过传入?page=xx参数指定页码。还有很多参数

from rest_framework.generics import RetrieveAPIView
class CourseRetrieveAPIView(RetrieveAPIView):
    queryset = Course.objects.filter(is_show=True, is_deleted=False).order_by("-id","order")
    serializer_class = CourseRetrieveModelSerializer  # 序列化器类