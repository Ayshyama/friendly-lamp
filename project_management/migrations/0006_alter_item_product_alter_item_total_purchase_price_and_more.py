# Generated by Django 4.2.16 on 2025-01-11 12:26

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        (
            "project_management",
            "0005_itemgroup_projectcalculation_productgroup_product_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="item_set",
                to="project_management.product",
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="total_purchase_price",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="item",
            name="total_selling_price_margin",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="itemgroup",
            name="total_purchase_price",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="itemgroup",
            name="total_selling_price_margin",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="productgroup",
            name="name",
            field=models.CharField(
                choices=[
                    ("Hauptzuleitung", "Hauptzuleitung"),
                    ("Hauptverteiler", "Hauptverteiler"),
                    ("Lastmanagement", "Lastmanagement"),
                    ("Zähleranlage", "Zähleranlage"),
                ],
                default="Hauptzuleitung",
                max_length=256,
            ),
        ),
        migrations.AlterField(
            model_name="projectcalculation",
            name="execution_date",
            field=models.DateField(default=datetime.date(2025, 1, 11)),
        ),
        migrations.AlterField(
            model_name="projectcalculation",
            name="total_purchase_price",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="projectcalculation",
            name="total_selling_price_margin",
            field=models.FloatField(null=True),
        ),
    ]
