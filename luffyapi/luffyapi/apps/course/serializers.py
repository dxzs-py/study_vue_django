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
    列表课程信息序列化器
    """
    # 序列化器嵌套，返回外检对应的序列化器数据
    teacher = TeacherModelSerializer()
    class Meta:
        model = Course
        fields = ["id","name","course_img","students","lessons","pub_lessons","price","teacher","lessons_list","discount_name","real_price"]


class TeacherRetrieveModelSerializer(TeacherModelSerializer):
    """
    课程详情专用的讲师序列化器（继承原有字段并扩展）
    """
    class Meta(TeacherModelSerializer.Meta):
        fields = TeacherModelSerializer.Meta.fields + ["brief", "image",]


class CourseRetrieveModelSerializer(serializers.ModelSerializer):
    """
    课程详情信息序列化器
    """
    teacher = TeacherRetrieveModelSerializer()
    class Meta:
        model = Course
        fields = ["id","name","course_img","course_video","students","lessons","pub_lessons","price","teacher","level_name","brief_html","course_video","discount_name","real_price","activity_time"]

from .models import CourseLesson
class CourseLessonModelSerializer(serializers.ModelSerializer):
    """
    课程章节信息序列化器
    """
    class Meta:
        model = CourseLesson
        fields = ["id","name","duration","free_trail","section_type","section_link"]

from .models import CourseChapter
class CourseChapterModelSerializer(serializers.ModelSerializer):
    """
    详细页课程章节列表
    """
    coursesections = CourseLessonModelSerializer(many=True)
    class Meta:
        model = CourseChapter
        fields = ["id","chapter","name","coursesections"]