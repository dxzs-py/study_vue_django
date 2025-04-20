# Register your models here.
from django.contrib import admin
from .models import CourseCategory
class CourseCategoryModelAdmin(admin.ModelAdmin):
    """课程分类模型管理类"""
    list_display = ["name","id"]
admin.site.register(CourseCategory, CourseCategoryModelAdmin)



from .models import Course
class CourseModelAdmin(admin.ModelAdmin):
    """课程模型管理类"""
    pass
admin.site.register(Course, CourseModelAdmin)


from .models import Teacher
class TeacherModelAdmin(admin.ModelAdmin):
    """老师模型管理类"""
    pass
admin.site.register(Teacher, TeacherModelAdmin)


from .models import CourseChapter
class CourseChapterModelAdmin(admin.ModelAdmin):
    """课程章节模型管理类"""
    pass
admin.site.register(CourseChapter, CourseChapterModelAdmin)



from .models import CourseLesson
class CourseLessonModelAdmin(admin.ModelAdmin):
    """课程课时模型管理类"""
    pass
admin.site.register(CourseLesson, CourseLessonModelAdmin)