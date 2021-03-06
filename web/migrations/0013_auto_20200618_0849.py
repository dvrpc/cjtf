# Generated by Django 3.0.3 on 2020-06-18 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0012_auto_20200611_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='fundingresource',
            name='due_date',
            field=models.DateField(blank=True, null=True, verbose_name='Due Date'),
        ),
        migrations.AlterField(
            model_name='fundingresource',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Program Name'),
        ),
        migrations.AlterField(
            model_name='fundingresource',
            name='source_name',
            field=models.CharField(max_length=200, verbose_name='Source'),
        ),
        migrations.AlterField(
            model_name='technicalresource',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Product Name'),
        ),
        migrations.AlterField(
            model_name='technicalresource',
            name='publication_date',
            field=models.DateField(verbose_name='Publication Date'),
        ),
    ]
