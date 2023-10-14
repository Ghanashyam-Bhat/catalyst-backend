from django.urls import path 
from . import views

urlpatterns = [
    path('add/',views.addnewProject),
    path('student/',views.addNewStudent),
    path('list/',views.listProjects),
    path('details/',views.projectDetails),
    path('approval/list/',views.approvalList),
    path('approval/',views.approve),
]