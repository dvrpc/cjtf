# Generated by Django 3.0.3 on 2020-02-19 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0009_auto_20200219_1116'),
    ]

    operations = [
        migrations.AddField(
            model_name='fundingresource',
            name='source_name',
            field=models.CharField(default='dvrpc', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='fundingresource',
            name='source_url',
            field=models.URLField(),
        ),
    ]
