# Generated by Django 4.1.1 on 2022-11-30 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartchurch', '0010_historicalpeople_name_people_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalpeople',
            name='age',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='people',
            name='age',
            field=models.IntegerField(default=0),
        ),
    ]
