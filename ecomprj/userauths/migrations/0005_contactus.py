# Generated by Django 5.0.1 on 2024-02-03 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("userauths", "0004_profile_user"),
    ]

    operations = [
        migrations.CreateModel(
            name="ContactUs",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("full_name", models.CharField(max_length=200)),
                ("email", models.CharField(max_length=200)),
                ("phone", models.CharField(max_length=200)),
                ("subject", models.CharField(max_length=200)),
                ("message", models.TextField()),
            ],
        ),
    ]