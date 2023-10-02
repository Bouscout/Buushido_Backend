# Generated by Django 4.1 on 2023-05-09 09:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("contenu", "0001_initial"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="video",
            unique_together=set(),
        ),
        migrations.AddField(
            model_name="la_video",
            name="special",
            field=models.CharField(blank=True, default=None, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name="la_video",
            name="url2",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="la_video",
            name="url3",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="video",
            name="background_tof2",
            field=models.ImageField(blank=True, null=True, upload_to="paysage_2/"),
        ),
        migrations.AddField(
            model_name="video",
            name="en_cours",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="video",
            name="has_film",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="video",
            name="note",
            field=models.FloatField(default=8.0),
        ),
        migrations.AddField(
            model_name="video",
            name="order_id",
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="video",
            name="other_name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="video",
            name="saisons",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="video",
            name="background_tof",
            field=models.ImageField(blank=True, null=True, upload_to="paysage/"),
        ),
        migrations.AlterField(
            model_name="video",
            name="genre_1",
            field=models.CharField(
                choices=[
                    ("Action", "Action"),
                    ("Aventure", "Aventure"),
                    ("Comedie", "Comedie"),
                    ("Drama", "Drama"),
                    ("Horreur", "Horreur"),
                    ("Romance", "Romance"),
                    ("Sci-fi", "Sci-fi"),
                    ("Slice of life", "Slice of life"),
                    ("Mystere", "Mystere"),
                    ("Seinen", "Seinen"),
                    ("Isekai", "Isekai"),
                    ("Shonen", "Shonen"),
                    ("Sport", "Sport"),
                    ("Fantaisie", "Fantaisie"),
                    ("Shojo", "Shojo"),
                    ("Thriller", "Thriller"),
                    ("Combat", "Combat"),
                    ("School life", "School life"),
                    ("Music", "Music"),
                    ("Ecchi", "Ecchi"),
                    ("Autres", "Autres"),
                    ("Classique", "Classique"),
                    ("Film", "Film"),
                ],
                max_length=50,
                verbose_name="genre",
            ),
        ),
        migrations.AlterField(
            model_name="video",
            name="genre_2",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Action", "Action"),
                    ("Aventure", "Aventure"),
                    ("Comedie", "Comedie"),
                    ("Drama", "Drama"),
                    ("Horreur", "Horreur"),
                    ("Romance", "Romance"),
                    ("Sci-fi", "Sci-fi"),
                    ("Slice of life", "Slice of life"),
                    ("Mystere", "Mystere"),
                    ("Seinen", "Seinen"),
                    ("Isekai", "Isekai"),
                    ("Shonen", "Shonen"),
                    ("Sport", "Sport"),
                    ("Fantaisie", "Fantaisie"),
                    ("Shojo", "Shojo"),
                    ("Thriller", "Thriller"),
                    ("Combat", "Combat"),
                    ("School life", "School life"),
                    ("Music", "Music"),
                    ("Ecchi", "Ecchi"),
                    ("Autres", "Autres"),
                    ("Classique", "Classique"),
                    ("Film", "Film"),
                ],
                max_length=50,
                null=True,
                verbose_name="genre",
            ),
        ),
        migrations.AlterField(
            model_name="video",
            name="genre_3",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Action", "Action"),
                    ("Aventure", "Aventure"),
                    ("Comedie", "Comedie"),
                    ("Drama", "Drama"),
                    ("Horreur", "Horreur"),
                    ("Romance", "Romance"),
                    ("Sci-fi", "Sci-fi"),
                    ("Slice of life", "Slice of life"),
                    ("Mystere", "Mystere"),
                    ("Seinen", "Seinen"),
                    ("Isekai", "Isekai"),
                    ("Shonen", "Shonen"),
                    ("Sport", "Sport"),
                    ("Fantaisie", "Fantaisie"),
                    ("Shojo", "Shojo"),
                    ("Thriller", "Thriller"),
                    ("Combat", "Combat"),
                    ("School life", "School life"),
                    ("Music", "Music"),
                    ("Ecchi", "Ecchi"),
                    ("Autres", "Autres"),
                    ("Classique", "Classique"),
                    ("Film", "Film"),
                ],
                max_length=50,
                null=True,
                verbose_name="genre",
            ),
        ),
        migrations.AlterField(
            model_name="video",
            name="genre_4",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Action", "Action"),
                    ("Aventure", "Aventure"),
                    ("Comedie", "Comedie"),
                    ("Drama", "Drama"),
                    ("Horreur", "Horreur"),
                    ("Romance", "Romance"),
                    ("Sci-fi", "Sci-fi"),
                    ("Slice of life", "Slice of life"),
                    ("Mystere", "Mystere"),
                    ("Seinen", "Seinen"),
                    ("Isekai", "Isekai"),
                    ("Shonen", "Shonen"),
                    ("Sport", "Sport"),
                    ("Fantaisie", "Fantaisie"),
                    ("Shojo", "Shojo"),
                    ("Thriller", "Thriller"),
                    ("Combat", "Combat"),
                    ("School life", "School life"),
                    ("Music", "Music"),
                    ("Ecchi", "Ecchi"),
                    ("Autres", "Autres"),
                    ("Classique", "Classique"),
                    ("Film", "Film"),
                ],
                max_length=50,
                null=True,
                verbose_name="genre",
            ),
        ),
        migrations.AlterField(
            model_name="video",
            name="poster_tof",
            field=models.ImageField(blank=True, null=True, upload_to="poster/"),
        ),
        migrations.AlterField(
            model_name="video",
            name="tof_url",
            field=models.ImageField(blank=True, null=True, upload_to="portrait/"),
        ),
        migrations.CreateModel(
            name="films",
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
                ("special_name", models.CharField(max_length=100)),
                ("saison", models.PositiveIntegerField(default=0)),
                ("url", models.CharField(blank=True, max_length=200, null=True)),
                ("url2", models.CharField(blank=True, max_length=200, null=True)),
                ("url3", models.CharField(blank=True, max_length=200, null=True)),
                (
                    "name",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenu.video",
                    ),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="video",
            name="moretext",
        ),
    ]
