# Generated by Django 4.2.16 on 2024-10-16 16:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tracker", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="pricealert",
            name="product_image_url",
            field=models.CharField(default="", max_length=255),
        ),
    ]
