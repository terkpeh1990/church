from django.contrib.auth.models import AbstractUser, User
from django.db import models
from crum import get_current_user
from django.db.models import Count
from django.conf import settings
from django.contrib.sessions.models import Session
from simple_history.models import HistoricalRecords
from smartchurch.utils import incrementor
from smartchurch.models import Church,People
import requests
import sys


User = settings.AUTH_USER_MODEL


class Accounts(models.Model):
    sts= (
        
        ('Expense','Expense'),
        ('Cash-Eq','Cash-Eq'),
        ('Offerings','Offerings'),
        ('Tithe','Tithe'),
        ('Pledges','Pledges'),
        ('Welfare','Welfare'),
     
    )
    st= (
        ('Revenue','Revenue'),
        ('Expense','Expense'),
        ('Others','Others'),
       
     
    )
    code = models.CharField(max_length=300)
    description = models.CharField(max_length=300)
    tag = models.CharField(max_length=10, choices= sts , default='Expense')
    group = models.CharField(max_length=10, choices= st , default='Revenue')
    
    history = HistoricalRecords()

    def __str__(self):
        return  str(self.code)

class Sub_Accounts(models.Model):

    code = models.ForeignKey(Accounts, on_delete= models.CASCADE)
    sub_code = models.CharField(max_length=300)
    sub_description = models.CharField(max_length=300)
    
    history = HistoricalRecords()


    def __str__(self):
        return  str(self.sub_code) + '----' + self.sub_description


class Accumulated_fund(models.Model):
    sts= (
        ('Open','Open'),
        ('Set To Close','Set To Close'),
        ('Closed','Closed'),  
    )
    id = models.CharField(max_length=100, primary_key=True)
    church = models.ForeignKey(Church,on_delete=models.CASCADE,blank=True, null=True)
    description = models.CharField(max_length=300)
    status = models.CharField(max_length=50, choices= sts,blank=True, null=True)
    open_date = models.DateField()
    closing_date = models.DateField(blank=True, null=True)
    open_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    walfare_open_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    credit_open_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    close_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    walfare_close_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    creditunion_close_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    history = HistoricalRecords()

    def __str__(self):
            return self.description


    def save(self, *args, **kwargs):
        if not self.id:
            number = incrementor()
            self.id =  "ACC"+ " "+str(number())
            while Accumulated_fund.objects.filter(id=self.id).exists():
                self.id = "ACC"+ " "+str(number())
        super(Accumulated_fund, self).save(*args, **kwargs)






class General_Ledger(models.Model):
    typ= (
        ('Church','Church'),
        ('Credit Union','Credit Union'),
        ('Welfare','Welfare'),
    )
    account_period = models.ForeignKey(Accumulated_fund, on_delete= models.CASCADE,blank=True, null=True)
    transactionref  = models.CharField(max_length=300, blank=True, null=True)
    transaction_date = models.DateField()
    sub_code = models.ForeignKey(Sub_Accounts, on_delete=models.CASCADE)
    description = models.CharField(max_length=300)
    debit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cedit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    church = models.ForeignKey(Church,on_delete=models.CASCADE,blank=True, null=True)
    type = models.CharField(max_length=25, choices= typ, default='Church')
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('auth.User', related_name='glcreatedby', on_delete=models.SET_NULL, blank=True, null=True,default=None)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, related_name='glmodifiedby', blank=True, null=True,default=None)

    history = HistoricalRecords()

    def __str__(self):
        return self.sub_code.sub_code + " "+ self.description


    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.modified_by = user
        super(General_Ledger, self).save(*args, **kwargs)


