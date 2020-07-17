import markdown
import re
from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from .models import Post
from markdown.extensions.toc import TocExtension #导入美化标题的锚点URL

# Create your views here.

def index(request):
    post_list = Post.objects.all().order_by('-created_time')

    return render(request, 'blog/index.html', context={'post_list': post_list})

def detail(request, pk):
    post = get_object_or_404(Post, pk = pk)
    
    # md = markdown.markdown
    # exts = ['extra', 'codehilite', 'toc'] #将所有的扩展集中在一个数组里

    md = markdown.Markdown(extensions = ['extra', 'codehilite', TocExtension(slugify = slugify),]) #导入新的扩展

    post.body = md.convert(post.body)
    post.toc = md.toc

    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S) #使用政策表达式来判断是否为空目录
    post.toc = m.group(1) if m is None else ''


    return render(request, 'blog/detail.html', context = {'post': post})