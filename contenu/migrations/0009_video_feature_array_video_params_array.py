# Generated by Django 4.1 on 2023-09-30 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenu', '0008_cluster_centroid'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='feature_array',
            field=models.BinaryField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='params_array',
            field=models.BinaryField(default=None, null=True),
        ),
    ]
