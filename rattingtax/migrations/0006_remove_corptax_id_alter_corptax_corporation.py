# Generated by Django 4.0.9 on 2023-02-13 08:44

# Django
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("eveonline", "0017_alliance_and_corp_names_are_not_unique"),
        ("rattingtax", "0005_alter_corptax_corporation"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="corptax",
            name="id",
        ),
        migrations.AlterField(
            model_name="corptax",
            name="corporation",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                primary_key=True,
                serialize=False,
                to="eveonline.evecorporationinfo",
            ),
        ),
    ]