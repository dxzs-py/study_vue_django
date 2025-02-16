from django.contrib import admin

# Register your models here.
from django.contrib import admin

admin.site.site_header = '戴兴django学习后端'  # 设置header
admin.site.site_title = '戴兴学习后端'  # 设置title
admin.site.index_title = '戴兴django学习'

from .models import Banner

admin.site.register(Banner)

