from django.conf.urls import url
from .views import *

urlpatterns = [
  #访问路径是http://localhost:8000/
  url(r'^$',index_views),
  #访问路径是http://localhost:8000/login
  url(r'^login/$',login_views,name='login'),
  #访问路径是http://localhost:8000/register
  url(r'^register/$',register_views,name='register'),

  #访问路径是http://localhost:8000/check_login/
  url(r'^check_login/$',check_login_views),
  # 访问路径是http://localhost:8000/check_logout/
  url(r'^logout/$',logout_views),
  # 访问路径是http://localhost:8000/check_uphone/
  url(r'^check_uphone/$',check_uphone_views),

  # 访问路径是http://localhost:8000/load_type_goods(加载、路径、商品)/
  url(r'^load_type_goods/$',load_type_goods),

]
