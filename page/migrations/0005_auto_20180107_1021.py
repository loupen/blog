# Generated by Django 2.0 on 2018-01-07 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0004_auto_20180107_1020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='brief',
            field=models.TextField(),
        ),
    ]