# Generated by Django 4.1.8 on 2023-05-18 17:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("extrafeetype", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("processingtask", "0001_initial"),
        ("product", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ExtraFee",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now, editable=False, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now, editable=False, verbose_name="modified"
                    ),
                ),
                (
                    "unit_price",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=20, verbose_name="Unit Price"),
                ),
                ("unit_percentage", models.FloatField(blank=True, default=0, null=True, verbose_name="Percentage")),
                ("quantity", models.FloatField(blank=True, default=1, null=True, verbose_name="Quantity")),
                (
                    "unit_amount",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=20, verbose_name="Unit Amount"),
                ),
                (
                    "total_amount",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=20, verbose_name="Total Amount"),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(app_label)s_%(class)s_creator",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created by",
                    ),
                ),
                (
                    "extra_fee_type",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="extrafeetype.extrafeetype",
                        verbose_name="Extra Fee Type",
                    ),
                ),
                (
                    "last_modified_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(app_label)s_%(class)s_last_modified_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Last modified by",
                    ),
                ),
                (
                    "processing_task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="processingtask.processingtask",
                        verbose_name="Processing Task",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="product.product",
                        verbose_name="Product",
                    ),
                ),
            ],
            options={
                "verbose_name": "Extra Fee",
                "verbose_name_plural": "Extra Fees",
                "db_table": "finance_extra_fee",
            },
        ),
    ]
