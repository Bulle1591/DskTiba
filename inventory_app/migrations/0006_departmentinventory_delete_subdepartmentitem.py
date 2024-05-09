# Generated by Django 5.0.3 on 2024-05-05 12:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr_app', '0002_alter_designation_title_alter_jobtype_title'),
        ('inventory_app', '0005_alter_item_dosage_form_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DepartmentInventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr_app.department')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory_app.item')),
                ('sub_department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hr_app.subdepartmentmaster')),
            ],
        ),
        migrations.DeleteModel(
            name='SubDepartmentItem',
        ),
    ]