from django.urls import path
from django.contrib.auth import views as auth_view
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('sign-up/', views.sign_up, name='sign_up'),
    path('login/', views.login_view, name='login'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('post_detail/<int:pk>/', views.post_detail, name='post_detail'),
    path('post_edit/<int:pk>/', views.post_edit, name='post_edit'),
    path('post_delete/<int:pk>/', views.post_delete, name='post_delete'),
    path('password_reset/', auth_view.PasswordResetView.as_view(template_name='password/password_reset.html'),
         name='password_reset'),
    path('password_reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='password/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/', auth_view.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'),
         name='password_reset_complete'),
    path('search/', views.account_search_view, name="search"),
    path('chat/', views.chat_view, name='chat'),


]
