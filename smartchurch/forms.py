from django import forms
from django.forms import Form
from django.forms.widgets import NumberInput
from django.contrib.auth import authenticate
import datetime
from .import models


class DateInput(forms.DateInput):
    input_type = "date"


class UserLoginForm(forms.Form):
    username = forms.CharField(label=False, widget=forms.TextInput(
        attrs={'placeholder': 'Username'}))
    password = forms.CharField(label=False, widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Username or Password incorrect')
            if not user.check_password(password):
                raise forms.ValidationError('Username or Password incorrect')
            if not user.is_active:
                raise forms.ValidationError('Username or Password incorrect')
        return super(UserLoginForm, self).clean(*args, **kwargs)

    class Meta():
        model = models.User
        fields = ('username', 'password')

class PersonForm(forms.ModelForm):
    dob = forms.DateField(widget=NumberInput(attrs={'type': 'date'}), label='Date of Birth') 
    class Meta:
        model = models.People
        fields = ('surname','first_name','other_name','tile','email','contact','gender','marital_status','dob','address','status','profile_picture',)

class ChildrenForm(forms.ModelForm):
    dob = forms.DateField(widget=NumberInput(attrs={'type': 'date'}), label='Date of Birth')
    class Meta:
        model = models.Peoples_Children
        fields =('name','dob',)


class BaptismForm(forms.ModelForm):
    date_of_baptism = forms.DateField(widget=NumberInput(attrs={'type': 'date' }), label='Date of Baptism')
    class Meta:
        model = models.Baptism
        fields=('where','date_of_baptism',)

class EmmergencyForm(forms.ModelForm):
    class Meta:
        model = models.Emmergency_Contact
        fields=('name','contact','relationship','if_others_specify',)