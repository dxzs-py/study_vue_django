# Register your models here.
from django.contrib import admin
from .models import CourseCategory


class CourseCategoryModelAdmin(admin.ModelAdmin):
    """课程分类模型管理类"""
    list_display = ["name", "id"]


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

from .models import CourseDiscountType


class CourseDiscountTypeModelAdmin(admin.ModelAdmin):
    """价格优惠类型"""
    pass


admin.site.register(CourseDiscountType, CourseDiscountTypeModelAdmin)

from .models import CourseDiscount


class CourseDiscountModelAdmin(admin.ModelAdmin):
    """价格优惠公式"""
    pass


admin.site.register(CourseDiscount, CourseDiscountModelAdmin)

from .models import Activity


class ActivityModelAdmin(admin.ModelAdmin):
    """商品活动模型"""
    pass


admin.site.register(Activity, ActivityModelAdmin)

from .models import CoursePriceDiscount


class CoursePriceDiscountModelAdmin(admin.ModelAdmin):
    """商品优惠和活动的关系"""
    pass


admin.site.register(CoursePriceDiscount, CoursePriceDiscountModelAdmin)

from .models import CourseExpire
class CourseExpireModelAdmin(admin.ModelAdmin):
    """商品有效期模型"""
    pass
admin.site.register(CourseExpire, CourseExpireModelAdmin)