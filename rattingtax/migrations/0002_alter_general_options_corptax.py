# Generated by Django 4.0.9 on 2023-02-12 12:22

# Django
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("eveonline", "0017_alliance_and_corp_names_are_not_unique"),
        ("rattingtax", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="general",
            options={
                "default_permissions": (),
                "managed": False,
                "permissions": (
                    ("basic_access", "Can access the corp tax overview"),
                    ("corp_access", "Can access tax info for own corp"),
                    ("alliance_access", "Can access tax info for alliance corps"),
                ),
            },
        ),
        migrations.CreateModel(
            name="CorpTax",
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
                ("amount", models.BigIntegerField(default=0)),
                ("last_updated_at", models.DateTimeField(auto_now=True)),
                (
                    "corporation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="eveonline.evecorporationinfo",
                    ),
                ),
            ],
        ),
    ]
