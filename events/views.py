from django.shortcuts import render
from home.views import auth
from events import models
from home.models import club,student
from django.http import JsonResponse
import json
from datetime import datetime
from .pdfgen import generate_certificate
from django.http import FileResponse
import io
from edcred.settings import configFile

# Create your views here.

def addEvent(request):
    req_body = request.body.decode('utf-8')
    message,status = auth(req_body=req_body)
    req = json.loads(req_body)
    print(message,req)
    if status==200 and message["group"]=="clubs":
        try:
            req_body = request.body.decode('utf-8')
            req = json.loads(req_body)
            clubId =  club.objects.get(id=message["id"])
            dateStr  = datetime.strptime(req["date"], "%Y-%m-%d").date()
            new = models.event(name=req["name"],club=clubId,date=dateStr,details=req["details"])
            new.save()
        except Exception as e:
            print("ERROR:",e)
            message['message'] = "FAILURE"
            status = 404
    else:
        message['message'] = "FAILURE"
        status = 401
    return JsonResponse(message,status=status)

    
def eventList(request):
    req_body = request.body.decode('utf-8')
    message,status = auth(req_body=req_body)
    req = json.loads(req_body)
    print(message,req)
    eventList = list()
    if status==200:
        if message['group']=="clubs":
            clubId =  club.objects.get(id=message["id"])
            message["name"] = clubId.name
            events = models.event.objects.filter(club__id=message['id'])
            eventList = list()
            for event in  events:
                eventList.append({
                    "id" : event.id,
                    "name":event.name,
                    "date":event.date,
                    "details":event.details,
                    "status":event.signed
                })
            message["events"] = eventList
        elif message['group']=="students":
            events = models.event.objects.filter(participants__srn__srn=message["id"])
            for event in  events:
                if event.club!=None:
                    eventList.append({
                        "id" : event.id,
                        "name":event.name,
                        "date":event.date,
                        "details":event.details,
                        "status":event.signed,
                        "clubId":event.club.id,
                        "clubName":event.club.name,
                    })
                else:
                    eventList.append({
                        "id" : event.id,
                        "name":event.name,
                        "date":event.date,
                        "details":event.details,
                        "status":event.signed,
                        "clubId":None,
                        "clubName":None,
                    })
            message["events"] = eventList
        elif message['group']=="faculties":
            try:
                req_body = request.body.decode('utf-8')
                req = json.loads(req_body)
                clubId = club.objects.get(id = req['club'])
                message["name"] = clubId.name
                events =  models.event.objects.filter(club=clubId)
                for event in  events:
                    eventList.append({
                        "id" : event.id,
                        "name":event.name,
                        "date":event.date,
                        "details":event.details,
                        "status":event.signed
                    })   
            except:
                pass
            message["events"] = eventList
        else:
            message['message'] = "FAILURE"
            status = 401
    return JsonResponse(message,status=status)

def addReport(request):
    req_body = request.POST.get('request')
    file = request.FILES.get('file')
    print(file)
    req = json.loads(req_body)
    message,status = auth(req_body=req_body)
    if status==200:
        if message['group']=="clubs":
            try:
                eventId = models.event.objects.get(id=req["eventid"])
                eventId.signed = 0
                eventId.save()
                new = models.report(
                    details = req["details"],
                    img = file,
                    event = eventId
                )
                new.save()
            except Exception as e:
                print("ERROR:",e)
                message['message'] = "FAILURE"
                status = 401
        else:
            message['message'] = "FAILURE"
            status = 401
        return JsonResponse(message,status=status)

def getLeaderBoard(request):
    req_body = request.body.decode('utf-8')
    message,status = auth(req_body=req_body)
    req = json.loads(req_body)
    print(message,req)
    try:
        students = student.objects.all().order_by('-crypto')
        studentsList = []
        rank = 0
        for eachStudent in students:
            rank += 1
            studentsList.append({
                "name":eachStudent.name,
                "srn":eachStudent.srn,
                "rank":rank
            })
        message["leaderboard"] = studentsList
    except:
        message['message'] = "FAILURE"
        status = 401
    return JsonResponse(message,status=status)

