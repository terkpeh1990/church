from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from smartchurch.models import People
import datetime


def create_pleges(request):
    church = request.user.profile.church
    if request.method == "POST":
        form = PledgeForm(request.POST)
        if form.is_valid():
            try:
                ff = Accumulated_fund.objects.filter(church=church).order_by('id').last()
                if ff is None :
                    messages.success(request,'You cannot Record a pledge until you start an accounting year')
                    return redirect('accounts:create_offering')
                elif ff.status == 'Closed':
                    messages.success(request,'You cannot Record an pledge until you start an accounting year')
                    return redirect('accounts:create_offering')
                else:
                    cc=form.save(commit=False)
                    vv = Accumulated_fund.objects.filter(church=church).order_by('id')
                    bb=vv.last()
                    cc.church = church
                    cc.account_period=bb
                    cc.save()
                    return redirect('accounts:add_pledge_details',cc.id)

            except Accumulated_fund.DoesNotExist:
                pass
           
    else:
        form = PledgeForm()
    template = 'accounts/pledge.html'
    context = {
        'form':form,
    }
    return render(request,template,context)


def add_pledge_details(request,pk):
       
    people = People.objects.all()  
    
    try:
        pledge = Pledges.objects.get(id=pk)  
    except Pledges.DoesNotExist:
        pass

    try:
        general_ledger = General_Ledger.objects.filter(transactionref=pk) 
    except General_Ledger.DoesNotExist:
        pass
    try:
        pledge_details= Pledges_Details.objects.filter(pledge=pledge)
    except Pledges_Details.DoesNotExist:
        pass
    if pledge_details:
        gross_total = pledge_details.aggregate(cc=Sum('amount'))
        pledge.amount = gross_total['cc']
        pledge.save()
    else:
        gross_total = 0.00
        pledge.amount = gross_total
        pledge.save()

    if request.method =='POST':
        form=PledgeDetailForm(request.POST)
        prod = request.POST.get("pledge")
        print(prod)
   
        
        
        if form.is_valid():
            amount= form.cleaned_data.get('amount')
            
            item = People.objects.get(name=prod) 
            if Pledges_Details.objects.filter(member=item,pledge=pledge).exists():
                messages.success(request, item.surname + " "+ item.first_name +" "+"has already been selected")
                return redirect('accounts:add_pledge_details',pledge.id)
            else:
                instance = Pledges_Details.objects.create(member=item,amount=amount,pledge=pledge)
                messages.success(request, instance.member.surname + " "+ instance.member.first_name +" " +"Pledge added successfully")
                return redirect('accounts:add_pledge_details',pledge.id)
    else:
        form = PledgeDetailForm()

    
    template='accounts/detail-pledge.html'
    context={
        'people':people,
        'detail':pledge_details,
        'pledge':pledge,
        'general_ledger':general_ledger,
        'form':form,
    }
    return render(request,template,context)


def deletes_pledge(request,pk):
    pro = Pledges_Details.objects.get(id=pk)
    pv = Pledges.objects.get(id=pro.pledge.id)
    pv.amount -= pro.amount
    pv.save()
    pro.delete()
    return redirect('accounts:add_pledge_details',pv.id)


def manage_pledges(request):
    church = request.user.profile.church
    pv = Pledges.objects.filter(church=church)
    template = 'accounts/manage_pledge.html'
    context={
        'pv':pv,
    }
    return render(request,template,context)


def cancelled_pledge(request,pk):
    pv = Pledges.objects.get(id=pk)
    pv.status = "cancelled"
    pv.save()
    messages.success(request,'Pledge Cancelled')
    return redirect('accounts:add_pledge_details',pv.id)


def approve_pledge(request,pk):
    pv = Pledges.objects.get(id=pk)
    pv.status = "approved"
    # All_Transaction.objects.create(transaction_date=pv.transaction_date,sub_code=pv.sub_code,description=pv.description,amount=pv.amount,church=pv.church,account_period=pv.account_period)
    # General_Ledger.objects.create(transaction_date=pv.transaction_date,sub_code=pv.sub_code,description=pv.description,cedit=pv.amount,church=pv.church,transactionref=pv.id,account_period=pv.account_period)
    pv.save()
    messages.success(request,'Pledge Posted To General Ledger')
    return redirect('accounts:add_pledge_details',pv.id)



def plege_payment(request,pk):
    pledge_details= Pledges_Details.objects.get(id=pk)

    pv = Pledges.objects.get(id=pledge_details.pledge.id)
    today =datetime.date.today()
    if request.method == "POST":
        church = request.user.profile.church
        ff = Accumulated_fund.objects.filter(church=church).order_by('id').last()
        if ff is None :
            messages.success(request,'You cannot post a pledge until you start an accounting year')
            return redirect('accounts:add_pledge_details',pv.id)
        elif ff.status == 'Closed':
            messages.success(request,'You cannot post a pledge until you start an accounting year')
            return redirect('accounts:add_pledge_details',pv.id)
        else:
            form = paymentforms(request.POST)
            if form.is_valid():
                sub_code = form.cleaned_data.get("sub_code")
                amount = form.cleaned_data.get("amount_paid")

                All_Transaction.objects.create(transaction_date=today,sub_code=pv.sub_code,description=pv.description,amount=amount,church=pv.church,account_period=ff)
                General_Ledger.objects.create(transaction_date=today,sub_code=pv.sub_code,description=pv.description,cedit=amount,church=pv.church,transactionref=pv.id,account_period=ff)
            
                All_Transaction.objects.create(transaction_date=today,sub_code=sub_code,description=pv.description,amount=amount,church=pv.church,account_period=ff)
                General_Ledger.objects.create(transaction_date=today,sub_code=sub_code,description=pv.description,debit=amount,church=pv.church,transactionref=pv.id,account_period=ff)
                pledge_details.amount_paid+=amount
                pledge_details.save()
                pv.amount_paid+=amount
                pv.save()
            
                return redirect('accounts:add_pledge_details',pv.id)
    else:
        form = paymentforms()
    template = 'accounts/pledge_payment.html'
    context = {
        'form':form,
        'pledge':pv
    }
    return render(request,template,context)
