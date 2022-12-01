from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from smartchurch.models import People
import datetime


def add_tithe(request):
       
    people = People.objects.all()  
   
    church = request.user.profile.church

    try:
        welfare = Tithe.objects.filter(church=church)
    except Tithe.DoesNotExist:
        pass
    

    if request.method =='POST':
        form=TitheForm(request.POST)
        prod = request.POST.get("pledge")
        print(prod)
   
        
        
        if form.is_valid():
            try:
                ff = Accumulated_fund.objects.filter(church=church).order_by('id').last()
                if ff is None :
                    messages.success(request,'You cannot Record a tithe until you start an accounting year')
                    return redirect('accounts:add_tithe')
                elif ff.status == 'Closed':
                    messages.success(request,'You cannot Record a tithe until you start an accounting year')
                    return redirect('accounts:add_tithe')
                else:
                    
                    vv = Accumulated_fund.objects.filter(church=church).order_by('id')
                    bb=vv.last()
                    amount= form.cleaned_data.get('amount')
                    transaction_date = form.cleaned_data.get('transaction_date')
                    sub_code = form.cleaned_data.get('sub_code')
                    item = People.objects.get(name=prod)
                    church = church
                    instance = Tithe.objects.create(transaction_date=transaction_date,member=item,amount=amount,sub_code=sub_code,church=church,status="pending",account_period=bb)
                    messages.success(request, instance.member.surname + " "+ instance.member.first_name +" " +"Tithe recorded successfully")
                    return redirect('accounts:add_tithe')
                    

            except Accumulated_fund.DoesNotExist:
                pass
           
    else:
        form = TitheForm()

    
    template='accounts/tithe.html'
    context={
        'people':people,
        'welfare':welfare,
        'form':form,
    }
    return render(request,template,context)


def cancelled_tithe(request,pk):
    pv = Tithe.objects.get(id=pk)
    pv.status = "cancelled"
    pv.save()
    messages.success(request,'Tithe Cancelled')
    return redirect('accounts:add_tithe')


def approve_tithe(request,pk):
    pv = Tithe.objects.get(id=pk)
    pv.status = "approved"
    All_Transaction.objects.create(transaction_date=pv.transaction_date,sub_code=pv.sub_code,description="Tithe contribution",amount=pv.amount,church=pv.church,account_period=pv.account_period)
    General_Ledger.objects.create(transaction_date=pv.transaction_date,sub_code=pv.sub_code,description="Tithe contribution",cedit=pv.amount,church=pv.church,transactionref=pv.id,account_period=pv.account_period)
    pv.save()
    messages.success(request,'Walfare Posted To General Ledger')
    return redirect('accounts:add_tithe')


def receive_tithe(request, pk):# to visit again
   
    today =datetime.date.today()
    accounts = Sub_Accounts.objects.filter(code__tag = 'Cash-Eq').order_by('sub_description')
    # payables = Account_Receivables.objects.get(reference=pk)
    offering = Tithe.objects.get(id=pk)
    general_ledger = General_Ledger.objects.filter(transactionref=pk)
    
    if request.method == "POST":
        form = paymentform(request.POST)
        code = request.POST.get("code")
        a,_= code.split('-----')

     
        
        subcode = Sub_Accounts.objects.get(sub_code = a)
        
        All_Transaction.objects.create(transaction_date=offering.transaction_date,sub_code=subcode,description="Tithe contribution",amount=offering.amount,church=offering.church,account_period=offering.account_period)
        General_Ledger.objects.create(transaction_date=offering.transaction_date,sub_code=subcode,description="Tithe contribution",debit=offering.amount,church=offering.church,transactionref=offering.id,account_period=offering.account_period)
        offering.status = "Tithe Posted"
        offering.save()
        messages.success(request, "Tithe Transacted, General Ledger Updates")
        return redirect('accounts:receive_tithe',offering.id)

    

    context = {
        
        
        'accounts':accounts,
        'general_ledger':general_ledger,
        'offering':offering,
        
    }
    template = 'accounts/rec_tithe.html'
    return render(request, template, context)