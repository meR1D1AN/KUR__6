# Generated by Django 5.0.6 on 2024-07-06 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("service_customer", "0003_alter_mailing_active"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mailing",
            name="active",
            field=models.BooleanField(
                choices=[(True, "Да"), (False, "Нет")],
                verbose_name="Активна ли подписка",
            ),
        ),
    ]
