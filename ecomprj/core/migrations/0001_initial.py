# Generated by Django 5.0.1 on 2024-01-21 14:07

import core.models
import django.db.models.deletion
import shortuuid.django_fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
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
                (
                    "category_id",
                    shortuuid.django_fields.ShortUUIDField(
                        alphabet="abcdefgh12345",
                        length=10,
                        max_length=20,
                        prefix="CAT",
                        unique=True,
                    ),
                ),
                ("title", models.CharField(default="Accessories", max_length=100)),
                (
                    "image",
                    models.ImageField(default="category.jpg", upload_to="category"),
                ),
            ],
            options={
                "verbose_name_plural": "Categories",
            },
        ),
        migrations.CreateModel(
            name="Tags",
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
            ],
        ),
        migrations.CreateModel(
            name="Address",
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
                ("address", models.CharField(max_length=100, null=True)),
                ("status", models.BooleanField(default=False)),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Addresses",
            },
        ),
        migrations.CreateModel(
            name="CartOrder",
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
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2, default="0.00", max_digits=999999999999
                    ),
                ),
                ("paid_status", models.BooleanField(default=False)),
                ("order_date", models.DateTimeField(auto_now_add=True)),
                (
                    "product_status",
                    models.CharField(
                        choices=[
                            ("process", "Processing"),
                            ("intransit", "In-Transit"),
                            ("shipped", "Shipped"),
                            ("delivered", "Delivered"),
                        ],
                        default="processing",
                        max_length=30,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Cart Orders",
            },
        ),
        migrations.CreateModel(
            name="CartOrderItems",
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
                ("invoice_no", models.CharField(max_length=200)),
                ("product_status", models.CharField(max_length=200)),
                ("item", models.CharField(max_length=200)),
                ("image", models.CharField(max_length=200)),
                ("quantity", models.IntegerField(default=0)),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2, default="0.00", max_digits=999999999999
                    ),
                ),
                (
                    "total",
                    models.DecimalField(
                        decimal_places=2, default="0.00", max_digits=999999999999
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.cartorder"
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Cart Order Items",
            },
        ),
        migrations.CreateModel(
            name="Product",
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
                (
                    "product_id",
                    shortuuid.django_fields.ShortUUIDField(
                        alphabet="abcdefgh12345",
                        length=10,
                        max_length=20,
                        prefix="PDT",
                        unique=True,
                    ),
                ),
                ("title", models.CharField(default="Branded Tshirt", max_length=100)),
                (
                    "image",
                    models.ImageField(
                        default="product.jpg", upload_to=core.models.user_dir_path
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, default="This is a good product", null=True
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2, default="10.00", max_digits=999999999999
                    ),
                ),
                (
                    "standard_price",
                    models.DecimalField(
                        decimal_places=2, default="5.00", max_digits=999999999999
                    ),
                ),
                ("specifications", models.TextField(blank=True, null=True)),
                (
                    "product_status",
                    models.CharField(
                        choices=[
                            ("draft", "Drafr"),
                            ("disabled", "Disabled"),
                            ("rejected", "Rejected"),
                            ("inreview", "in Review"),
                            ("published", "Published"),
                        ],
                        default="inreview",
                        max_length=10,
                    ),
                ),
                ("status", models.BooleanField(default=True)),
                ("in_stock", models.BooleanField(default=True)),
                ("featured", models.BooleanField(default=False)),
                ("digital", models.BooleanField(default=False)),
                (
                    "sku",
                    shortuuid.django_fields.ShortUUIDField(
                        alphabet="0123456789",
                        length=4,
                        max_length=10,
                        prefix="sku",
                        unique=True,
                    ),
                ),
                ("date", models.DateTimeField(blank=True, null=True)),
                (
                    "category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="core.category",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "tags",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="core.tags",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Products",
            },
        ),
        migrations.CreateModel(
            name="ProductImages",
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
                (
                    "images",
                    models.ImageField(
                        default="product.jpg", upload_to="product-images"
                    ),
                ),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "product",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="core.product",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Product Images",
            },
        ),
        migrations.CreateModel(
            name="ProductReview",
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
                ("review", models.TextField()),
                (
                    "rating",
                    models.IntegerField(
                        choices=[
                            (1, "★☆☆☆☆"),
                            (2, "★★☆☆☆"),
                            (3, "★★★☆☆"),
                            (4, "★★★★☆"),
                            (5, "★★★★★"),
                        ],
                        default=None,
                    ),
                ),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "product",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="core.product",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Product Reviews",
            },
        ),
        migrations.CreateModel(
            name="Vendor",
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
                (
                    "vendor_id",
                    shortuuid.django_fields.ShortUUIDField(
                        alphabet="abcdefgh12345",
                        length=10,
                        max_length=20,
                        prefix="VEN",
                        unique=True,
                    ),
                ),
                ("title", models.CharField(default="Mix&Pix", max_length=100)),
                (
                    "image",
                    models.ImageField(
                        default="vendor.jpg", upload_to=core.models.user_dir_path
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, default="The most reliable vendor", null=True
                    ),
                ),
                ("address", models.CharField(default="1300,O'Block", max_length=100)),
                ("contact", models.CharField(default="+254113708866", max_length=100)),
                ("response_time", models.CharField(default="1", max_length=100)),
                ("shipping_time", models.CharField(default="100", max_length=100)),
                ("rating", models.CharField(default="100", max_length=100)),
                ("return_days", models.CharField(default="100", max_length=100)),
                ("warranty_period", models.CharField(default="100", max_length=100)),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Vendors",
            },
        ),
        migrations.CreateModel(
            name="WishList",
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
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "product",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="core.product",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "wishlists",
            },
        ),
    ]