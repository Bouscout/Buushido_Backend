# Generated by Django 4.1 on 2023-11-22 03:46

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='cluster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('centroid', models.BinaryField(default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='genres',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='anime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField(blank=True, null=True)),
                ('completed', models.BooleanField(default=True)),
                ('studios', models.CharField(blank=True, max_length=150, null=True)),
                ('num_episodes', models.IntegerField(default=12)),
                ('buushido_id', models.IntegerField(default=None, null=True)),
                ('anime_id', models.IntegerField(default=None, null=True)),
                ('portrait_pic', models.URLField(default=None, null=True)),
                ('nsfw', models.BooleanField(default=False)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(default=None, null=True)),
                ('rating', models.DecimalField(decimal_places=2, default=5.0, max_digits=4, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('features_vector', models.BinaryField(default=None, null=True)),
                ('params_vector', models.BinaryField(default=None, null=True)),
                ('cluster', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='recommendations.cluster')),
                ('genres', models.ManyToManyField(default=None, to='recommendations.genres')),
            ],
        ),
    ]
