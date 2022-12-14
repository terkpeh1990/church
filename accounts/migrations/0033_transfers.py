# Generated by Django 4.1.1 on 2022-11-19 10:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('smartchurch', '0010_historicalpeople_name_people_name'),
        ('accounts', '0032_alter_historicalwalfares_status_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transfers',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('transaction_date', models.DateField()),
                ('tran_dec', models.CharField(blank=True, default='Transfer', max_length=300, null=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Comfirmed', 'Comfirmed'), ('Cancelled', 'Cancelled')], default='Comfirmed', max_length=10)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('type', models.CharField(choices=[('Church', 'Church'), ('Credit Union', 'Credit Union'), ('Welfare', 'Welfare')], default='Church', max_length=25)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('church', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='smartchurch.church')),
                ('created_by', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Trcreatedby', to=settings.AUTH_USER_MODEL)),
                ('fromaccount_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='froms', to='accounts.sub_accounts')),
                ('modified_by', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trmodifiedby', to=settings.AUTH_USER_MODEL)),
                ('toaccount_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to', to='accounts.sub_accounts')),
            ],
        ),
    ]
