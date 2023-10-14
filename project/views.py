from django.http import JsonResponse
import json
from home.views import auth
from project import models
from home.models import faculty,student,department
from events.models import event

# Create your views here.
def addnewProject(request):
    req_body = request.body.decode('utf-8')
    message,status = auth(req_body=req_body)
    req = json.loads(req_body)
    print(req,message)
    if status==200:
        try:
            if message["group"]=="students":
                if req["withCollege"] == True:
                    if req["category"]=="subject" :
                        newProject = models.project(
                            title = req["title"],
                            details = req["details"],
                            withCollege = req["withCollege"],
                            link = req["link"],
                            category = req["category"],
                            guide =  faculty.objects.get(id=req["guide"])
                        )
                    elif req["category"]=="capstone":
                        newProject = models.project(
                            title = req["title"],
                            details = req["details"],
                            withCollege = req["withCollege"],
                            link = req["link"],
                            category = req["category"],
                            guide =  faculty.objects.get(id=req["guide"]),
                            department = department.objects.get(id=req["department"])
                        )
                    elif req["category"]=="hackathon":
                        newProject = models.project(
                            title = req["title"],
                            details = req["details"],
                            withCollege = req["withCollege"],
                            link = req["link"],
                            category = req["category"],
                            hackathon =  event.objects.get(id=req["hackathon"])
                        )
                else:
                    newProject = models.project(
                            title = req["title"],
                            details = req["details"],
                            withCollege = req["withCollege"],
                            link = req["link"],
                            guide =  faculty.objects.get(id=req["guide"])
                        )
            newProject.save()
            new = models.studentProject(
                project = newProject,
                student = student.objects.get(srn=message["id"])
            )
            new.save()
        except Exception as e:
            print(e)
            message['message'] = "FAILURE"
            return JsonResponse(message,status=500)
    else:
        message['message'] = "FAILURE"
        status = 401
    return JsonResponse(message,status=status)

def addNewStudent(request):
    req_body = request.body.decode('utf-8')
    message,status = auth(req_body=req_body)
    req = json.loads(req_body)
    print(req,message)
    if status==200:
        try:
            if message["group"]=="students":
                new = models.studentProject(
                    project = models.project.objects.get(id=req["project"]),
                    student = student.objects.get(srn=message["id"])
                )
            new.save()
        except Exception as e:
            print(e)
            message['message'] = "FAILURE"
            return JsonResponse(message,status=404)
    else:
        message['message'] = "FAILURE"
        status = 401
    return JsonResponse(message,status=status) 
    
def listProjects(request):
    req_body = request.body.decode('utf-8')
    message,status = auth(req_body=req_body)
    req = json.loads(req_body)
    print(req,message)
    if status==200:
        try:
            projectsList = list()
            projects = models.project.objects.all()
            for project in projects:
                studentsList = list()
                students = models.studentProject.objects.filter(project__id = project.id)
                for itr in students:
                    studentsList.append({
                        "name":itr.student.name,
                        "srn":itr.student.srn
                    })
                guide = None 
                event = None
                department = None 
                try:
                    department = project.department.id
                except:
                    pass 
                try:
                    guide = project.guide.id 
                except:
                    pass 
                
                try:
                    event = project.hackathon.id
                except:
                    pass 
                
                projectsList.append({
                    "id":project.id,
                    "title":project.title,
                    "details":project.details,
                    "withCollege":project.withCollege,
                    "link":project.link,
                    "category":project.category,
                    "guide":guide,
                    "hackathon":event,
                    "completion":project.completion,
                    "approval":project.approval,
                    "department":department,
                    "students":studentsList
                })
            message["projects"] = projectsList
        except:
            message['message'] = "FAILURE"
            status = 404
    else:
        message['message'] = "FAILURE"
        status = 401
    return JsonResponse(message,status=status)

