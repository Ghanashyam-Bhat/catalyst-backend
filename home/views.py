from django.http import HttpResponse
from django.contrib.auth import authenticate,login
from django.http import JsonResponse
import json
from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model
import http.client
from home import models
from events.models import event

# Create your views here.
def login_api(request):    
    if request.method=="GET":
        return HttpResponse("Testing")
    req_body = request.body.decode('utf-8')
    req = json.loads(req_body)
    username = req["id"]
    password = req["passwd"]
    user = authenticate(request, username=username, password=password)

    if user is not None:
        # Authentication successful
        login(request, user) 
        groups = user.groups.all()         
        response =  JsonResponse({'message': 'SUCCESS','group': f'{groups[0]}'}, status=200)
        return response   
    else:
        # Authentication failed
        return JsonResponse({'message': 'FAILURE'}, status=401)
    
def auth(req_body):
    try:
        req = json.loads(req_body)
        cookie = req["cookies"]
        session_key = cookie.split("=")[1]
        print(session_key)
    except:
        return {'message': 'FAILURE'},401
        
    User = get_user_model()
    try:
        session = Session.objects.get(session_key=session_key)
        user_id = session.get_decoded().get('_auth_user_id')
        if user_id:
            user = User.objects.get(pk=user_id)
            print("user:",user)
            if user.is_authenticated:
                groups = user.groups.all()   
                return {'message': 'SUCCESS','group': f'{groups[0]}','id':f"{user}"},200
        return {'message': 'FAILURE'},401
    except Session.DoesNotExist:
        return {'message': 'FAILURE'},401


def auth_api(request):
    req_body = request.body.decode('utf-8')
    message,status = auth(req_body=req_body)
    return JsonResponse(message,status=status)
    
    
def logout_api(request):
    req_body = request.body.decode('utf-8')
    try:
        req = json.loads(req_body)
        cookie = req["cookies"]
        session_key = cookie.split("=")[1]
    except:
        return JsonResponse({'message': 'FAILURE'}, status=401)
    
    User = get_user_model()
    try:
        session = Session.objects.get(session_key=session_key)
        session_data = session.get_decoded()
        user_id = session_data.get('_auth_user_id')
        
        if user_id:
            user = User.objects.get(pk=user_id)
            if user.is_authenticated:
                # Clear the session data to mark the user as unauthenticated
                session_data['_auth_user_id'] = None
                session_data['_auth_user_backend'] = ''
                session_data['_auth_user_hash'] = ''
                session.session_data = session_data
                session.save()
                return JsonResponse({'message': 'SUCCESS'}, status=200)
            else:
                return JsonResponse({'message': 'FAILURE'}, status=401)
    except Session.DoesNotExist:
        return JsonResponse({'message': 'FAILURE'}, status=401)


def proxy_handler(request,*args):
    if request.method == 'GET':
        # Specify the target server and path
        remaining_path = request.path.replace('/proxy', '')

        # Specify the target server and path
        target_host = request.get_host()
        target_path = remaining_path
        
        connection = http.client.HTTPSConnection(target_host)
        # Send a GET request to the target server
        connection.request('GET', target_path)

        # Get the response from the target server
        response = connection.getresponse()
        response_body = response.read().decode('utf-8')
        response_data = json.loads(response_body)
        message = json.dumps(response_data)
        # Close the connection to the target server
        connection.close()
        return HttpResponse(message, content_type='application/json')

    elif request.method == 'POST':
        # Specify the target server and path
        remaining_path = request.path.replace('/proxy', '')

        # Specify the target server and path
        target_host = request.get_host()
        target_path = remaining_path

        # Extract the POST data from the request
        content_length = int(request.META['CONTENT_LENGTH'])
        post_data = request.body.decode('utf-8')

        # Create a connection to the target server
        connection = http.client.HTTPSConnection(target_host)

        # Set the headers for the POST request
        headers = {
            'Content-Type': 'application/json',
            'Content-Length': content_length
        }

        # Send a POST request to the target server
        connection.request('POST', target_path, body=post_data, headers=headers)

        # Get the response from the target server
        response = connection.getresponse()
        response_body = response.read().decode('utf-8')
        response_data = json.loads(response_body)
        
        # Close the connection to the target server
        connection.close()
        
        # Extract the cookie from the response
        if response.status == 200:
            try:
                cookie = response.headers['Set-Cookie'].split(";")[0]
                cookie = cookie.split("=")
                key = cookie[0]
                value = cookie[1]
                response_data[key] = value
                return JsonResponse(response_data,status=200)
            except:
                print("No Cookie Infotmation")
                pass
        return JsonResponse(response_data,status=401)

