# Generated by Django 5.1.3 on 2024-11-08 19:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("artwork", "0009_rename_creation_date_artwork_created_at_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="payment",
                to="artwork.order",
            ),
        ),
    ]
