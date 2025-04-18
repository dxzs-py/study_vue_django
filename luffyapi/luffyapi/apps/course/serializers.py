from rest_framework import serializers
from .models import CourseCategory
class CourseCategoryModelSerializer(serializers.ModelSerializer):
    """
    课程分类序列化器
    """
    class Meta:
        model = CourseCategory
        fields = ["id","name"]


from .models import Course,Teacher
class TeacherModelSerializer(serializers.ModelSerializer):
    """
    讲师信息序列化器
    """
    class Meta:
        model = Teacher
        fields = ["name","title","signature",]


class CourseModelSerializer(serializers.ModelSerializer):
    """
    课程信息序列化器
    """
    # 序列化器嵌套，返回外检对应的序列化器数据
    teacher = TeacherModelSerializer()
    class Meta:
        model = Course
        fields = ["id","name","course_img","students","lessons","pub_lessons","price","teacher","lessons_list"]