# Generated by Django 2.2 on 2019-06-11 20:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_auto_20190611_1923'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='meal',
            options={'ordering': ['-date']},
        ),
    ]
