# Generated by Django 5.0.6 on 2024-06-21 05:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messageapp', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='group',
        ),
        migrations.RemoveField(
            model_name='message',
            name='attachment',
        ),
        migrations.RemoveField(
            model_name='usermessage',
            name='attachment',
        ),
        migrations.DeleteModel(
            name='Group',
        ),
    ]