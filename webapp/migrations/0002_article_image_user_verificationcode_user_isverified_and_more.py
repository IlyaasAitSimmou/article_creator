# Generated by Django 5.0.7 on 2024-12-28 00:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("webapp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="article",
            name="Image",
            field=models.ImageField(blank=True, upload_to="images/"),
        ),
        migrations.AddField(
            model_name="user",
            name="VerificationCode",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="user",
            name="isVerified",
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name="Project",
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
                ("title", models.CharField(max_length=255)),
                ("Image", models.ImageField(blank=True, upload_to="images/")),
                ("PDFfile", models.FileField(upload_to="pdfs/")),
                ("content", models.TextField()),
                (
                    "ProjectSubThemes",
                    models.JSONField(blank=True, default=["default_themes"]),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="article",
            name="projects",
            field=models.ManyToManyField(to="webapp.project"),
        ),
    ]