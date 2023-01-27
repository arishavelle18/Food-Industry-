from django.shortcuts import redirect, render,HttpResponse
# from django.contrib.auth.models import User
from .models import User
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail,EmailMessage,EmailMultiAlternatives
from django.core import mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from email.mime.image import MIMEImage
from datetime import datetime
from django.conf import settings
import uuid
# Create your views here.
import numpy as np
import cv2 as cv
from django.utils import timezone
from django.http import JsonResponse
import re
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.oath import totp
from functools import wraps
from django.http import HttpResponseRedirect
from django.urls import reverse



# make a custom restriction if the user does not use 2fa the n he/she cannot access the admin panel

def admin_only(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_anonymous:
            return render(request,"adminportal/home.html")
        user = User.objects.filter(email = request.user.email)[0]
        # kapag yung user is annonymous
        if user.adminAccess and not request.user.is_anonymous:
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/admin')
    return wrap




def loginPage(request):
    if  request.user.is_authenticated:
        user = User.objects.filter(email = request.user.email)
        if user:
            if user[0].adminAccess:
                return redirect("home")
            else:
                return redirect("authenticator")        
        
    return render(request,"adminportal/login.html")

def loginVerify(request):
    #  request.POST.get("email") if not request.POST.get("email") == "" else 
    email = request.POST.get("email")
    # 
    password = request.POST.get("pass")
    
    try:
        user = User.objects.get(email = email)
    except:
        return JsonResponse({"res":False,"message":"User does not exist"})
        # check if the data is in the database 
    if user.check_password(password):
        login(request,user)
        return JsonResponse({"res":True,"message":"Login Successfully"})
    else:
        return JsonResponse({"res":False,"message":"Email or Password does not exist"})


# homepage and check if the user have a sessionid if not then, you cannot go to home unless you logged in
# @login_required(login_url='login-page')
@admin_only
def home(request):
    return render(request,"adminportal/home.html")

#logout and check if the user have a sessionid if not then, you cannot go to home unless you logged in 
@login_required(login_url='login-page')
def logoutPage(request):
    user =  User.objects.filter(email= request.user.email)
    user.update(adminAccess=False)
    logout(request)
    # if "uid" in request.session.keys():
    #     del request.session["qr"]
    
    return redirect("login-page")



# recover the admin acc
def recoverLog(request):
    content = {}
    return render(request,"adminportal/recovery.html",content)

def recoverValidation(request):
    # get the email in the ajax 
    email = request.POST["email"]

    # check if the user is existed or not
    res = User.objects.filter(email=email)
    if res:
        return JsonResponse({"res":list(res.values())})
    else:
        return JsonResponse({"res":None})

# for sending otp in the email that is being provided by the admin 

def sendOtp(request,name):
    user = User.objects.filter(email=name)
    #  check if it existed
    if not user:
        return HttpResponse("Unauthorized Access<br><hr>")

    # generate the uuid for the code recovery  
    myuuid  = uuid.uuid4()
    # process the sending mail to the email that is want to be recover
    subject = 'Recovering Email Account'
    content = {"myuuid": myuuid, "user": user[0].email}
    html_message = render_to_string("adminportal/sendmail.html",content)
    plain_message = strip_tags(html_message)
    from_email = 'From inspectiontool18@gmail.com'
    to = user[0].email
    mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

    # manipulate the data in the model and update the code and the datetime of the code that is created
    user[0].code = myuuid
    user[0].codeCreated = datetime.now()
    user[0].save()

    return render(request,"adminportal/codeverify.html")

def updatePass(request,name):
    user = User.objects.filter(email=name)
    if user:
        content = {"name":name}
        return render(request,'adminportal/otp.html',content)
    else:
        return HttpResponse("Unauthorized Access<br><hr>")

def validatePassOtp(request):
    newPas = request.POST["newPas"]
    conPas = request.POST["conPas"]
    emailHide = request.POST["emailHide"]
    user = User.objects.filter(email=emailHide)
    if user:
        if not newPas == user[0].password:
            # if same the check if the pass of the user is the same to the old
            if re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', newPas) and not user[0].check_password(newPas):
                # to update the password you need to set it and bad to hash
                user[0].set_password(newPas)
                user[0].save()
                user.update(auth=False)
                return JsonResponse({"res":True,"message":f"Password has been Succefully Changed {newPas}"})
            else:
                return JsonResponse({"res":False,"message":"Invalid Password,Atleast 8 characters has Uppercase, Lowercase, Symbol and Number."})
        else:
            return JsonResponse({"res":False,"message":"New Password and Old Password is the same"})
    else :
        # if the user is not exist
        return JsonResponse({"res":False,"message":"Invalid Password"})


# check the code 
def codeChecker(request):
    code = request.POST["code"]
    # check if the code is a uuid4 or not
    try:
            uuid.UUID(code,version=4)
    except:
            return JsonResponse({"res":False})
    user = User.objects.filter(code=code)
    # check the user if the code is being get or not
    if user:
        # compare the code in the database and inputted code 
        if str(user[0].code) == str(code):
            return JsonResponse({"res":True,"acc":user[0].email})
        else:
            return JsonResponse({"res":False})
    else:
        return JsonResponse({"res":False})


# if you miss the route this will appear
def error_404(request,exception):
    return render(request,'error.html')

@login_required(login_url='login-page')
def authenticator(request):
    # check if this is not annonymous 
    if not request.user.is_anonymous:
        user = User.objects.filter(email=request.user.email)
        # content = {"user":request.user}
        # check if the fucking user is in TOTP device
        if TOTPDevice.objects.filter(name=user[0].email):
            # if the fucking user is already in TOTPDevice then you need to use authenticator
            if not user[0].auth: 
                userId=TOTPDevice.objects.get(name=user[0].email)
                qr_code_url = reverse('admin:%s_%s_qrcode' % (TOTPDevice._meta.app_label, TOTPDevice._meta.model_name), args=[userId.pk]) 
                content = {"user":user[0],"qr_code_url":qr_code_url}
            else:
                content = {"user":user[0]}
        else:
            TOTPDevice.objects.create(
                user = user[0],
                name = user[0].email
            )
            user.update(auth=True)
            user.update(adminAccess=True)
            userId=TOTPDevice.objects.get(name=user[0].email)
            qr_code_url = reverse('admin:%s_%s_qrcode' % (TOTPDevice._meta.app_label, TOTPDevice._meta.model_name), args=[userId.pk])
            content = {"user":request.user,"qr_code_url":qr_code_url}
    else:
        content= {"user":"wala"}
    return render(request,"adminportal/authenticator.html",content)

@login_required(login_url='login-page')
def tokenValidator(request):
    try:
        email = request.POST.get("email")
        password = int(request.POST.get("pass"))
    except:
        return JsonResponse({"res": "mali"})
    

    # check if the user is in TOTP device
    user = TOTPDevice.objects.filter(name=email)
    # activate the access capability of the admin 
    person = User.objects.filter(email = email)
    if user:
       
        # convert the key into number that correlate to google authentication
        token = totp(user[0].bin_key)
        if token == password:
            person.update(auth=True)
            person.update(adminAccess=True)
            return JsonResponse({"res": True,"messages":"Successfully Login!"})
            
        else: 
            return JsonResponse({"res": False,"messages":"Token is incorrect!"})
    else:
        return JsonResponse({"res": False,"messages":"User not found!"})


@login_required(login_url='login-page')
# cancel the token authenticator 
def cancelAuth(request):
    user =  User.objects.filter(email= request.user.email)
    user.update(adminAccess=False)
    logout(request)
    return HttpResponseRedirect("/admin")
