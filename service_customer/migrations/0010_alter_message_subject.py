# Generated by Django 5.0.6 on 2024-06-03 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("service_customer", "0009_alter_mailing_periodicity"),
    ]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="subject",
            field=models.CharField(max_length=255, verbose_name="Тема"),
        ),
    ]
