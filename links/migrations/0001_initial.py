# Generated by Django 3.1.1 on 2020-09-14 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channel_id', models.CharField(max_length=100)),
                ('listen', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='URL',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, null=True)),
                ('link', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=1000, null=True)),
                ('image', models.TextField(max_length=1000, null=True)),
                ('msg', models.CharField(default='', max_length=100)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]