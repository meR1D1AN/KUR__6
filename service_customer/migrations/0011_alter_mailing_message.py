# Generated by Django 5.0.6 on 2024-06-03 11:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_customer', '0010_alter_message_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service_customer.message'),
        ),
    ]
