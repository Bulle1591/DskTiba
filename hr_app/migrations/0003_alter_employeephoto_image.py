# Generated by Django 5.0.3 on 2024-05-09 06:08

import hr_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr_app', '0002_alter_designation_title_alter_jobtype_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeephoto',
            name='image',
            field=models.ImageField(default='media/staff/avatar.jpg', upload_to=hr_app.models.user_directory_path),
        ),
    ]
