from django.urls import path
from . import views
from  .views import log_confirm


#app_name='login_and_signups'  #I made dir in template so I need this I think....

urlpatterns = [
    #login_and_signups
    path('',views.welcome, name='welcome'),
    path('login_admin/',views.login_admin,name='login_admin'),
    path('login_common/',views.login_common,name='login_common'),
    path('login_staff/',views.login_staff, name='login_staff'),
    path('signup_admin/',views.signup_admin, name='signup_admin'),
    path('signup_common/',views.signup_common,name='signup_common'),
    path('signup_staff/',views.signup_staff,name='signup_staff'),
    path('log_confirm/',views.log_confirm, name='log_confirm'),
    #not in other directories
    path('welcome/',views.welcome,name='welcome'),
    #authenticate
    path('admin_only/',views.admin_only,name='admin_only'),
    path('everyone/',views.everyone,name='everyone'),
    path('denied/',views.denied,name='denied'),
    path('no_commons/',views.no_commons,name='no_commons'),
    path('logout/',views.logout, name='logout'),
    #Board and Comments
    path('create/',views.create_post,name='create_post'),
    path('post_list/',views.post_list,name='post_list'),
    path('post/<int:post_id>/delete/',views.delete_post,name='delete_post'), #관련 post_id는 어떻게 처리된다기는 한다는데....전 후 관계를 모르겠다
    path('post/<int:post_id>/comments/',views.comment,name='comment'), #현재 sql에서 오류가 났으니 여기를 해결할 것
]