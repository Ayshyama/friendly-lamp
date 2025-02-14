# Generated by Django 4.2.16 on 2025-01-19 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project_management", "0010_item_item_group"),
    ]

    operations = [
        migrations.RenameField(
            model_name="product",
            old_name="selling_price_inflation",
            new_name="selling_price",
        ),
        migrations.RemoveField(
            model_name="product",
            name="selling_price_safety_margin",
        ),
        migrations.AddField(
            model_name="product",
            name="article_number",
            field=models.CharField(default="A0001", max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="product",
            name="bundle_quantity",
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name="product",
            name="inflation_rate",
            field=models.FloatField(default=2.0, help_text="in %"),
        ),
        migrations.AddField(
            model_name="product",
            name="manufacturer",
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="packaging_cost_per_unite",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="product",
            name="product_type",
            field=models.CharField(
                choices=[
                    ("Produkt", "Produkt"),
                    ("Service", "Service"),
                    ("Arbeitszeit", "Arbeitszeit"),
                ],
                default="Produkt",
                max_length=128,
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="safety_margin",
            field=models.FloatField(default=2.0, help_text="in %"),
        ),
        migrations.AddField(
            model_name="product",
            name="shipping_cost_per_unite",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="product",
            name="target_purchase_price",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="product",
            name="unite",
            field=models.CharField(
                choices=[("Meter", "Meter"), ("Stück", "Stück"), ("Stunde", "Stunde")],
                default="Stück",
                max_length=32,
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="working_time",
            field=models.FloatField(default=0.0, help_text="in h"),
        ),
        migrations.AlterField(
            model_name="product",
            name="status",
            field=models.CharField(
                choices=[("aktiv", "aktiv"), ("veraltet", "veraltet")],
                default="aktiv",
                max_length=32,
            ),
        ),
    ]
