from django.urls import path
from . import views

app_name = 'blog' #定义显示的网站的名称

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<int:pk>/', views.detail, name = 'detail') #添加文章详情页
]