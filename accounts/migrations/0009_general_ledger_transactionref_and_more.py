# Generated by Django 4.1.1 on 2022-10-05 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_rename_amount_general_ledger_cedit_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='general_ledger',
            name='transactionref',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='historicalgeneral_ledger',
            name='transactionref',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
