# Generated by Django 5.0.2 on 2024-03-13 08:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='N', max_length=1),
        ),
        migrations.AlterField(
            model_name='employeephoto',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr_app.employee'),
        ),
    ]
