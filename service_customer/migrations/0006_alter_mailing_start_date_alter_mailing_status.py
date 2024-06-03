# Generated by Django 5.0.6 on 2024-05-31 13:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_customer', '0005_alter_client_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='mailing',
            name='status',
            field=models.CharField(choices=[('created', 'Создана'), ('started', 'Начата'), ('finished', 'Завершена')], default='created', max_length=50),
        ),
    ]