class All_Transaction(models.Model):
    typ= (
        ('Church','Church'),
        ('Credit Union','Credit Union'),
        ('Welfare','Welfare'),
       
    )
    account_period = models.ForeignKey(Accumulated_fund, on_delete= models.CASCADE,blank=True, null=True)
    transaction_date = models.DateField()
    sub_code = models.ForeignKey(Sub_Accounts, on_delete=models.CASCADE)
    description = models.CharField(max_length=300)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    church = models.ForeignKey(Church,on_delete=models.CASCADE,blank=True, null=True)
    type = models.CharField(max_length=25, choices= typ, default='Church')
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('auth.User', related_name='ATcreatedby', on_delete=models.SET_NULL, blank=True, null=True,default=None)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, related_name='ATmodifiedby', blank=True, null=True,default=None)

    history = HistoricalRecords()

    def __str__(self):
        return self.sub_code.sub_code + " "+ self.description


    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.modified_by = user
        super(All_Transaction, self).save(*args, **kwargs)

class Payment_Vouchers(models.Model):
    sts= (
        ('pending','pending'),
        ('approved','approved'),
        ('cancelled','cancelled'),
        ('void','void'),
    )
    typ= (
        ('Church','Church'),
        ('Credit Union','Credit Union'),
        ('Welfare','Welfare'),
       
    )
    account_period = models.ForeignKey(Accumulated_fund, on_delete= models.CASCADE,blank=True, null=True)
    id = models.CharField(max_length=100, primary_key=True)
    sub_account = models.ForeignKey(Sub_Accounts, on_delete=models.CASCADE)
    description = models.CharField(max_length=250)
    church = models.ForeignKey(Church,on_delete=models.CASCADE,blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    type = models.CharField(max_length=25, choices= typ, default='Church')
    status = models.CharField(max_length=10, choices= sts)
    created_date = models.DateField(auto_now_add=True)
    transaction_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.description


    def save(self, *args, **kwargs):
        if not self.id:
            number = incrementor()
            self.id =  "PV"+ " "+str(number())
            while Payment_Vouchers.objects.filter(id=self.id).exists():
                self.id = "PV"+ " "+str(number())
        super(Payment_Vouchers, self).save(*args, **kwargs)


class Pv_details(models.Model):
    id = models.AutoField(primary_key=True)
    payment_voucher = models.ForeignKey(Payment_Vouchers, on_delete=models.CASCADE)
    description = models.CharField(max_length=250)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    history = HistoricalRecords()
    def __str__(self):
        return self.payment_voucher.description + ' ---- ' + str(self.amount)

    def save(self, *args, **kwargs):
        self.amount = self.unit_price * self.quantity
        super(Pv_details, self).save( *args, **kwargs)


class Pv_Payment_History(models.Model):
    typ= (
        ('Church','Church'),
        ('Credit Union','Credit Union'),
        ('Welfare','Welfare'),
       
    )

    transaction_date = models.DateField(auto_now_add=True)
    reference = models.ForeignKey(Payment_Vouchers,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    church = models.ForeignKey(Church,on_delete=models.CASCADE,blank=True, null=True)
    type = models.CharField(max_length=25, choices= typ, default='Church')
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('auth.User', related_name='hiscreatedby', on_delete=models.SET_NULL, blank=True, null=True,default=None)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, related_name='hismodifiedby', blank=True, null=True,default=None)

    history = HistoricalRecords()

    def __str__(self):
        return   str(self.amount)


    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.modified_by = user
        super(Pv_Payment_History, self).save(*args, **kwargs)

class Account_Payables(models.Model):
    typ= (
        ('Church','Church'),
        ('Credit Union','Credit Union'),
        ('Welfare','Welfare'),
       
    )
    account_period = models.ForeignKey(Accumulated_fund, on_delete= models.CASCADE,blank=True, null=True)
    transaction_date = models.DateField()
    sub_code = models.ForeignKey(Sub_Accounts, on_delete=models.CASCADE)
    description = models.CharField(max_length=300)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    church = models.ForeignKey(Church,on_delete=models.CASCADE,blank=True, null=True)
    type = models.CharField(max_length=25, choices= typ, default='Church')
    reference = models.ForeignKey(Payment_Vouchers,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('auth.User', related_name='apcreatedby', on_delete=models.SET_NULL, blank=True, null=True,default=None)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, related_name='apmodifiedby', blank=True, null=True,default=None)

    history = HistoricalRecords()

    def __str__(self):
        return self.sub_code.sub_code + " "+ self.description


    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.modified_by = user
        super(Account_Payables, self).save(*args, **kwargs)




class Offerings(models.Model):
    sts= (
        ('pending','pending'),
        ('approved','approved'),
        ('cancelled','cancelled'),
        ('Transact','Transact'),
        ('Reversed','Reversed'),
        ('void','void'),
    )
    account_period = models.ForeignKey(Accumulated_fund, on_delete= models.CASCADE,blank=True, null=True)
    transaction_date = models.DateField()
    id = models.CharField(max_length=100, primary_key=True)
    sub_code = models.ForeignKey(Sub_Accounts, on_delete=models.CASCADE)
    description = models.CharField(max_length=300)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    church = models.ForeignKey(Church,on_delete=models.CASCADE,blank=True, null=True)
    offstatus = models.CharField(max_length=20, choices= sts, default='pending')
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('auth.User', related_name='ocreatedby', on_delete=models.SET_NULL, blank=True, null=True,default=None)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, related_name='omodifiedby', blank=True, null=True,default=None)

    history = HistoricalRecords()

    def __str__(self):
        return self.sub_code.sub_code + " "+ self.description


    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        
        if not self.id:
            number = incrementor()
            self.id = 'OF'+ '' +str(number())
            while Offerings.objects.filter(id=self.id).exists():
                self.id = 'OFF'+ '' + str(number())
            self.created_by = user
        self.modified_by = user
        super(Offerings, self).save(*args, **kwargs)



