# Generated by Django 5.0.1 on 2024-02-07 06:28

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="About",
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
                ("name", models.CharField(max_length=55)),
                ("state", models.CharField(max_length=55)),
                ("lga", models.CharField(max_length=55)),
            ],
        ),
    ]
