from django.db import models
from simple_history.models import HistoricalRecords
from crum import get_current_user
from django_resized import ResizedImageField
from django.conf import settings
from django.contrib.sessions.models import Session
from .utils import incrementor
from django.core.validators import RegexValidator
import datetime

# Create your models here.

User = settings.AUTH_USER_MODEL

class UserSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    session = models.OneToOneField(Session, on_delete=models.CASCADE)
    
    history = HistoricalRecords()

class Region(models.Model):
    region_name = models.CharField(max_length=100)
    
    history = HistoricalRecords()

    def __str__(self):
        return self.region_name


class District(models.Model):
    districtname = models.CharField(max_length=100)
    region = models.ForeignKey(
        Region, blank=True, null=True, on_delete=models.CASCADE)
    
    history = HistoricalRecords()

    

    def __str__(self):
        return self.districtname


class Church(models.Model):
    church_name = models.CharField(max_length=100)
    district = models.ForeignKey(
        District, blank=True, null=True, on_delete=models.CASCADE)
    
    history = HistoricalRecords()

    

    def __str__(self):
        return self.church_name


class Profile(models.Model):
    
    user = models.OneToOneField(
        User, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    church = models.ForeignKey(
        Church, blank=True, null=True, on_delete=models.CASCADE)
    is_new = models.BooleanField(default=False)
    history = HistoricalRecords()
   
    def __str__(self):
        return self.name

    def save(self,*args, **kwargs):
        
        super(Profile, self).save(*args, **kwargs)


class People(models.Model):
    phone_message = 'Phone number must begin with 0 and contain only 10 digits' 
    sex = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    st = (
        ('New', 'New'),
        ('Foundation Class', 'Foundation Class'),
        ('Member', 'Member'),
        ('Inactive', 'Inactive'),
        ('Deceased', 'Deceased'),
    )
    tit = (
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
        ('Miss', 'Miss'),
    )
    mstatus = (
        ('Married', 'Married'),
        ('Single', 'Single'),
        ('Divorce', 'Divorce'),
        ('Widowed', 'Widowed'),
        ('Separated','Separated'),
    )


     # your desired format 
    phone_regex = RegexValidator(
        regex=r'^(0)\d{9}$',
        message=phone_message
    )
    profile = models.OneToOneField(
       Profile, blank=True, null=True, on_delete=models.CASCADE)
    surname = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    other_name = models.CharField(max_length=200,null=True, blank=True)
    name = models.CharField(max_length=270,null=True, blank=True)
    tile = models.CharField(max_length=10, choices=tit, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    contact = models.CharField(validators=[phone_regex],null=True, blank=True,max_length=20)
    gender = models.CharField(max_length=10, choices=sex, null=True, blank=True)
    marital_status = models.CharField(max_length=30, choices=mstatus, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    age = models.IntegerField(default=0)
    address = models.CharField(max_length=200)
    status = models.CharField(max_length=30, choices=st,default='New' ,null=True, blank=True)
    profile_picture = ResizedImageField(default="avatar.jpg",size=[128, 128],blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.id)

    
    # def get_age(self):
    #     age = 
    #     return int((age).days/365.25)

    def save(self, *args, **kwargs):
        if not self.id:
            number = incrementor()
            self.id = str(number())
            while People.objects.filter(id=self.id).exists():
                self.id = str(number())
        self.name = str(self.id)+ "----"+ self.first_name + "----" +self.surname
        self.age = int((datetime.date.today()-self.dob).days/365.25)
        super(People, self).save(*args, **kwargs)


class Church_Members(models.Model):
    church = models.ForeignKey(
        Church, blank=True, null=True, on_delete=models.CASCADE)
    member = models.ForeignKey(
        People, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.member.id)

class Peoples_Children(models.Model):
    parent = models.ForeignKey(
        People, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    history = HistoricalRecords()

class Baptism(models.Model):
    bstatus = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    
    church = models.ForeignKey(
        Church, blank=True, null=True, on_delete=models.CASCADE)
    member = models.ForeignKey(
        People, blank=True, null=True, on_delete=models.CASCADE)
    date_of_baptism = models.DateField(null=True, blank=True)
    where = models.CharField(max_length=255,null=True, blank=True)
    history = HistoricalRecords()

class Emmergency_Contact(models.Model):
    phone_message = 'Phone number must begin with 0 and contain only 10 digits' 
     # your desired format 
    phone_regex = RegexValidator(
        regex=r'^(0)\d{9}$',
        message=phone_message
    )
    rel = (
        ('Father', 'Father'),
        ('Mother', 'Mother'),
        ('Sibling', 'Sibling'),
        ('Friend', 'Friend'),
        ('Spouse', 'Spouse'),
        ('Child', 'Child'),
        ('Others', 'Others'),
    )
    member = models.ForeignKey(
        People, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255,null=True, blank=True)
    contact = models.CharField(validators=[phone_regex],null=True, blank=True,max_length=20)
    relationship = models.CharField(max_length=30, choices=rel, null=True, blank=True)
    if_others_specify = models.CharField(max_length=255,null=True, blank=True)


