# Generated by Django 4.1 on 2023-05-11 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contenu", "0002_alter_video_unique_together_la_video_special_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="video",
            name="order_id",
            field=models.PositiveSmallIntegerField(default=14),
        ),
    ]
