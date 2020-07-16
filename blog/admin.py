from django.contrib import admin
from .models import Post, Category, Tag

# Register your models here.

class PostAdmin(admin.ModelAdmin): #显示文章详细信息
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author']
    fields = ['title', 'body', 'excerpt', 'category', 'tags'] #优化新增文章的表单

    def save_model(self, request, obj, form, change): #自动获取当前登陆的用户作为作者
        obj.author = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
