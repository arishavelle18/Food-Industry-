import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image,ImageDraw
from django.db import models
import uuid
from django_cryptography.fields import encrypt
# Create your models here.

class Attendance(models.Model):
    TIME_IN = 'time in'
    TIME_OUT = 'time out'
    BREAKTIME_OUT = "breaktime out"
    BREAKTIME_IN = "breaktime in"
    TIMECHOICES =(
        (TIME_IN,'Time In'),
        (TIME_OUT,'Time Out'),
        (BREAKTIME_OUT,'Breaktime Out'),
        (BREAKTIME_IN,'Breaktime In'),   
    )

    owner = models.ForeignKey('Profiles',on_delete=models.SET_NULL,null=True)
    personCode = models.CharField(max_length = 200)
    status = models.CharField(max_length=255,choices=TIMECHOICES)
    created = models.DateTimeField()
    inspect = models.ManyToManyField("Equipment",related_name="inspection" ,blank=True)
    
    def __str__(self):
        return f"{self.personCode} created at {self.created} and {self.status}"
    # change the order into decreasing order
    class Meta:
        ordering = ['-created']


class HistoryAttendance(models.Model):
    personCode = models.CharField(max_length = 200)
    created = models.DateTimeField()

    def __str__(self):
        return f"{self.personCode} created at {self.created}"



class Equipment(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Profiles(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,unique=True)
    name = models.CharField(max_length = 1000)
    email = models.CharField(max_length = 1000)
    bio = models.CharField(max_length = 1000)
    # inspect = models.ManyToManyField(Equipment,related_name="inspection" ,blank=True)
    qr_code = models.ImageField(upload_to='qr_codes',blank= True)
    created_at = models.DateTimeField()
    def __str__(self):
        return f"{self.name},{self.email},{self.bio}"
    
    class Meta(object):
        unique_together = ('email',)

    def save(self,*args,**kwargs):
        qrcode_img = qrcode.make(self.name)
        # construct
        canvas = Image.new("RGB",(400,400),"white")
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.name}'+".png"
        # create memory
        buffer =BytesIO()
        canvas.save(buffer,'PNG')
        # create a file object
        self.qr_code.save(fname,File(buffer),save=False)
        canvas.close()
        super().save(*args,**kwargs)
        
    

class MyModel(models.Model):
   owner = models.ForeignKey(Profiles,on_delete=models.SET_NULL,null=True)
   name = models.CharField(max_length=100)
   my_json_field = models.JSONField(default=dict)
   created_at = models.DateTimeField()
   inspect = models.ManyToManyField(Equipment,related_name="modelinspect" ,blank=True)
   def __str__(self):
       return f"{self.name} {self.created_at}"