# Generated by Django 3.0.3 on 2020-06-25 16:44

from django.db import migrations, models
import web.models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0015_auto_20200625_1119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateField(validators=[web.models.validate_date_not_past]),
        ),
    ]