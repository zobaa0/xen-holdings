# Generated by Django 4.1.1 on 2023-01-09 01:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_alter_withdrawal_minimum'),
    ]

    operations = [
        migrations.AlterField(
            model_name='withdrawal',
            name='minimum',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='dashboard.minimumamount'),
        ),
    ]
