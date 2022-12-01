# Generated by Django 4.1.1 on 2022-10-03 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartchurch', '0005_rename_profile_pic_historicalpeople_profile_picture_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='emmergency_contact',
            old_name='specify',
            new_name='if_others_specify',
        ),
        migrations.AlterField(
            model_name='emmergency_contact',
            name='relationship',
            field=models.CharField(blank=True, choices=[('Father', 'Father'), ('Mother', 'Mother'), ('Sibling', 'Sibling'), ('Friend', 'Friend'), ('Spouse', 'Spouse'), ('Child', 'Child'), ('Others', 'Others')], max_length=30, null=True),
        ),
    ]