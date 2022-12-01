# Generated by Django 4.1.1 on 2022-11-18 14:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('smartchurch', '0010_historicalpeople_name_people_name'),
        ('accounts', '0029_alter_historicalofferings_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Walfares',
            fields=[
                ('transaction_date', models.DateField()),
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('status', models.CharField(choices=[('pending', 'pending'), ('approved', 'approved'), ('cancelled', 'cancelled')], default='pending', max_length=20)),
                ('church', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='smartchurch.church')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smartchurch.people')),
                ('sub_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.sub_accounts')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalWalfares',
            fields=[
                ('transaction_date', models.DateField()),
                ('id', models.CharField(db_index=True, max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('status', models.CharField(choices=[('pending', 'pending'), ('approved', 'approved'), ('cancelled', 'cancelled')], default='pending', max_length=20)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('church', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='smartchurch.church')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('member', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='smartchurch.people')),
                ('sub_code', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='accounts.sub_accounts')),
            ],
            options={
                'verbose_name': 'historical walfares',
                'verbose_name_plural': 'historical walfaress',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]