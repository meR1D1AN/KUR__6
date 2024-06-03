# Generated by Django 5.0.6 on 2024-05-31 09:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('full_name', models.CharField(max_length=255)),
                ('comment', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=255, unique=True, verbose_name='Тема')),
                ('body', models.TextField(verbose_name='Текст')),
            ],
        ),
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('periodicity', models.CharField(choices=[('daily', 'Каждый день'), ('weekly', 'Каждую неделю'), ('monthly', 'Каждый месяц')], default='daily', max_length=50)),
                ('status', models.CharField(choices=[('created', 'Created'), ('started', 'Started'), ('finished', 'Finished')], default='created', max_length=50)),
                ('clients', models.ManyToManyField(to='service_customer.client')),
                ('message', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='service_customer.message')),
            ],
        ),
        migrations.CreateModel(
            name='MailingAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attempt_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=50)),
                ('server_response', models.TextField(blank=True, null=True)),
                ('mailing', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='service_customer.mailing')),
            ],
        ),
    ]
