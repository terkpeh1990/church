
from django.shortcuts import render, redirect
from django.db import models
from crum import get_current_user
from django.db.models import Count
from django.conf import settings
from django.contrib.sessions.models import Session
from .forms import *
from .models import *
from django.db.models import Sum
from .filters import *
import datetime
from django.contrib import messages


def manage_receivables(request):
    payables = Account_Receivables.objects.filter(amount__gt=0.00)
    total_payables = payables.count()
    payable_value = payables.aggregate(cc=Sum('amount'))

    myFilter = ReceivableFilter(request.GET, queryset=payables)
    payables = myFilter.qs
    total_payables = payables.count()
    payable_value = payables.aggregate(cc=Sum('amount'))
    template = 'accounts/receivables.html'
    context={
        'payables':payables,
        'total_payables':total_payables,
        'payable_value':payable_value,
        'myFilter':myFilter,
       
    }
    return render(request,template,context)



def receive_payment(request, pk):# to visit again

    
   
    today =datetime.date.today()
    accounts = Sub_Accounts.objects.filter(code__tag = 'Cash-Eq').order_by('sub_description')
    payables = Account_Receivables.objects.get(reference=pk)
    offering = Offerings.objects.get(id=pk)
    general_ledger = General_Ledger.objects.filter(transactionref=pk)
    
    if request.method == "POST":
        church = request.user.profile.church
        ff = Accumulated_fund.objects.filter(church=church).order_by('id').last()
        if ff is None :
            messages.success(request,'You cannot post an offering until you start an accounting year')
            return redirect('accounts:receive_payment',offering.id)
        elif ff.status == 'Closed':
            messages.success(request,'You cannot post an offering until you start an accounting year')
            return redirect('accounts:receive_payment',offering.id)
        
        form = paymentform(request.POST)
        code = request.POST.get("code")
        a,_= code.split('-----')

        payables.amount -= offering.amount
        payables.save()
        aa = offering.amount
        
        subcode = Sub_Accounts.objects.get(sub_code = a)
        
        All_Transaction.objects.create(transaction_date=offering.transaction_date,sub_code=subcode,description=offering.description,amount=offering.amount,church=offering.church,account_period=ff)
        General_Ledger.objects.create(transaction_date=offering.transaction_date,sub_code=subcode,description=offering.description,debit=offering.amount,church=offering.church,transactionref=offering.id,account_period=ff)
        offering.offstatus = "Transact"
        offering.save()
        messages.success(request, "Offering Transacted, General Ledger Updates")
        return redirect('accounts:receive_payment',offering.id)

    

    context = {
        
        'payables':payables,
        'accounts':accounts,
        'general_ledger':general_ledger,
        'offering':offering,
        
    }
    template = 'accounts/rec_payment.html'
    return render(request, template, context)




