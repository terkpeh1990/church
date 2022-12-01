from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .filters import *

def manage_transfer(request):
    profile = request.user.profile.church
    payables = Transfers.objects.filter(church=profile)

    myFilter = TransferFilter(request.GET, queryset=payables)
    payables = myFilter.qs
    church = request.user.profile.church

    if request.method =='POST':
        form=transferform(request.POST)

        if form.is_valid():
            try:
                ff = Accumulated_fund.objects.filter(church=church).order_by('id').last()
                if ff is None :
                    messages.success(request,'You cannot Record a tranfer until you start an accounting year')
                    return redirect('accounts:manage_transfer')
                elif ff.status == 'Closed':
                    messages.success(request,'You cannot Record a tranfer until you start an accounting year')
                    return redirect('accounts:manage_transfer')
                else:
                    cc=form.save(commit=False)
                    vv = Accumulated_fund.objects.filter(church=church).order_by('id')
                    bb=vv.last()
                    cc.status= 'Pending'
                    cc.church = church
                    cc.account_period=bb
                    cc.save()
                    messages.success(request,"Transfer Initiated")
                    return redirect('accounts:manage_transfer')
            except Accumulated_fund.DoesNotExist:
                pass

       

           
    else:
        form = transferform()

    template = 'accounts/manage_transfer.html'
    context={
        'payables':payables,
        'myFilter':myFilter,
        'form':form,
    }
    return render(request,template,context)


def edit_transfer(request,pk):
    transfer = Transfers.objects.get(id=pk)


    if request.method =='POST':
        form=transferform(request.POST,instance=transfer)

        if form.is_valid():

            form.save()

            messages.success(request,"Transfer Edited")
            return redirect('accounts:manage_transfer')
    else:
        form = transferform(instance=transfer)

    template = 'accounts/edit-transfer.html'

    context={

        'form':form,
    }
    return render(request,template,context)

def cancel_tranfer(request,pk):
    pv = Transfers.objects.get(id=pk)
    pv.status = "Cancelled"
    pv.save()
    messages.success(request,'Transfer Cancelled')
    return redirect('accounts:manage_transfer')


def comfirm_tranfer(request,pk):
    pv = Transfers.objects.get(id=pk)
    debit_transaction=General_Ledger.objects.create(transaction_date=pv.transaction_date,sub_code=pv.toaccount_code,description=pv.tran_dec,debit=pv.amount,type=pv.type,church=pv.church,account_period=pv.account_period)
    credit_transaction=General_Ledger.objects.create(transaction_date=pv.transaction_date,sub_code=pv.fromaccount_code,description=pv.tran_dec,cedit=pv.amount,type=pv.type,church=pv.church,account_period=pv.account_period)
    All_Transaction.objects.create(transaction_date=pv.transaction_date,sub_code=pv.toaccount_code,description=pv.tran_dec,amount=pv.amount,church=pv.church,type=pv.type,account_period=pv.account_period)
    All_Transaction.objects.create(transaction_date=pv.transaction_date,sub_code=pv.fromaccount_code,description=pv.tran_dec,amount= -pv.amount,church=pv.church,type=pv.type,account_period=pv.account_period)
    
    pv.status = "Comfirmed"
    pv.save()
    messages.success(request,'Transfer Comfirmed')
    return redirect('accounts:manage_transfer')



