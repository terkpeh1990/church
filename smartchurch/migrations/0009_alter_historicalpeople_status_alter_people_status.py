# Generated by Django 4.1.1 on 2022-10-03 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartchurch', '0008_rename_contact_name_emmergency_contact_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalpeople',
            name='status',
            field=models.CharField(blank=True, choices=[('New', 'New'), ('Foundation Class', 'Foundation Class'), ('Member', 'Member'), ('Inactive', 'Inactive'), ('Deceased', 'Deceased')], default='New', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='people',
            name='status',
            field=models.CharField(blank=True, choices=[('New', 'New'), ('Foundation Class', 'Foundation Class'), ('Member', 'Member'), ('Inactive', 'Inactive'), ('Deceased', 'Deceased')], default='New', max_length=30, null=True),
        ),
    ]
