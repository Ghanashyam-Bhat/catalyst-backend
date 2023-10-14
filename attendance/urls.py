from django.urls import path 
from . import views

urlpatterns = [
    path('declaration/add/',views.addDeclaration),
    path('request/add/',views.addAttendanceRequest),
    path('declaration/get/',views.getDeclaration),
    path('declaration/sign/',views.signDeclaration),
    path('request/get/',views.getAttendanceRequest),
    path('request/details/',views.getAttendanceRequestDetails),
    path('approval/',views.attendanceApproval),
]