import markdown
import re
from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from .models import Post, Category, Tag #引入Category,Tag类
from markdown.extensions.toc import TocExtension #导入美化标题的锚点URL
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger #添加分页功能

# Create your views here.

'''
def index(request):
    post_list = Post.objects.all().order_by('-created_time')

    return render(request, 'blog/index.html', context={'post_list': post_list})
'''

class IndexView(ListView): #将Index视图函数改写为类视图
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 10 # 每页显示十篇文章

'''
def detail(request, pk):
    post = get_object_or_404(Post, pk = pk)
    post.increase_views() #阅读量+1
    # md = markdown.markdown
    # exts = ['extra', 'codehilite', 'toc'] #将所有的扩展集中在一个数组里

    md = markdown.Markdown(extensions = ['extra', 'codehilite', TocExtension(slugify = slugify),]) #导入新的扩展

    post.body = md.convert(post.body)
    post.toc = md.toc

    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S) #使用政策表达式来判断是否为空目录
    post.toc = m.group(1) if m is None else ''


    return render(request, 'blog/detail.html', context = {'post': post})
'''

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        # 将文章阅读量 +1
        # 注意 self.object 的值就是被访问的文章 post
        self.object.increase_views()

        # 视图必须返回一个HttpResponse对象
        return response

    def get_object(self, queryset = None):
        # 覆写 get_object 方法的目的是因为需要对post的body值进行渲染
        post = super().get_object(queryset = None)
        md = markdown.Markdown(extensions = [
            'markdown.extensions.extra', 
            'markdown.extensions.codehilite', 
            TocExtension(slugify = slugify),
            ])
        post.body = md.convert(post.body)

        m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S) #使用正则表达式来判断是否为空目录
        post.toc = m.group(1) if m is None else ''

        return post

'''
def archive(request, year, month): #根据日期来分类文章
    post_list = Post.objects.filter(created_time__year = year, created_time__month = month).order_by('-created_time')
    return render(request, 'blog/index.html', context = {'post_list': post_list})
'''

class ArchiveView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get("year")
        month = self.kwargs.get("month")
        return super(ArchiveView, self).get_queryset().filter(created_time__year = year, created_time__month = month)

'''
def category(request, pk): #根据目录来分类文章
    cate = get_object_or_404(Category, pk = pk)
    post_list = Post.objects.filter(category = cate).order_by('-created_time')
    return render(request, 'blog/index.html', context = {'post_list': post_list})
'''

class CategoryView(IndexView): #同样改写为类视图，这里继承了IndexView类来进一步节省代码
    def get_queryset(self):
        cate = get_object_or_404(Category, pk = self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category = cate)

'''
def tag(request, pk): #根据标签来分类文章
    t= get_object_or_404(Tag, pk = pk)
    post_list = Post.objects.filter(tags = t).order_by('-created_time')
    return render(request, 'blog/index.html', context = {'post_list': post_list})
'''

class TagView(IndexView):
    def get_queryset(self):
        t = get_object_or_404(Tag, pk = self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags = t)