def addParticipant(request):
    req_body = request.POST.get('request')
    try:
        file = request.FILES.get('file')
    except:
        pass
    message,status = auth(req_body=req_body)
    req = json.loads(req_body)
    print(message,status,req)
    if status==200:
        if message['group']=="clubs":
            try:
                eventId = models.event.objects.get(id=req["eventid"])
                srn = student.objects.get(srn=req["srn"])
                new = models.participant(
                    srn = srn,
                    event = eventId,
                    position = int(req["pos"])
                )
                new.save()
                srn.crypto = srn.crypto + 1/(new.position)
                print(srn.crypto)
                srn.save()

            except Exception as e:
                print("ERROR:",e)
                message['message'] = "FAILURE"
                status = 404
        elif message['group']=="students":
            try:
                srn = student.objects.get(srn=message["id"])
                newEvent = models.event(
                    name = req["title"],
                    date  = datetime.strptime(req["date"], "%Y-%m-%d").date(),
                    details = req["subject"]
                )
                newEvent.save()
                newParticipant = models.participant(
                    srn = srn,
                    event = newEvent
                )
                newParticipant.save()
                newReport = models.report(
                    details = req["details"],
                    img = file,
                    event = newEvent
                )
                newReport.save()
                newEvent.signed = 0
                newEvent.save()
            except Exception as e:
                print(e)
                message['message'] = "FAILURE"
                status = 404
        else:
            message['message'] = "FAILURE"
            status = 401
    return JsonResponse(message,status=status)

def participantList(request):
    req_body = request.body.decode('utf-8')
    message,status = auth(req_body=req_body)
    req = json.loads(req_body)
    print(message,req)
    participant_list = list()
    if status==200:
        print(req)
        eventId = models.event.objects.get(id=req["eventid"])
        participants = models.participant.objects.filter(event=eventId)
        print(participants)
        for participant in  participants:
            participant_list.append({
                "srn" : participant.srn.srn,
                "name":participant.srn.name,
            })
        message["participants"] = participant_list
    return JsonResponse(message,status=status)

def addOrganizer(request):
    req_body = request.body.decode('utf-8')
    message,status = auth(req_body=req_body)
    print(message,status)
    if status==200:
        if message['group']=="clubs":
            try:
                req = json.loads(req_body)
                eventId = models.event.objects.get(id=req["eventid"])
                srn = student.objects.get(srn=req["srn"])
                new = models.organizer(
                    srn = srn,
                    event = eventId,
                    role = req["role"],
                )
                new.save()
            except Exception as e:
                print("ERROR:",e)
                message['message'] = "FAILURE"
                status = 401
        else:
            message['message'] = "FAILURE"
            status = 401
    return JsonResponse(message,status=status)

def organizerList(request):
    req_body = request.body.decode('utf-8')
    message,status = auth(req_body=req_body)
    if status==200:
        organizer_list = list()
        req = json.loads(req_body)
        print(req)
        eventId = models.event.objects.get(id=req["eventid"])
        organizers = models.organizer.objects.filter(event=eventId)
        print(organizers)
        for organizer in  organizers:
            organizer_list.append({
                "srn" : organizer.srn.srn,
                "name":organizer.srn.name,
                "role" : organizer.role,
            })
        message["organizers"] = organizer_list
    return JsonResponse(message,status=status)

def getReport(request):
    req_body = request.body.decode('utf-8')
    message,status = auth(req_body=req_body)
    if status==200:
        try:
            req_object = request.body.decode('utf-8')
            req = json.loads(req_object)
            report_obj = models.report.objects.filter(event__id=req["eventid"]).first()
            print(report_obj)
            image_url = report_obj.img.url
            message["image"] = image_url
            message["report"] = report_obj.details
        except Exception as e:
                print("ERROR:",e)
                message['message'] = "FAILURE"
                status = 404
    else:
        message['message'] = "FAILURE"
        status = 401
    return JsonResponse(message,status=status)   