class Account_Receivables(models.Model):
    typ= (
        ('Church','Church'),
        ('Credit Union','Credit Union'),
        ('Welfare','Welfare'),
       
    )
    account_period = models.ForeignKey(Accumulated_fund, on_delete= models.CASCADE,blank=True, null=True)
    transaction_date = models.DateField()
    sub_code = models.ForeignKey(Sub_Accounts, on_delete=models.CASCADE)
    description = models.CharField(max_length=300)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    church = models.ForeignKey(Church,on_delete=models.CASCADE,blank=True, null=True)
    type = models.CharField(max_length=25, choices= typ, default='Church')
    reference = models.ForeignKey(Offerings,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('auth.User', related_name='arcreatedby', on_delete=models.SET_NULL, blank=True, null=True,default=None)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, related_name='armodifiedby', blank=True, null=True,default=None)

    history = HistoricalRecords()

    def __str__(self):
        return self.sub_code.sub_code + " "+ self.description


    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.modified_by = user
        super(Account_Receivables, self).save(*args, **kwargs)



class Pledges(models.Model):

    sts= (
        ('pending','pending'),
        ('approved','approved'),
        ('cancelled','cancelled'),
    )
   
    transaction_date = models.DateField()
    account_period = models.ForeignKey(Accumulated_fund, on_delete= models.CASCADE,blank=True, null=True)
    id = models.CharField(max_length=100, primary_key=True)
    sub_code = models.ForeignKey(Sub_Accounts, on_delete=models.CASCADE)
    description = models.CharField(max_length=300)
    church = models.ForeignKey(Church,on_delete=models.CASCADE,blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices= sts, default='pending')
    
    history = HistoricalRecords()

    def __str__(self):
        return self.description 
    
    def save(self, *args, **kwargs):
        if not self.id:
            number = incrementor()
            self.id = 'PL'+ '' +str(number())
            while Pledges.objects.filter(id=self.id).exists():
                self.id = 'PL'+ '' + str(number())
          
        self.balance = float(self.amount)-float(self.amount_paid)
        super(Pledges, self).save(*args, **kwargs)



