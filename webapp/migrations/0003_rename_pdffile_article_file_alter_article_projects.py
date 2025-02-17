# Generated by Django 5.0.7 on 2024-12-29 01:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("webapp", "0002_article_image_user_verificationcode_user_isverified_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="article",
            old_name="PDFfile",
            new_name="File",
        ),
        migrations.AlterField(
            model_name="article",
            name="projects",
            field=models.ManyToManyField(blank=True, to="webapp.project"),
        ),
    ]
