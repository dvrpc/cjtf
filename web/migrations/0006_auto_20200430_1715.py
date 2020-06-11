# Generated by Django 3.0.3 on 2020-04-30 21:15

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_auto_20200424_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fundingresource',
            name='url',
            field=models.URLField(help_text='Include http://'),
        ),
        migrations.AlterField(
            model_name='page',
            name='sidebar',
            field=ckeditor.fields.RichTextField(blank=True, help_text='Sidebar/additional info (right column).', null=True),
        ),
    ]
