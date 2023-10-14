from django.urls import path 
from . import views
from django.urls import re_path

urlpatterns = [
    path('add/',views.addEvent),
    path('get/',views.eventList),
    path('report/add/',views.addReport),
    path('participant/add/',views.addParticipant),
    path('participant/get/',views.participantList),
    path('organizer/add/',views.addOrganizer),
    path('organizer/get/',views.organizerList),
    path('report/get/',views.getReport),
    path('club/get/',views.getClubList),
    path('approvals/get/',views.eventApprovals),
    path('approval/',views.signEvent),
    path('certificate/',views.downloadCertificate),
    re_path(r'^certificate/verify/$',views.verifyEvent)
]