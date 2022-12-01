from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.forms.widgets import NumberInput
# import datetime
from .import models

class AccountsForm(forms.ModelForm):
    
    class Meta:
        model = models.Accounts
        fields = '__all__'


class SubAccountsForm(forms.ModelForm):

    class Meta:
        model = models.Sub_Accounts
        fields = ('sub_code','sub_description',)


class PvForm(forms.ModelForm):
    
    transaction_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}),label='Value Date')
    sub_account = forms.ModelChoiceField(
         queryset=models.Sub_Accounts.objects.filter(code__tag='Expense').order_by('sub_description'))
       

    class Meta:
        model = models.Payment_Vouchers
        fields = ('transaction_date','sub_account','description','type',)

class Pv_detailsForm(forms.ModelForm):
    description = forms.CharField(label=False)
    quantity = forms.IntegerField(label=False)
    unit_price=forms.DecimalField(decimal_places=2,label=False)
    class Meta:
        model = models.Pv_details
        fields = ('description','quantity','unit_price',)

class paymentform(forms.Form):
    amount_paid = forms.DecimalField(decimal_places=2,label=False)
    # sub_code = forms.ModelChoiceField(queryset=models.Sub_Accounts.objects.filter(code__tag='Cash-Eq').order_by('sub_description'),label=False)

class paymentforms(forms.Form):
    amount_paid = forms.DecimalField(decimal_places=2,label=False)
    sub_code = forms.ModelChoiceField(queryset=models.Sub_Accounts.objects.filter(code__tag='Cash-Eq').order_by('sub_description'),label=False)


class OfferingForm(forms.ModelForm):

    transaction_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}),label='Value Date')
    sub_code = forms.ModelChoiceField(
         queryset=models.Sub_Accounts.objects.filter(code__tag='Offerings').order_by('sub_description'))
       
    class Meta:
        model = models.Offerings
        fields = ('transaction_date','sub_code','description','amount',)



class PledgeForm(forms.ModelForm):
    
    transaction_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}),label='Value Date')
    sub_code = forms.ModelChoiceField(
         queryset=models.Sub_Accounts.objects.filter(code__tag='Pledges').order_by('sub_description'))
     
       
    class Meta:
        model = models.Pledges
        fields = ('transaction_date','sub_code','description')


class PledgeDetailForm(forms.ModelForm):
    
    amount = forms.DecimalField(label=False)

    def clean(self, *args, **kwargs):
        amount = self.cleaned_data.get('amount')
      
        if amount <= 0:
            raise forms.ValidationError(
                {'amount': ["Amount cannot be less than GHC 1.00"]})
            
        return super(PledgeDetailForm, self).clean(*args, **kwargs)

    class Meta:
        model = models.Pledges_Details
        fields = ('amount',)

class WelfarelForm(forms.ModelForm):
    
    
    transaction_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}),label=False)
    sub_code = forms.ModelChoiceField(
         queryset=models.Sub_Accounts.objects.filter(code__tag='Welfare').order_by('sub_description'),label=False)
    amount = forms.DecimalField(label=False)
     
       
    def clean(self, *args, **kwargs):
        amount = self.cleaned_data.get('amount')
      
        if amount <= 0:
            raise forms.ValidationError(
                {'amount': ["Amount cannot be less than GHC 1.00"]})
            
        return super(WelfarelForm, self).clean(*args, **kwargs)

    class Meta:
        model = models.Walfares
        fields = ('amount', 'sub_code','transaction_date',)

class transferform(forms.ModelForm):
    transaction_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}),label='Value Date')
    fromaccount_code = forms.ModelChoiceField(
         queryset=models.Sub_Accounts.objects.filter(code__tag='Cash-Eq').order_by('sub_description'), label='From')
    toaccount_code = forms.ModelChoiceField(
         queryset=models.Sub_Accounts.objects.filter(code__tag='Cash-Eq').order_by('sub_description'), label='To')
    tran_dec = forms.CharField(label='Transfer Description')

    class Meta:
        model = models.Transfers
        fields = ('transaction_date','fromaccount_code','tran_dec','toaccount_code','amount','type',)



class TitheForm(forms.ModelForm):
    
    transaction_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}),label=False)
    sub_code = forms.ModelChoiceField(
         queryset=models.Sub_Accounts.objects.filter(code__tag='Tithe').order_by('sub_description'),label=False)
    amount = forms.DecimalField(label=False)
     
       
    def clean(self, *args, **kwargs):
        amount = self.cleaned_data.get('amount')
      
        if amount <= 0:
            raise forms.ValidationError(
                {'amount': ["Amount cannot be less than GHC 1.00"]})
            
        return super(TitheForm, self).clean(*args, **kwargs)

    class Meta:
        model = models.Tithe
        fields = ('amount', 'sub_code','transaction_date',)



class AccForm(forms.ModelForm):
    
    open_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}),label=False)
    description = forms.CharField(label=False)
     
    class Meta:
        model = models.Accumulated_fund
        fields = ('description', 'open_date',)


class AccCloseForm(forms.ModelForm):
    
    closing_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}),label=False)
    
    class Meta:
        model = models.Accumulated_fund
        fields = ( 'closing_date',)