# Generated by Django 5.0.1 on 2024-08-09 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_alter_product_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]