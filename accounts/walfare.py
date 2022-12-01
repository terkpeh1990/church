from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from smartchurch.models import People
import datetime


def add_walfare(request):
       
    people = People.objects.all()  
   
    church = request.user.profile.church

    try:
        welfare = Walfares.objects.filter(church=church)
    except Walfares.DoesNotExist:
        pass
    

    if request.method =='POST':
        form=WelfarelForm(request.POST)
        prod = request.POST.get("pledge")
        print(prod)
   
        
        
        if form.is_valid():
            amount= form.cleaned_data.get('amount')
            transaction_date = form.cleaned_data.get('transaction_date')
            sub_code = form.cleaned_data.get('sub_code')
            item = People.objects.get(name=prod)
            church = request.user.profile.church
            
            instance = Walfares.objects.create(transaction_date=transaction_date,member=item,amount=amount,sub_code=sub_code,church=church,status="pending")
            messages.success(request, instance.member.surname + " "+ instance.member.first_name +" " +"Walfare added successfully")
            return redirect('accounts:add_walfare')
    else:
        form = WelfarelForm()

    
    template='accounts/walfare.html'
    context={
        'people':people,
        'welfare':welfare,
        'form':form,
    }
    return render(request,template,context)


def cancelled_walfare(request,pk):
    pv = Walfares.objects.get(id=pk)
    pv.status = "cancelled"
    pv.save()
    messages.success(request,'Walfare Cancelled')
    return redirect('accounts:add_walfare')


def approve_walfare(request,pk):
    pv = Walfares.objects.get(id=pk)
    pv.status = "approved"
    All_Transaction.objects.create(transaction_date=pv.transaction_date,sub_code=pv.sub_code,description="Walfare contribution",amount=pv.amount,church=pv.church,type="Welfare")
    General_Ledger.objects.create(transaction_date=pv.transaction_date,sub_code=pv.sub_code,description="Walfare contribution",cedit=pv.amount,church=pv.church,transactionref=pv.id,type="Welfare")
    pv.save()
    messages.success(request,'Walfare Posted To General Ledger')
    return redirect('accounts:add_walfare')


def receive_walfare(request, pk):# to visit again
   
    today =datetime.date.today()
    accounts = Sub_Accounts.objects.filter(code__tag = 'Cash-Eq').order_by('sub_description')
    # payables = Account_Receivables.objects.get(reference=pk)
    offering = Walfares.objects.get(id=pk)
    general_ledger = General_Ledger.objects.filter(transactionref=pk)
    
    if request.method == "POST":
        form = paymentform(request.POST)
        code = request.POST.get("code")
        a,_= code.split('-----')

       
        aa = offering.amount
        
        subcode = Sub_Accounts.objects.get(sub_code = a)
        
        All_Transaction.objects.create(transaction_date=offering.transaction_date,sub_code=subcode,description="Walfare contribution",amount=offering.amount,church=offering.church,type="Welfare")
        General_Ledger.objects.create(transaction_date=offering.transaction_date,sub_code=subcode,description="Walfare contribution",debit=offering.amount,church=offering.church,transactionref=offering.id,type="Welfare")
        offering.status = "Walfare Posted"
        offering.save()
        messages.success(request, "Walfare Transacted, General Ledger Updates")
        return redirect('accounts:receive_walfare',offering.id)

    

    context = {
        
        
        'accounts':accounts,
        'general_ledger':general_ledger,
        'offering':offering,
        
    }
    template = 'accounts/rec_walfare.html'
    return render(request, template, context)
