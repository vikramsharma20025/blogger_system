from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('register',views.register,name='register'),
    path('add',views.add,name='add'),
    path('changepassword',views.change_pass,name='changepassword'),
    path('otpchecker',views.checkotp,name='otpchecker'),
    path('global',views.globalpage,name='globalpage'),
    path('comments/',views.commentsall,name='commentsall'),
    path('post/<str:title>',views.showpost,name='showpost'),
    path('user/<str:username>',views.showuser,name='showuser'),
    path('commentadding/<str:title>',views.commentadding,name='commentadding'),
    path('personalinfo',views.personalinfo,name='personalinfo'),
    path('comment/<str:title>/<int:id>',views.show_commentandreplies,name='showthiscomment'),
    path('addreply/<str:title>/<int:id>',views.addreply,name='addreply'),
    path('followuser/<str:username>/<str:usernameby>',views.followthis,name='followuser'),
    path('profile/update',views.update_profile,name='updateprofile'),
    path('post/update',views.update_post,name='updatepost'),
]
# features to be added
# theme
# stats
# search bar
# google authentication system
# update profile
# update blog

# channel not a feature
# telusko