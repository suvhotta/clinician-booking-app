# Generated by Django 4.0.4 on 2022-05-03 08:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinician', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clinician',
            name='joining_date',
        ),
    ]