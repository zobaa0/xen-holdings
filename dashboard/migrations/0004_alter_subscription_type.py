# Generated by Django 4.1.1 on 2023-01-09 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_alter_withdrawal_minimum'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='type',
            field=models.CharField(default='Investment', editable=False, max_length=10),
        ),
    ]
