# Generated by Django 3.0.3 on 2020-04-24 17:20

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_auto_20200422_1421'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='location',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateTimeField(help_text='Date in format m/d/yyyy, m/d/yy, yy-m-d, or yyyy-m-d  and time in 24 hr format, i.e. 09:00 for 9am or 13:00 for 1pm'),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='date',
            field=models.DateTimeField(help_text='Date in format m/d/yyyy, m/d/yy, yy-m-d, or yyyy-m-d  and time in 24 hr format, i.e. 09:00 for 9am or 13:00 for 1pm'),
        ),
    ]