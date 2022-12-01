from django.shortcuts import render, redirect
from .forms import *
from .models import *

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum



def create_offering(request):
    church = request.user.profile.church
    

    
    offering = Offerings.objects.filter(church=church)
    template = 'accounts/manage_pv.html'
    if request.method == "POST":
        form = OfferingForm(request.POST)
        if form.is_valid():
            try:
                ff = Accumulated_fund.objects.filter(church=church).order_by('id').last()
                if ff is None :
                    messages.success(request,'You cannot Record an offering until you start an accounting year')
                    return redirect('accounts:create_offering')
                elif ff.status == 'Closed':
                    messages.success(request,'You cannot Record an offering until you start an accounting year')
                    return redirect('accounts:create_offering')
                else:
                    cc=form.save(commit=False)
                    vv = Accumulated_fund.objects.filter(church=church).order_by('id')
                    bb=vv.last()
                    cc.offstatus = "Pending"
                    cc.church = request.user.profile.church
                    cc.account_period=bb
                    cc.save()
                    messages.success(request, "Offering Recorded Please Comfirm")
                    return redirect('accounts:create_offering')

            except Accumulated_fund.DoesNotExist:
                pass

            

    
    else:
        form = OfferingForm()
    template = 'accounts/offerings.html'
    context = {
        'form':form,
        'offering':offering
    }
    return render(request,template,context)


def cancel_offering(request,pk):
    pv = Offerings.objects.get(id=pk)
    pv.status = "cancelled"
    pv.save()
    messages.success(request,'Offering Cancelled')
    return redirect('accounts:create_offering')

def approve_offering(request,pk):
    church = request.user.profile.church
    ff = Accumulated_fund.objects.filter(church=church).order_by('id').last()
    if ff is None :
        messages.success(request,'You cannot Approve an Offering until you start an accounting year')
        return redirect('accounts:create_offering')
    elif ff.status == 'Closed':
        messages.success(request,'You cannot approve an offering until you start an accounting year')
        return redirect('accounts:create_offering')
    else:
        pv = Offerings.objects.get(id=pk)
        pv.offstatus = "approved"
        Account_Receivables.objects.create(transaction_date=pv.transaction_date,sub_code=pv.sub_code,description=pv.description,amount=pv.amount,reference=pv,church=pv.church)
        All_Transaction.objects.create(transaction_date=pv.transaction_date,sub_code=pv.sub_code,description=pv.description,amount=pv.amount,church=pv.church,account_period=ff)
        General_Ledger.objects.create(transaction_date=pv.transaction_date,sub_code=pv.sub_code,description=pv.description,cedit=pv.amount,church=pv.church,transactionref=pv.id,account_period=ff)
        # AExpenditure.objects.create(account_code=pv.sub_account,amount=pv.amount,company=pv.company,pvno=pv)
        pv.save()
        messages.success(request,'Offering Approved')
        return redirect('accounts:create_offering')