def studentsList(request):
    req_body = request.body.decode('utf-8')
    message,status = auth(req_body=req_body)
    req = json.loads(req_body)
    print(message,req)
    if status==200:
        try:
            students_list = list()
            students = models.student.objects.all()
            for Iter in students:
                students_list.append({
                    "srn":Iter.srn,
                    "name":Iter.name,
                    "departmentId":Iter.department.id,
                    "departmentName":Iter.department.name,
                    "sem":Iter.sem,
                })
            message["students"] = students_list
        except Exception as e:
                print("ERROR:",e)
                message['message'] = "FAILURE"
                status = 404
    else:
        message['message'] = "FAILURE"
        status = 401
    return JsonResponse(message,status=status)

def studentProfile(request):
    req_body = request.body.decode('utf-8')
    message,status = auth(req_body=req_body)
    req = json.loads(req_body)
    print(message,req)
    if status==200:
        try:
            eventList = list()
            student = models.student.objects.get(srn=req["srn"])
            message["srn"] = student.srn 
            message["name"] = student.name 
            message["departmentName"] = student.department.name
            message["departmentId"] = student.department.id 
            message["sem"] = student.sem
            message["cgpa"] = None 
            message["events"] = None
            if message["group"] == "faculties":
                events = event.objects.filter(participants__srn__srn=req["srn"])
                for Iter in  events:
                    eventList.append({
                        "id" : Iter.id,
                        "name":Iter.name,
                        "date":Iter.date,
                        "details":Iter.details
                    })
                message["cgpa"] = student.cgpa
                message["events"] = eventList
            if student.srn == message["id"]:
                message["cgpa"] = student.cgpa
                
                # Getting declaration forms list and status
                target_host = request.get_host()
                target_path = "/attendance/declaration/get/"
                
                # Create a connection to the target server
                connection = http.client.HTTPSConnection(target_host)
                
                post_data = {
                    "cookies":req["cookies"]
                }
                # Encode the post_data as JSON
                post_data_json = json.dumps(post_data).encode('utf-8')

                # Calculate the length of the encoded data
                content_length = len(post_data_json)

                # Set the headers for the POST request
                headers = {
                    'Content-Type': 'application/json',
                    'Content-Length': content_length,
                }

                
                # Send a POST request to the target server
                connection.request('POST', target_path, body=post_data_json, headers=headers)

                # Get the response from the target server
                response = connection.getresponse()
                response_body = response.read().decode('utf-8')
                response_data = json.loads(response_body)   
                
                message["declaration"] = response_data["declaration"]
   
        except Exception as e:
                print("ERROR:",e)
                message['message'] = "FAILURE"
                status = 404
    else:
        message['message'] = "FAILURE"
        status = 401
    return JsonResponse(message,status=status)

def facultyProfile(request):
    req_body = request.body.decode('utf-8')
    message,status = auth(req_body=req_body)
    req = json.loads(req_body)
    print(message,req)
    if status==200:
        try:
            faculty = models.faculty.objects.get(id=req["id"])
            message["id"] = faculty.id
            message["name"] = faculty.name
        except Exception as e:
                print("ERROR:",e)
                message['message'] = "FAILURE"
                status = 404
    else:
        message['message'] = "FAILURE"
        status = 401
    return JsonResponse(message,status=status)
            