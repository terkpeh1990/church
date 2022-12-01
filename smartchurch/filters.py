import django_filters
from django import forms
from django_filters import DateFilter, CharFilter, NumberFilter
from .models import *


class DateInput(forms.DateInput):
    input_type = 'date'



class MemberFilter(django_filters.FilterSet):
    
    start_age = NumberFilter(field_name="member__age", lookup_expr='gte', label='Start Age',
                           

                            )
    end_age = NumberFilter(field_name="member__age", lookup_expr='lte', label='End Age',
                         

                          )
    class Meta:
        model = Church_Members
        fields = ['start_age','end_age', 'member__gender','member__status','member__marital_status']