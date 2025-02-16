# Generated by Django 4.2.17 on 2025-01-15 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jobs", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="job",
            name="days_required",
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="job",
            name="rate",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="job",
            name="description",
            field=models.TextField(default=""),
        ),
        migrations.AlterField(
            model_name="job",
            name="title",
            field=models.CharField(default="", max_length=255),
        ),
    ]
