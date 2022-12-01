from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from decimal import Decimal



def accounting_year(request):

    
    accounts = Accumulated_fund.objects.all()
    church = request.user.profile.church
    if request.method == 'POST':
        form = AccForm(request.POST)
        if form.is_valid():
            cc=form.save(commit=False)
            cc.church = church
            cc.save()
            messages.success(request,'Account Saved')
            return redirect('accounts:accounting_year')
    
    else:
        form = AccForm()

    template = 'accounts/accounting_year.html'

    context = {
        'accounts': accounts,
        'form':form,
    }

    return render(request,template,context)


def start_accounting_year(request,pk):
    pv = Accumulated_fund.objects.get(id=pk)
    try:
        cc = Accumulated_fund.objects.all().order_by('id')
        if cc:
            acc = cc.reverse()[1]
            if acc.close_amount is None:
                pv.open_amount = 0.00
            else:
                pv.open_amount = acc.close_amount
            
            if acc.walfare_open_amount is None:
                pv.walfare_open_amount = 0.00
            else:
                pv.walfare_open_amount = acc.walfare_close_amount
            
            if acc.credit_open_amount is None:
                pv.credit_open_amount = 0.00
            else:
                pv.credit_open_amount = acc.creditunion_close_amount

    except Accumulated_fund.DoesNotExist:
        pv.open_amount = 0.00
        pv.walfare_open_amount = 0.00
        pv.credit_open_amount = 0.00
        pass
    pv.status = "Open"
    pv.save()
    messages.success(request,'Accounting Period Opened')
    return redirect('accounts:accounting_year')


# def set_accounting_year_closure(request,pk):
#     pv = Accumulated_fund.objects.get(id=pk)
    
#     pv.status = "Set To Close"
#     pv.save()
#     messages.success(request,'Accounting Period Closure Set. lick Close Account to End the Accounting Period')
#     return redirect('accounts:accounting_year')

def close_accounting_year(request,pk):
    pv = Accumulated_fund.objects.get(id=pk)

    try:
        total_transaction = All_Transaction.objects.filter(account_period=pv.id)
        cash_eq = total_transaction.filter(sub_code__code__group='Revenue',type='Church')
        exp = total_transaction.filter(sub_code__code__group='Expense',type='Church')
        walfare_cash_eq = total_transaction.filter(sub_code__code__group='Revenue',type='Welfare')
        walfare_exp = total_transaction.filter(sub_code__code__group='Expense',type='Welfare')
        creditunion_cash_eq = total_transaction.filter(sub_code__code__group='Revenue',type='Credit Union')
        creditunion_exp = total_transaction.filter(sub_code__code__group='Expense',type='Credit Union')

        if cash_eq:
            if cash_eq is None:
                cash_value = 0.00
            else:
                cc = cash_eq.aggregate(cash=Sum('amount'))
                cash_value = cc['cash']
        else:
            cash_value = 0.00

        
        if walfare_cash_eq:
            if walfare_cash_eq is None:
                walfare_cash_value = 0.00
            else:
                aa = walfare_cash_eq.aggregate(walfare=Sum('amount'))
                walfare_cash_value = aa['walfare']

        else:
            walfare_cash_value = 0.00

        
        if creditunion_cash_eq:
            if creditunion_cash_eq is None:
                creditunion_cash_value = 0.00
            else:
                bb = creditunion_cash_eq.aggregate(creditunion=Sum('amount'))
                creditunion_cash_value = bb['walfare']
        else:
            creditunion_cash_value = 0.00




        if exp:
            if exp is None:
                exp_value = 0.00
            else:
                dd= exp.aggregate(exp=Sum('amount'))
                exp_value = dd['exp']
        else:
            exp_value = 0.00

        
        if walfare_exp:
            if walfare_exp is None:
                walfare_exp_value = 0.00
            else:
                ee = walfare_exp.aggregate(walfare_exp =Sum('amount'))
                walfare_exp_value =ee['walfare_exp']
        else:
            walfare_exp_value= 0.00

        
        if creditunion_exp:
            if creditunion_exp is None:
               creditunion_exp_value = 0.00
            else:
                ff= creditunion_exp.aggregate(creditunion_exp =Sum('amount'))
                creditunion_exp_value  =ff['creditunion_exp']
        else:
            creditunion_exp_value = 0.00


        print(cash_value)
        print(walfare_cash_value)
        print(creditunion_cash_value)
        profit = (float(cash_value)+float(pv.open_amount)) -  float(exp_value)
        walfare_profit = float(walfare_cash_value)  - float(walfare_exp_value)
        creditunion_profit = float(creditunion_cash_value)  - float(creditunion_exp_value)


        pv.close_amount = profit
        pv.walfare_close_amount = walfare_profit
        pv.creditunion_close_amount = creditunion_profit
       
    except Accumulated_fund.DoesNotExist:
        pv.close_amount = 0.00
        pv.walfare_close_amount = 0.00
        pv.creditunion_close_amount = 0.00
        pass
    pv.status = "Closed"
    pv.save()
    messages.success(request,'Accounting Period Closed')
    return redirect('accounts:accounting_year')




def set_closure_date_accounting_year(request,pk):
    
    close_acc = Accumulated_fund.objects.get(id=pk)
    accounts = Accumulated_fund.objects.all()
    
    if request.method == 'POST':
        form = AccCloseForm(request.POST)
        if form.is_valid():
            closing_date = form.cleaned_data.get("closing_date")
            close_acc.closing_date = closing_date
            close_acc.status = "Set To Close"
            close_acc.save()
            messages.success(request,'Accounting Period Closure Set. lick Close Account to End the Accounting Period')
            return redirect('accounts:accounting_year')
    
    else:
        form = AccCloseForm()

    template = 'accounts/close_acc_date.html'

    context = {
        'accounts': accounts,
        'form':form,
    }

    return render(request,template,context)

