from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum,Q
from smartchurch.models import Church_Members
from django.db.models.functions import TruncMonth
import datetime


def dashboard(request):
    profile = request.user.profile.church
    today = datetime.datetime.now()
    all_members = Church_Members.objects.filter(church=profile)
    sub_account = Sub_Accounts.objects.filter(code__tag='Cash-Eq',all_transaction__type='Church')
    cash_eq = sub_account.values('sub_description').annotate(total=Sum('all_transaction__amount')).values('sub_description','sub_code','total').exclude(total__lte=0)
    transfer = Transfers.objects.filter(church=profile)

    all_transaction = All_Transaction.objects.filter(type='Church').annotate(month = TruncMonth('transaction_date'))
    monthly_transaction_in_year = all_transaction.values('month').annotate(revenue=Sum('amount',filter=Q(sub_code__code__group='Revenue')),expenditure=Sum('amount',filter=Q(sub_code__code__group='Expense'))).values('month','revenue','expenditure').filter(transaction_date__year=today.year)
    
    ff = Accumulated_fund.objects.filter(church=profile).order_by('id').last()
    accounting_year = Accumulated_fund.objects.filter(church=profile, status = 'Closed')
    if ff is None :
       open_balace = 0.00
    else:
        open_balace = ff.open_amount

  
    template = 'accounts/dashboard.html'

    context = {
        'cash_eq': cash_eq,
        'transfer':transfer,
        'all_members':all_members,
        'monthly_transaction_in_year':monthly_transaction_in_year,
        'open_balace':open_balace,
        'accounting_year':accounting_year,
    }

    return render(request,template,context)