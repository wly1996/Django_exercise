import markdown
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags

# Create your models here.


class Category(models.Model): #分类
    name = models.CharField(max_length = 100)

    class Meta: #设置中文显示
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Tag(models.Model): #标签
    name = models.CharField(max_length = 100)

    class Meta: #设置中文显示
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Post(models.Model): #文章
    title = models.CharField('标题', max_length = 70) #标题

    body = models.TextField('正文') #正文

    created_time = models.DateTimeField('创建时间', default = timezone.now) #创建时间，并获取当前时间
    modified_time = models.DateTimeField('修改时间') #修改时间

    excerpt = models.CharField('摘要', max_length = 200, blank=True) #摘要，可以为空

    category = models.ForeignKey(Category, verbose_name = '分类', on_delete = models.CASCADE) #设置正文的分类

    tags = models.ManyToManyField(Tag, verbose_name = '标签', blank = True) #设置正文的标签，可以为空

    author = models.ForeignKey(User, verbose_name = '作者', on_delete = models.CASCADE) #设置作者

    class Meta: #设置中文显示
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs): #每次修改时自动获取当前时间
        self.modified_time = timezone.now()

        md = markdown.Markdown(extension = ['extra', 'codehilite',]) #自动摘取正文前N个自字符作为摘要
        self.excerpt = strip_tags(md.convert(self.body))[:54]

        super().save(*args, **kwargs)
    

    def __str__(self):
        return self.title

    def get_absolute_url(self): #获取文章详情
        return reverse('blog:detail', kwargs = {'pk': self.pk})