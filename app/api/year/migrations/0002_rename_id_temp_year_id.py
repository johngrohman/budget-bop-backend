# Generated by Django 4.2.11 on 2025-03-02 06:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("year", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="year",
            old_name="id_temp",
            new_name="id",
        ),
    ]
