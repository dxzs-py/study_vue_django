from django.urls import path
from . import views

urlpatterns = [
    path(r'category/', views.CourseCategoryListAPIView.as_view()),
    path(r'', views.CourseListAPIView.as_view()),
]
