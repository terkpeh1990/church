# Generated by Django 4.1.1 on 2022-11-22 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0041_accumulated_fund_credit_open_amount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='accumulated_fund',
            name='creditunion_close_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='historicalaccumulated_fund',
            name='creditunion_close_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]