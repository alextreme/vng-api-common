# Generated by Django 2.0.6 on 2018-11-05 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="JWTSecret",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "identifier",
                    models.CharField(
                        max_length=50, unique=True, verbose_name="identifier"
                    ),
                ),
                ("secret", models.CharField(max_length=255, verbose_name="secret")),
            ],
        )
    ]
