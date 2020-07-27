# 添加“最新文章”模版标签功能

from django import template
from ..models import Post, Category, Tag

from django.db.models.aggregates import Count
from blog.models import Category

register = template.Library()

@register.inclusion_tag('blog/inclusions/_recent_posts.html', takes_context = True) #最新文章模板标签
def show_recent_posts(context, num = 5):
    return{'recent_post_list': Post.objects.all().order_by('-created_time')[:num],}

@register.inclusion_tag('blog/inclusions/_archives.html', takes_context = True) #归档模板标签
def show_archives(context): 
    return{'date_list': Post.objects.dates('created_time', 'month', order = 'DESC'),}

@register.inclusion_tag('blog/inclusions/_categories.html', takes_context = True) #分类模板标签
def show_categories(context):
    category_list = Category.objects.annotate(num_posts = Count('post')).filter(num_posts__gt = 0) #从数据库中取出所有文章并进行计数
    return{'category_list': category_list,}
    
@register.inclusion_tag('blog/inclusions/_tags.html', takes_context = True) #标签云模板标签
def show_tags(context):
    tag_list = Tag.objects.annotate(num_posts = Count('post')).filter(num_posts__gt = 0) #对Tag进行同样的操作
    return{'tag_list': tag_list,}