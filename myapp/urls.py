"""mysiteF19 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import include
from django.contrib import admin
from django.urls import path
from django.conf.urls import *
from myapp import views
from django.contrib.auth import views as auth_views

app_name = 'myapp'

urlpatterns = [
    path(r'about/', views.about, name='about_page'),
    path(r'<int:book_id>/', views.DetailView.as_view(), name='detail'),
    path(r'', views.IndexView.as_view(), name='index'),
    path(r'findbooks/', views.findbooks, name='findbooks'),
    path(r'place_order/', views.place_order, name='place_order'),
    path(r'review/', views.review, name='review'),
    path(r'login/', views.user_login, name='login'),
    path(r'logout/', views.user_logout, name='logout'),
    path(r'chk_reviews/<int:book_id>', views.chk_reviews, name='chk_reviews'),
    path(r'member_order/', views.myorders, name='myorders'),
    path(r'user_signup', views.user_signup, name='user_signup'),
    # path(r'cookie', views.test_cookie, name='cookie')
 path(r'password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
         name='password_change_done'),

    path(r'password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'),name='password_change'),

    path(r'password_reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),

    path(r'reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path(r'password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

    path(r'reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),

    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),

    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]