def getClubList(request):
    req_body = request.body.decode('utf-8')
    message,status = auth(req_body=req_body)
    req = json.loads(req_body)
    print(message,req)
    if status==200:
        try:
            clubList = list()
            clubs = club.objects.all()
            for Itr in clubs:
                clubList.append({
                    "name" : Itr.name,
                    "id" : Itr.id,
                    "headSRN" : Itr.head.srn,
                    "headName": Itr.head.name,
                    "facultyId" : Itr.faculty.id,
                    "facultyName":Itr.faculty.name,
                })
            message["clubs"] = clubList
        except Exception as e:
                print("ERROR:",e)
                message['message'] = "FAILURE"
                status = 404
    else:
        message['message'] = "FAILURE"
        status = 401
    return JsonResponse(message,status=status)  

def eventApprovals(request):
    req_body = request.body.decode('utf-8')
    message,status = auth(req_body=req_body)
    req = json.loads(req_body)
    print(message,req)
    if status==200:
        try:
            unsignedClubEventsList = list()
            unsignedExtraEventsList = list()
            if message["group"] == "faculties":
                unsignedClubEvents = models.event.objects.filter(signed=0,club__faculty__id=message["id"])
                unsignedExtraEvents = models.event.objects.filter(signed=0,club=None)

                for itr in unsignedClubEvents:
                    unsignedClubEventsList.append({
                        "id" : itr.id,
                        "name":itr.name,
                        "date":itr.date,
                        "details":itr.details,
                        "clubId":itr.club.id,
                        "clubName":itr.club.name
                    })
                for itr in unsignedExtraEvents:
                    unsignedExtraEventsList.append({
                        "id" : itr.id,
                        "name":itr.name,
                        "date":itr.date,
                        "details":itr.details,
                        "status":itr.signed,
                        "srn": itr.participants.first().srn.srn,
                        "student":itr.participants.first().srn.name,
                    })
                    
            message["clubEvents"] = unsignedClubEventsList
            message["extraEvents"] = unsignedExtraEventsList
                
        except Exception as e:
            print("ERROR:",e)
            message['message'] = "FAILURE"
            status = 404
    else:
        message['message'] = "FAILURE"
        status = 401
    return JsonResponse(message,status=status)
                
def signEvent(request):
    req_body = request.body.decode('utf-8')
    message,status = auth(req_body=req_body)
    req = json.loads(req_body)
    print(message,req)
    if status==200 and message["group"]=="faculties":
        try:
            eventId = models.event.objects.get(id=req["eventid"])
            if req["result"] == True:
                eventId.signed = eventId.signed + 1
            else:
                eventId.signed = -1
            print(req["result"],eventId.signed)
            eventId.save()
        except Exception as e:
            print("ERROR:",e)
            message['message'] = "FAILURE"
            status = 404
    else:
        message['message'] = "FAILURE"
        status = 401
    return JsonResponse(message,status=status)
            
            
def downloadCertificate(request):
    req_body = request.body.decode('utf-8')
    message,status = auth(req_body=req_body)
    req = json.loads(req_body)
    print(message,req)
    if status==200 and message["group"]=="students":
        eventid_str = req["eventid"]
        srn = message["id"]
        event_name = models.event.objects.get(id=req["eventid"]).name
        student_name = student.objects.get(srn=message["id"]).name
        # Generate the PDF certificate
        path = configFile["DJANGO"]+f"/events/certificate/verify?eventid={eventid_str}&srn={srn}"
        buffer = generate_certificate(event_name, student_name,path)
        # Create a FileResponse with the buffer as the file content
        response = FileResponse(buffer, as_attachment=True, filename=f'{event_name}_{student_name}.pdf')
        print("certificate sent")
        return response
    return JsonResponse(message,status=401)

def verifyEvent(request):
    eventid = request.GET['eventid']
    srn = request.GET['srn']
    event = models.event.objects.filter(participants__srn__srn=srn, id=eventid).first()
    studentData = student.objects.get(srn=srn)
    
    if event is None:
        return render(request, 'verify_event.html', context={'event': None})
    else:
        return render(request, 'verify_event.html', context={'event': event,'student':studentData})
    