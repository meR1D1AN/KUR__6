# Generated by Django 5.0.6 on 2024-07-06 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("service_customer", "0012_alter_mailing_periodicity"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mailing",
            name="periodicity",
            field=models.IntegerField(
                choices=[
                    (1, "1 минута"),
                    (2, "Каждый день"),
                    (10080, "Каждую неделю"),
                    (43200, "Каждый месяц"),
                ],
                default="10080",
                verbose_name="Периодичность рассылки",
            ),
        ),
    ]
