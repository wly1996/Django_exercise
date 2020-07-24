from django.urls import path
from . import views

app_name = 'blog' #定义显示的网站的名称

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'), #将原来的Index视图修改为新更改的类视图
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name = 'detail'), #添加文章详情页
    path('archives/<int:year>/<int:month>', views.ArchiveView.as_view(), name = 'archive'), #添加按照日期归档文章
    path('categories/<int:pk>/', views.CategoryView.as_view(), name = 'category'), #添加根据分类归档文章,并修改为类视图
    path('tags/<int:pk>/', views.TagView.as_view(), name = 'tag'), #根据标签来分类文章，并修改为类视图
]