from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    #working category
    path('',views.index,name='index'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('register',views.register,name='register'),
    path('add',views.add,name='add'),
    path('search',views.search,name='search'),
    path('global',views.globalpage,name='globalpage'),
    path('comments/',views.commentsall,name='commentsall'),
    path('post/<str:title>',views.showpost,name='showpost'),
    path('user/<str:username>',views.showuser,name='showuser'),
    path('commentadding/<str:title>',views.commentadding,name='commentadding'),
    path('personalinfo',views.personalinfo,name='personalinfo'),
    path('comment/<str:title>/<int:id>',views.show_commentandreplies,name='showthiscomment'),
    path('addreply/<str:title>/<int:id>',views.addreply,name='addreply'),
    path('followuser/<str:username>/<str:usernameby>',views.followthis,name='followuser'),
    path('profileupdate',views.update_profile,name='updateprofile'),
    path('postupdate',views.update_post,name='postupdate'),
    #not working category
    path('about',views.about,name='about'),
    #waste category
    path('stats',views.stats,name='stats'),
    # otp checker and change password problem
    path('changepassword',views.change_pass,name='changepassword'),
    path('otpchecker',views.change_pass_otp,name='otpchecker'),
    
]
#<div class="desc">{{ i.desc }}</div>
# features to be added

# channel not a feature
# telusko


# <div class="title">
#                 <label for="title">Title</label>
#                 <input type="text" name="title" id="title">
#             </div>
#             <div class="descs">
#                 <label for="description">Description</label>
#                 <textarea name="desc" id="desc" cols="30" rows="10"></textarea>
#             </div>
#             <div class="submitbutton">
#                 <button type="submit">Done</button>
#             </div>
