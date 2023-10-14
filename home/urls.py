from django.urls import path 
from . import views
from django.urls import re_path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login',views.login_api),
    path('logout',views.logout_api),
    path('auth',views.auth_api),
    path('student/profile',views.studentProfile),
    path('faculty/profile',views.facultyProfile),
    path('students/get',views.studentsList),
    re_path(r'^proxy/(.*)$', views.proxy_handler),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)