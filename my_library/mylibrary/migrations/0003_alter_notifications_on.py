# Generated by Django 4.2.2 on 2023-07-18 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mylibrary', '0002_alter_notifications_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notifications',
            name='on',
            field=models.DateTimeField(verbose_name='Date and Time'),
        ),
    ]