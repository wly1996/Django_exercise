from django.urls import path
from . import views

app_name = 'blog' #定义显示的网站的名称

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<int:pk>/', views.detail, name = 'detail'), #添加文章详情页
    path('archives/<int:year>/<int:month>', views.archive, name = 'archive'), #添加按照日期归档文章
    path('categories/<int:pk>/', views.category, name = 'category'), #添加根据分类归档文章
    path('tags/<int:pk>/', views.tag, name = 'tag'),

]