def projectDetails(request):
    req_body = request.body.decode('utf-8')
    message,status = auth(req_body=req_body)
    req = json.loads(req_body)
    print(req,message)
    
    if status==200:
        try:
            studentsList = list()
            project = models.project.objects.get(id=req["project"])
            students = models.studentProject.objects.filter(project__id = project.id)
            for itr in students:
                studentsList.append({
                    "name":itr.student.name,
                    "srn":itr.student.srn
                })
            guide = None 
            event = None
            department = None 
            try:
                department = project.department.id
            except:
                pass 
            
            try:
                guide = project.guide.id 
            except:
                pass 
            
            try:
                event = project.hackathon.id
            except:
                pass 
            
            projectsDetails = {
                "id":project.id,
                "title":project.title,
                "details":project.details,
                "withCollege":project.withCollege,
                "link":project.link,
                "category":project.category,
                "guide":guide,
                "hackathon":event,
                "completion":project.completion,
                "approval":project.approval,
                "department":department,
                "students":studentsList
            }
            message["details"] = projectsDetails 
        except:
            message['message'] = "FAILURE"
            status = 404
    else:
        message['message'] = "FAILURE"
        status = 401
    return JsonResponse(message,status=status)

def approvalList(request):
    req_body = request.body.decode('utf-8')
    message,status = auth(req_body=req_body)
    req = json.loads(req_body)
    print(req,message)
    if status==200:
        # try:
            projectsList = list()
            projectsSub = list()
            projectsHack = list()
            projectsCap = list()
            projectExt = list()
            if message["group"] == "clubs":
                projectsHack = list(models.project.objects.filter(hackathon__club__id=message["id"],approval=0,category="hackathon",withCollege=True) )
            elif message["group"] == "faculties":
                facultyId = faculty.objects.get(id=message["id"])
                if facultyId.access >= 1:
                    projectsSub = list(models.project.objects.filter(guide__id=message["id"],approval=0,category="subject",withCollege=True))
                    projectsHack = list(models.project.objects.filter(guide__id=message["id"],approval=1,category="hackathon",withCollege=True)) 
                    projectsCap = list(models.project.objects.filter(guide__id=message["id"],approval=0,category="capstone",withCollege=True))
                    projectExt = list(models.project.objects.filter(guide__id=message["id"],approval=0,withCollege=False))
                elif facultyId.access == 2:
                    projectsCap = list(models.project.objects.filter(department__chairperson__id=message["id"],approval=0,category="capstone",withCollege=True) )
            projects = projectsSub+projectsHack+projectsCap+projectExt
            for project in projects:
                studentsList = list()
                students = models.studentProject.objects.filter(project__id = project.id)
                for itr in students:
                    studentsList.append({
                        "name":itr.student.name,
                        "srn":itr.student.srn
                    })
                guide = None 
                event = None
                department = None 
                try:
                    department = project.department.id
                except:
                    pass 
                
                try:
                    guide = project.guide.id 
                except:
                    pass 
                
                try:
                    event = project.hackathon.id
                except:
                    pass 
                
                projectsList.append({
                    "id":project.id,
                    "title":project.title,
                    "details":project.details,
                    "withCollege":project.withCollege,
                    "link":project.link,
                    "category":project.category,
                    "guide":guide,
                    "hackathon":event,
                    "completion":project.completion,
                    "approval":project.approval,
                    "department":department,
                    "students":studentsList,
                })
            message["projects"] = projectsList
        # except:
        #     message['message'] = "FAILURE"
        #     status = 404
    else:
        message['message'] = "FAILURE"
        status = 401
    return JsonResponse(message,status=status)
    
def approve(request):
    req_body = request.body.decode('utf-8')
    message,status = auth(req_body=req_body)
    req = json.loads(req_body)
    print(req,message)
    if status==200 and (message["group"] == "clubs" or message["group"] == "faculties"):
        try:
            project = models.project.objects.get(id=req["id"])
            if req["approval"] == True:
                project.approval = project.approval + 1
            else:
                project.approval = -1
                
            if req["completion"] != None:
                project.completion = req["completion"]
            project.save()
        except:
            message['message'] = "FAILURE"
            status = 500
    else:
        message['message'] = "FAILURE"
        status = 401
    return JsonResponse(message,status=status)