class Pledges_Details(models.Model):
    
    pledge  = models.ForeignKey(Pledges,on_delete=models.CASCADE)
    member = models.ForeignKey(People,on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    history = HistoricalRecords()

    def __str__(self):
        return self.pledge.description + " "+ str(self.amount)

    
    def save(self, *args, **kwargs):
        self.balance = float(self.amount)-float(self.amount_paid)
        super(Pledges_Details, self).save(*args, **kwargs)



class Walfares(models.Model):
    
    sts= (
        ('pending','pending'),
        ('approved','approved'),
        ('cancelled','cancelled'),
         ('Walfare Posted','Welfare Posted'),
    )

    account_period = models.ForeignKey(Accumulated_fund, on_delete= models.CASCADE,blank=True, null=True)
    transaction_date = models.DateField()
    id = models.CharField(max_length=100, primary_key=True)
    sub_code = models.ForeignKey(Sub_Accounts, on_delete=models.CASCADE)
    church = models.ForeignKey(Church,on_delete=models.CASCADE,blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    member = models.ForeignKey(People,on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices= sts, default='pending')
    
    history = HistoricalRecords()

    def __str__(self):
        return str(self.amount)
    
    def save(self, *args, **kwargs):
        if not self.id:
            number = incrementor()
            self.id = 'WF'+ '' +str(number())
            while Walfares.objects.filter(id=self.id).exists():
                self.id = 'WF'+ '' + str(number())
        super(Walfares, self).save(*args, **kwargs)


class Transfers(models.Model):
    sts= (
        ('Pending','Pending'),
        ('Comfirmed','Comfirmed'),
        ('Cancelled','Cancelled'),

    )
    typ= (
        ('Church','Church'),
        ('Credit Union','Credit Union'),
        ('Welfare','Welfare'),
       
    )
    id = models.CharField(max_length=100, primary_key=True)
    account_period = models.ForeignKey(Accumulated_fund, on_delete= models.CASCADE,blank=True, null=True)
    transaction_date = models.DateField()

    tran_dec = models.CharField(max_length=300,default ='Transfer' ,blank=True,null=True)
    status = models.CharField(max_length=10, choices= sts,default='Comfirmed')
    fromaccount_code = models.ForeignKey(Sub_Accounts, on_delete=models.CASCADE, related_name='froms')
    toaccount_code = models.ForeignKey(Sub_Accounts, on_delete=models.CASCADE, related_name='to')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    church = models.ForeignKey(Church,on_delete=models.CASCADE,blank=True, null=True)
    type = models.CharField(max_length=25, choices= typ, default='Church')
    # toamount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_date = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey('auth.User', related_name='Trcreatedby', on_delete=models.SET_NULL, blank=True, null=True,default=None)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, related_name='trmodifiedby', blank=True, null=True,default=None)

    history = HistoricalRecords()

    def __str__(self):
        return str(self.amount)
    
    def save(self, *args, **kwargs):
        if not self.id:
            number = incrementor()
            self.id = 'TR'+ '' +str(number())
            while Transfers.objects.filter(id=self.id).exists():
                self.id = 'TR'+ '' + str(number())
        super(Transfers, self).save(*args, **kwargs)
    



class Tithe(models.Model):
    
    sts= (
        ('pending','pending'),
        ('approved','approved'),
        ('cancelled','cancelled'),
         ('Tithe Posted','Tithe Posted'),
    )
   
    transaction_date = models.DateField()
    account_period = models.ForeignKey(Accumulated_fund, on_delete= models.CASCADE,blank=True, null=True)
    id = models.CharField(max_length=100, primary_key=True)
    sub_code = models.ForeignKey(Sub_Accounts, on_delete=models.CASCADE)
    church = models.ForeignKey(Church,on_delete=models.CASCADE,blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    member = models.ForeignKey(People,on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices= sts, default='pending')
    
    history = HistoricalRecords()

    def __str__(self):
        return str(self.amount)
    
    def save(self, *args, **kwargs):
        if not self.id:
            number = incrementor()
            self.id = 'TH'+ '' +str(number())
            while Tithe.objects.filter(id=self.id).exists():
                self.id = 'TH'+ '' + str(number())
        super(Tithe, self).save(*args, **kwargs)