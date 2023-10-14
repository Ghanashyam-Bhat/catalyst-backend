from django.http import JsonResponse
import json
from home.views import auth
from home.models import student,subject,faculty
from attendance import models
from datetime import datetime
from dateutil.parser import parse
from events.models import event

# Create your views here.
def addDeclaration(request):
    req_body = request.POST.get('request')
    file = request.FILES.get('file')
    message,status = auth(req_body=req_body)
    req = json.loads(req_body)
    if status==200:
        try:
            srn = student.objects.get(srn=message["id"])
            new = models.declaration(
                student = srn,
                signed = 0,
                doc = file
            )
            new.save()
        except Exception as e:
                print("ERROR:",e)
                message['message'] = "FAILURE"
                status = 404
    else:
        message['message'] = "FAILURE"
        status = 401
    return JsonResponse(message,status=status)
        
        
def addAttendanceRequest(request):
    req_body = request.body.decode('utf-8')
    message,status = auth(req_body=req_body)
    req = json.loads(req_body)
    print(req,message)
    if status==200:
        try:
            srn = student.objects.get(srn=message["id"])
            eventId = event.objects.get(id=req["eventid"])
            newForm = models.attendaceRequest(
                student = srn,
                signed = 0,
                event = eventId
            )
            newForm.save()
            total = 0
            for iter in req["attendancerequest"]:
                start_datetime = parse(iter["start"]).time()
                end_datetime = parse(iter["end"]).time()
                new = models.subjectAttendaceRequest(
                    subject = subject.objects.get(id=iter["subject"]),
                    form = newForm,
                    date = datetime.strptime(iter["date"], "%Y-%m-%d").date(),
                    start = start_datetime,
                    end = end_datetime,
                )
                new.save()
                time_difference = datetime.combine(datetime.today(), end_datetime) - datetime.combine(datetime.today(), start_datetime)
                total += time_difference.total_seconds() // 3600
            newForm.total = total 
            newForm.save()
        except Exception as e:
            print("ERROR:",e)
            message['message'] = "FAILURE"
            status = 404
    else:
        message['message'] = "FAILURE"
        status = 401
    return JsonResponse(message,status=status)


def getDeclaration(request):
    req_body = request.body.decode('utf-8')
    message,status = auth(req_body=req_body)
    req = json.loads(req_body)
    print(message,req)
    declarationList = list()
    if status==200 :
        try:
            declarations = ["hehe"]
            if message["group"]=="faculties":
                facultyId = faculty.objects.get(id=message["id"])
                if facultyId.access == 1:
                    declarations = models.declaration.objects.filter(student__fams__faculty__id=message["id"], signed = 0)
                elif facultyId.access == 2:
                    declarations = models.declaration.objects.filter(student__department__chairperson__id = facultyId.id, signed = 1)
                elif facultyId.access == 3:
                    declarations = models.declaration.objects.filter(signed = 2)
                        
            elif message["group"] == "students":
                declarations = models.declaration.objects.filter(student__srn=message["id"])
            
            for itr in declarations:
                declarationList.append({
                    "srn":itr.student.srn,
                    "name":itr.student.name,
                    "doc":itr.doc.url,
                    "id":itr.id,
                    "status" : itr.signed,
                    })
    
            message["declaration"] = declarationList
        except Exception as e:
            print("ERROR:",e)
            message['message'] = "FAILURE"
            status = 404
    else:
        message['message'] = "FAILURE"
        status = 401
    return JsonResponse(message,status=status)

def signDeclaration(request):
    req_body = request.body.decode('utf-8')
    message,status = auth(req_body=req_body)
    req = json.loads(req_body)
    print(message,req)    
    if status==200 and message["group"]=="faculties":
        try:
            declaration = models.declaration.objects.get(id=req["id"])
            if req["result"] == True:
                declaration.signed = declaration.signed + 1
            else:
                declaration.signed = -1
            declaration.save()
        except Exception as e:
            print("ERROR:",e)
            message['message'] = "FAILURE"
            status = 404
    else:
        message['message'] = "FAILURE"
        status = 401
    return JsonResponse(message,status=status)

