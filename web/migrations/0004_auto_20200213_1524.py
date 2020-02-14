# Generated by Django 3.0.3 on 2020-02-13 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='internal_name',
            field=models.CharField(default='about', help_text='Do not change!', max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='page',
            name='left_column',
            field=models.TextField(help_text='Content in left column.'),
        ),
        migrations.AlterField(
            model_name='page',
            name='right_column',
            field=models.TextField(help_text='Content in right column.'),
        ),
        migrations.AlterField(
            model_name='page',
            name='title',
            field=models.CharField(help_text='Title of the page.', max_length=30),
        ),
    ]
