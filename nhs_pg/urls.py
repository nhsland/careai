"""nhs_pg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as user_views
from django.views.static import serve
# from . import views
from django.conf.urls import url
from ckeditor_uploader import views as uploader_views
from django.views.decorators.cache import never_cache

urlpatterns = [
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^ckeditor/upload/',
        uploader_views.upload, name='ckeditor_upload'),
    url(r'^ckeditor/browse/',
        never_cache(uploader_views.browse), name='ckeditor_browse'),
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('challenges/', include('challenges.urls')),
    path('solutions/', include('solutions.urls')),
    path('discussion/', include('discussion.urls')),
    path('tutorial/', include('tutorial.urls')),
    path('register/', user_views.RegisterView.as_view(), name='register'),
    path('profile/<username>', user_views.specific_profile, name='specific_profile'),
    path('profile/', user_views.profile, name='profile'),
    path('register/developer/', user_views.DeveloperRegisterView.as_view(), name='developer_register'),
    path('register/clinician/', user_views.ClinicianRegisterView.as_view(), name='clinician_register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