def getAttendanceRequest(request):
    req_body = request.body.decode('utf-8')
    message,status = auth(req_body=req_body)
    req = json.loads(req_body)
    print(message,req)  
    attendenceRequestList = list()  
    if status==200:
        try:
            attendenceRequest = list()
            if message["group"] == "clubs":
                attendenceRequest = models.attendaceRequest.objects.filter(event__club__id=message["id"],signed=0)
            elif message["group"] == "faculties":
                facultyId = faculty.objects.get(id=message["id"])
                if facultyId.access == 1:
                    attendenceRequest = models.attendaceRequest.objects.filter(student__fams__faculty__id=message["id"], signed = 1)
                elif facultyId.access == 2:
                    attendenceRequest = models.attendaceRequest.objects.filter(student__department__chairperson__id = facultyId.id, signed = 2)
                elif facultyId.access == 3:
                    attendenceRequest = models.attendaceRequest.objects.filter(signed = 3)
                
            for itr in attendenceRequest:
                attendenceRequestList.append({
                    "id":itr.id,
                    "srn":itr.student.srn,
                    "name":itr.student.name,
                    "eventid":itr.event.id,
                    "eventname":itr.event.name,
                    "status":itr.signed,
                    "cgpa":itr.student.cgpa,
                    "total":itr.total,
                    "department":itr.student.department.id,
                })
            message["attendanceRequest"] = attendenceRequestList
        except Exception as e:
            print("ERROR:",e)
            message['message'] = "FAILURE"
            status = 404
    else:
        message['message'] = "FAILURE"
        status = 401
    return JsonResponse(message,status=status)

def getAttendanceRequestDetails(request):
    req_body = request.body.decode('utf-8')
    message,status = auth(req_body=req_body)
    req = json.loads(req_body)
    print(message,req)  
    attendenceRequestDetails = list()  
    if status==200:
        try:
            subjectAttendance = models.subjectAttendaceRequest.objects.filter(form__id=req["id"])   
            for itr in subjectAttendance:
                attendance = models.studentcourse.objects.filter(subject__id=itr.subject.id,student__srn=itr.form.student.srn).first()
                attendenceRequestDetails.append({
                    "id":itr.id,
                    "subject":itr.subject.id,
                    "subjectName":itr.subject.name,
                    "date":itr.date,
                    "starttime":itr.start,
                    "endtime":itr.end,
                    "current": attendance.attendance,
                })
            message["subjectAttendance"] = attendenceRequestDetails
        except Exception as e:
            print("ERROR:",e)
            message['message'] = "FAILURE"
            status = 404
    else:
        message['message'] = "FAILURE"
        status = 401
    return JsonResponse(message,status=status)



def attendanceApproval(request):
    req_body = request.body.decode('utf-8')
    message,status = auth(req_body=req_body)
    req = json.loads(req_body)
    print(message,req)  
    if status==200:
        try:
            if message["group"] == "faculties":
                for itr in req["data"]:
                    attendenceRequest = models.attendaceRequest.objects.get(id = itr["id"])
                    if itr["result"] == True:
                        attendenceRequest.signed = attendenceRequest.signed + 1
                    else:
                        attendenceRequest.signed = -1
                    attendenceRequest.save()
            elif message["group"] == "clubs":
                attendenceRequest = models.attendaceRequest.objects.get(id = req["id"])
                if req["result"] == True:
                    attendenceRequest.signed = attendenceRequest.signed + 1
                else:
                    attendenceRequest.signed = -1
                attendenceRequest.save()
        except Exception as e:
            print("ERROR:",e)
            message['message'] = "FAILURE"
            status = 401
    else:
        message['message'] = "FAILURE"
        status = 401
    return JsonResponse(message,status=status)
