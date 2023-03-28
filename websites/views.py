
from django.shortcuts import redirect, render
from .models import Profiles,Attendance,HistoryAttendance,MyModel
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.db.models import Q
from django.core.mail import send_mail,EmailMessage,EmailMultiAlternatives
from django.template.loader import render_to_string
from email.mime.image import MIMEImage
from django.conf import settings
from django.templatetags.static import static
from  .forms import UserForm
import cv2 as cv    
import os 
import re
from datetime import datetime
import datetime as dt
from functools import wraps
import csv
import uuid
from adminportal.models import User
from django.http import HttpResponseRedirect
import json

# qr code 
# @login_required(login_url="login-page")
def qrCode(request):
    return render(request,"websites/qrcode.html")


def admin_only(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        user = User.objects.filter(email = request.user.email)[0]
        # kapag yung user is annonymous
        if request.user.is_anonymous:
            return HttpResponseRedirect('/')
        elif user.adminAccess and not request.user.is_anonymous:
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/admin')
    return wrap


# validate the qr for attendance
# @login_required(login_url="login-page")
def qrValidation(request):
    # check if it has session of qr if yes delete and change the session
    pk = request.session.get("qr") if request.session.get("qr") else ""

    # check the current date
    today = datetime.now()
    year,month,day = [today.year,today.month,today.day]
    
    if pk:
        user = Attendance.objects.filter(
            personCode = pk,
            status = 'time in',
            created__year = year,
            created__month = month,
            created__day = day
        )
            # if user:
            #     equipment = user[0].inspect.all()
            
            #     # check if the equipment is complete or not 
            #     if len(equipment)==0:

            #         # delete all the session and attendance that is no equipment
            #         # attend = Attendance.objects.get(personCode=pk)
            #         # attend.delete()
            #         user.delete()
        del request.session['qr']

    text = request.GET.get("decodedText") if request.GET.get("decodedText") is not None else ""
    # checker if you are already in the attendance or not
    check = Attendance.objects.filter(personCode=text,status="time in")
    # check the person if it is register or not 
    person = Profiles.objects.filter(name=text)
    attend = Attendance.objects.filter(
        personCode = text,
        status = 'time in',
        created__year = year,
        created__month = month,
        created__day = day
    )
    # if the the person is in the system and not being timestamp the time he arrive
    if person and not attend:
        Attendance.objects.create(
            owner = person[0],
            personCode = text,
            status = 'time in',
            created = today
        )
        request.session["qr"] = text
        return JsonResponse({"ret":True,"text":text})
    else:
        return JsonResponse({"ret":False})
    

# add menu
# @login_required(login_url="login-page")
def menu(request):
    return render(request,"websites/menu.html")

# add employee
@login_required(login_url="login-page")
@admin_only  # check if the user is already otp or not
def addEmployee(request):
    form = UserForm()
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        
        # check if the email is unique
        if not Profiles.objects.filter(email=email):
            Profiles.objects.create(
                name = name,
                email = email,
                created_at = datetime.now()
            )
            user = Profiles.objects.get(name = name)
            # return HttpResponse(f"<img src='{user.qr_code.url}' ></img>")
            # this one has an error 
            subject = 'Django sending email'
            body_html = '''
            <html>
                <body>
                    <h3>This is qr code </h3>
                    <img src="{{user.qr_code.url}}" />
                </body>
            </html>
            '''

            from_email = 'inspectiontool18@gmail.com'
            to_email = user.email

            msg = EmailMultiAlternatives(
                subject,
                body_html,
                from_email=from_email,
                to=[to_email]
            )

            msg.mixed_subtype = 'related'
            msg.attach_alternative(body_html, "text/html")
            img_dir = 'static/media'
            image = user.qr_code.name
            file_path = os.path.join(img_dir, image)
            with open(file_path, 'rb') as f:
                img = MIMEImage(f.read())
                img.add_header('Content-ID', '<{name}>'.format(name=image))
                img.add_header('Content-Disposition', 'inline', filename=image)
            msg.attach(img)
            msg.send()
            return redirect("home")
    context = {"form":form}
    return render(request,"websites/addEmployee.html",context   )

# @login_required(login_url="login-page")
def test(request):
    return render(request,"websites/scannerInspect.html")
    return render(request,"websites/gotest.html")
    
# @login_required(login_url="login-page")
def test2(request):
    pk = request.session.get("qr")
    pk = re.sub("\s","-",pk)
    os.system(f'python detect.py --source 0 --qr {pk}')
    return JsonResponse({"mask":True})
    # return HttpResponse(request.session.get("qr"))
    

@login_required(login_url="login-page")
# use to download all attendance
@admin_only  # check if the user is already otp or not
def getAttendance(request):
    
    id = request.POST.get('id')
    
    # chec the validity of uuid in the id
    if not id == "All":
        try:
            uuid.UUID(id,version=4)
        except:
            return JsonResponse({})
        
    minDate = request.POST['minDate']
    minYear = request.POST['minYear']
    minMonth = request.POST['minMonth']
    minDay = request.POST['minDay']
    min = dt.date(int(minYear),int(minMonth),int(minDay))
    maxDate = request.POST["maxDate"]
    maxYear = request.POST["maxYear"]
    maxMonth = request.POST["maxMonth"]
    maxDay = request.POST["maxDay"]
    max = dt.date(int(maxYear),int(maxMonth),int(maxDay))
    if not id == 'All':
        test = MyModel.objects.filter(owner=id,created_at__date__range=(min,max))
        if test:
            return JsonResponse({"id":id,"minDate":minDate,"maxDate":maxDate,"test":list(test.values())})
        else:
            return JsonResponse({})
    else:
        test = MyModel.objects.filter(created_at__date__range=(min,max))
        if test:
            return JsonResponse({"id":id,"minDate":minDate,"maxDate":maxDate,"test":list(test.values())})
        else:
            return JsonResponse({})

# @login_required(login_url="login-page")
# check if he has equipment 
def getUpdate(request):
    # wala pang checker kung  may session o wala
    pk = request.session.get("qr") if request.session.get("qr") is not None else ""
    
    if pk and Attendance.objects.filter(personCode=pk) : 
        profiles = Attendance.objects.get(personCode=pk,created__year = datetime.now().year,created__month = datetime.now().month,created__day = datetime.now().day)
        inspect =profiles.inspect.all()
        context = {"inspect":list(inspect.values())}     
        return JsonResponse(context)
    else:
        context ={"inspect": "" ,"pk":pk}
        return render(request,"websites/test.html",context)

@login_required(login_url="login-page")
# display view attendance
@admin_only  # check if the user is already otp or not
def viewAttendance(request):
    old = Attendance.objects.last().created
    latest = Attendance.objects.first().created
    q = request.GET.get('q')  if request.GET.get('q') != None else ""
    #  delete all the data that has no equipment 
        # delete_attend = Attendance.objects.all().filter(Q(status="time in")).exclude(~Q(inspect__name =None))
        # if delete_attend:
        #     delete_attend.delete()

    # get all the attendance but you can see if the person have a complete equipments in inpection part
    if q :
        attend = MyModel.objects.all().filter(Q(name__icontains=q) | Q(owner__id__icontains=q)).exclude(Q(inspect__name=None))
    else:
        attend = Attendance.objects.all()
        attend = MyModel.objects.all()
        # attend_data = [{'name': user.name,"owner_id":user.owner_id,"created_at":user.created_at,"my_json_field":user.my_json_field, 'inspect': list(user.inspect.values_list('id', 'name'))} for user in attend]
        


        # person = attend.value_list("inspection")
        # return HttpResponse(attend.owner)
        # .exclude(Q(inspect__name=None) & Q(status="time in"))
    logs = HistoryAttendance.objects.all()
    context = {"attend":attend,"logs":logs,"old":f"{old.year}-{old.month}-{old.day}","latest":f"{latest.year}-{latest.month}-{latest.day}"}

    return render(request,"websites/viewAttendance.html",context)

# eto pa ajax
def updateAttendance(request):
    q = request.GET.get('q')  if request.GET.get('q') != None else ""
    #  delete all the data that has no equipment 
        # delete_attend = Attendance.objects.all().filter(Q(status="time in")).exclude(~Q(inspect__name =None))
        # if delete_attend:
        #     delete_attend.delete()

    # get all the attendance but you can see if the person have a complete equipments in inpection part
    if q :
        attend = MyModel.objects.all().filter(Q(name__icontains=q) | Q(owner__id__icontains=q))
    
    else:
        attend = Attendance.objects.all()
        attend = MyModel.objects.all()
        
    attend_data = [{'name': user.name,"owner_id":user.owner_id,"created_at":user.created_at,"my_json_field":user.my_json_field, 'inspect': list(user.inspect.values_list('id', 'name'))} for user in attend]
        

        # person = attend.value_list("inspection")
        # return HttpResponse(attend.owner)
        # .exclude(Q(inspect__name=None) & Q(status="time in"))
    logs = HistoryAttendance.objects.all()
    # context = {"attend_ins":attend_data,"logs":logs,"old":f"{old.year}-{old.month}-{old.day}","latest":f"{latest.year}-{latest.month}-{latest.day}"}

    return JsonResponse({"hey":attend_data,})
    
def getEquipment(request):
    id = request.GET.get("id") if request.GET.get("id") is not None else ""
    today = datetime.now()
    year,month,day = [today.year,today.month,today.day]
    try:
        person = MyModel.objects.get(
        owner_id = id,
        created_at__year = year,
        created_at__month = month,
        created_at__day = day
        )
    except:
        return JsonResponse({"res":False,})
    equipment = person.inspect.all()
    return JsonResponse({"res":True,"equipment":list(equipment.values())})
    pass

# @login_required(login_url="login-page")
# scan timeout 
def scanTimeout(request):
    return render(request,"websites/scanTimeout.html")

# @login_required(login_url="login-page")
# validate the qr for time out
def timeoutValidation(request):
    # get the qr code
    text = request.GET.get("decodedText") if request.GET.get("decodedText") is not None else ""
    # check if the user is in the system
    person = Profiles.objects.filter(name = text)
    # get the current datetime
    today = datetime.now()
    year,month,day = [today.year,today.month,today.day]
    timeIn = Attendance.objects.filter(
        personCode = text,
        status ="time in",
        created__year = year,
        created__month = month,
        created__day = day
    ) 
    timeOut = Attendance.objects.filter(
        personCode = text,
        status = "time out",
        created__year = year,
        created__month = month,
        created__day = day
    )
    breaktimeOut = Attendance.objects.filter(
        personCode = text,
        status ="breaktime out",
        created__year = year,
        created__month = month,
        created__day = day
    )
    breaktimeIn = Attendance.objects.filter(
        personCode = text,
        status ="breaktime in",
        created__year = year,
        created__month = month,
        created__day = day
    )
    #  check if the person time in within this day and not yet timeout
    if timeIn and not timeOut:
        if breaktimeOut and not breaktimeIn:
            return JsonResponse({"ret":False}) 
        else:
            Attendance.objects.create(
                owner = person[0],
                personCode = text,
                status = "time out",
                created = today
            )
            return JsonResponse({"ret":True}) 
    else:
        return JsonResponse({"ret":False}) 

def timeCheck(request):
    today = datetime.now()
    # return JsonResponse({"date":today.month})
    attend = Attendance.objects.filter(created__year=today.year)
    return JsonResponse({"date":list(attend.values())})
    

def breaktimeOut(request):
    return render(request,"websites/breaktimeOut.html")

def breaktimeOutValidation(request):
    text = request.GET.get("decodedText") if request.GET.get("decodedText") is not None else ""
    #  check if they have time in, no breaktime in and timeout
    today = datetime.now()
    year,month,day = [today.year,today.month,today.day]
    # check if the user is in the system
    person = Profiles.objects.filter(name = text)
    timeIn = Attendance.objects.filter(
        personCode = text,
        status ="time in",
        created__year = year,
        created__month = month,
        created__day = day
    )
    timeOut = Attendance.objects.filter(
        personCode = text,
        status = "time out",
        created__year = year,
        created__month = month,
        created__day = day
    )
    breaktimeIn = Attendance.objects.filter(
        personCode = text,
        status ="breaktime in",
        created__year = year,
        created__month = month,
        created__day = day
    )
    breaktimeOut = Attendance.objects.filter(
        personCode = text,
        status ="breaktime out",
        created__year = year,
        created__month = month,
        created__day = day
    )

    if timeIn and person and not timeOut and not breaktimeIn and not breaktimeOut:
        Attendance.objects.create(
            owner = person[0],
            personCode = text,
            status = "breaktime out",
            created = today
        )
        return JsonResponse({"ret":True}) 
    else:
        return JsonResponse({"ret":False})
     

def breaktimeIn(request):
    #  check if they have time in, no breaktime in and timeout
    return render(request,"websites/breaktimeIn.html")
     
def breaktimeInValidation(request):
    text = request.GET.get("decodedText") if request.GET.get("decodedText") is not None else ""
    # check the datetime today
    today = datetime.now()
    year,month,day = [today.year,today.month,today.day]
    # check if the user is in the system
    person = Profiles.objects.filter(name = text)
    timeIn = Attendance.objects.filter(
        personCode = text,
        status ="time in",
        created__year = year,
        created__month = month,
        created__day = day
    )
    timeOut = Attendance.objects.filter(
        personCode = text,
        status = "time out",
        created__year = year,
        created__month = month,
        created__day = day
    )
    breaktimeIn = Attendance.objects.filter(
        personCode = text,
        status ="breaktime in",
        created__year = year,
        created__month = month,
        created__day = day
    )
    breaktimeOut = Attendance.objects.filter(
        personCode = text,
        status ="breaktime out",
        created__year = year,
        created__month = month,
        created__day = day
    )
    #  check if they have time in, no breaktime out and timeout
    if person and timeIn and breaktimeOut and not timeOut and not breaktimeIn:
        Attendance.objects.create(
            owner = person[0],
            personCode = text,
            status = "breaktime in",
            created = today
        )
        return JsonResponse({"ret":True}) 
    else:
        return JsonResponse({"ret":False})

def scanner(request):
    return render(request,"websites/scanner.html")


def scannerValidation(request):
    pk = request.session.get("qr") if request.session.get("qr") else ""
    # this session check if the user stop proceeding to inpection of equipment
    if pk:
        del request.session['qr']

    text = request.GET.get("decodedText") if request.GET.get("decodedText") is not None else ""
    # check first if that name is in the profile
    check = Profiles.objects.filter(name=text)
    if not check:
        return JsonResponse({"ret":False,"text":"User is not Found"})
    # check if his/her name is not in the database if not then we need to create his/her own json
    today = datetime.now()
    month,day,year =[today.month,today.day,today.year]
    attend = MyModel.objects.filter(
        name = text,
        created_at__month = month,
        created_at__day = day,
        created_at__year = year
    )
    
    
    if check and not attend:
        MyModel.objects.create(
            name = text,
            created_at = today,
            owner = check[0],
        )
        # create session for inspection
        request.session["qr"] = text
        return JsonResponse({"ret":True,"text":"User record successfully","first":True})
    # check if the user want to record his/her attendance again in the same day
    elif check and attend:
        
        # count in 1 base 
        try:
            # if there is no key existed in the format converting to json is not good
            y = json.loads(attend[0].my_json_field)
        except:
            y = attend[0].my_json_field
        count = str(len(y) + 1)
        y[count] = {"time":today}
        val = json.dumps(y,default=str) 
        attend[0].my_json_field = val
        attend[0].save()
        return JsonResponse({"ret":True,"text":attend[0].my_json_field,"first":False})
    else:
        return JsonResponse({"ret":False,"text":"Invalid Process"})

    return JsonResponse({"ret":text})

def scannerInspect(request):
    return render(request,"websites/scannerInspect.html")

def scannerGetUpdate(request):
    # wala pang checker kung  may session o wala
    pk = request.session.get("qr") if request.session.get("qr") is not None else ""
    
    if pk and MyModel.objects.filter(name=pk) : 
        profiles = MyModel.objects.get(name=pk,created_at__year = datetime.now().year,created_at__month = datetime.now().month,created_at__day = datetime.now().day)
        inspect = profiles.inspect.all()
        context = {"inspect":list(inspect.values())}     
        return JsonResponse(context)
    else:
        context ={"inspect": "" ,"pk":pk}
        return render(request,"websites/test.html",context)
