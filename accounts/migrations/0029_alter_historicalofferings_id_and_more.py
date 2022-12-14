# Generated by Django 4.1.1 on 2022-11-18 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0028_historicalpledges_amount_paid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalofferings',
            name='id',
            field=models.CharField(db_index=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='historicalpledges',
            name='id',
            field=models.CharField(db_index=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='offerings',
            name='id',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='pledges',
            name='id',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]
