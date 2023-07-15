from django.urls import path
from . import views

urlpatterns = [
    path('register',views.register,name="register"),
    path('',views.logining,name="login"),
    path('logout',views.logouting,name="logout"),
    path('test', views.test, name='test'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('view_profile', views.view_profile, name='view_profile'),
    path('create_publication', views.create_publication, name='create_publication'),
    path('like', views.like, name='like'),
    path('comment', views.comment, name='comment'),
    path('comments_detail', views.comments_detail, name='comments_detail'),
]
