from django.contrib import admin

# Register your models here.
from index.models import *

#定义高级管理类
class GoodsAdmin(admin.ModelAdmin):
    #1.定义搜索字段
    search_fields = ('title',)
    #2.定义右侧的过滤器 暨 定义过滤器筛选字段
    list_filter = ('goodsType',)
    #3.定义在列表页中显示的数据字段
    list_display = ('title','price','spec')

admin.site.register(GoodsType)
admin.site.register(Goods,GoodsAdmin)
