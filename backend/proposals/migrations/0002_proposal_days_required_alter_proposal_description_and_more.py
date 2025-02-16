# Generated by Django 4.2.17 on 2025-01-15 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("proposals", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="proposal",
            name="days_required",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="proposal",
            name="description",
            field=models.TextField(default=""),
        ),
        migrations.AlterField(
            model_name="proposal",
            name="rate",
            field=models.IntegerField(default=0),
        ),
    ]
