from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model): #分类
    name = models.CharField(max_length = 100)

class Tag(models.Model): #标签
    name = models.CharField(max_length = 100)

class Post(models.Model): #文章
    title = models.CharField(max_length = 70) #标题

    body = models.TextField() #正文

    created_time = models.DateTimeField() #创建时间
    modified_time = models.DateTimeField() #修改时间

    excerpt = models.CharField(max_length = 200, blank=True) #摘要，可以为空

    category = models.ForeignKey(Category, on_delete = models.CASCADE) #设置正文的分类

    tags = models.ManyToManyField(Tag, blank = True) #设置正文的标签，可以为空

    author = models.ForeignKey(User, on_delete = models.CASCADE) #设置作者
