# Generated by Django 3.0.7 on 2020-10-07 21:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='url',
            options={'ordering': ('title', 'link')},
        ),
    ]
