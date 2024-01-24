# Generated by Django 5.0.1 on 2024-01-23 19:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_remove_product_tags_product_vendor"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="product_status",
            field=models.CharField(
                choices=[
                    ("draft", "Draft"),
                    ("disabled", "Disabled"),
                    ("rejected", "Rejected"),
                    ("inreview", "in Review"),
                    ("published", "Published"),
                ],
                default="inreview",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="vendor",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="category",
                to="core.vendor",
            ),
        ),
    ]