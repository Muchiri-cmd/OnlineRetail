# Generated by Django 5.0.1 on 2024-02-01 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0014_alter_productreview_product"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cartorder",
            name="product_status",
            field=models.CharField(
                choices=[
                    ("processing", "Processing"),
                    ("intransit", "In-Transit"),
                    ("shipped", "Shipped"),
                    ("delivered", "Delivered"),
                ],
                default="processing",
                max_length=30,
            ),
        ),
    ]