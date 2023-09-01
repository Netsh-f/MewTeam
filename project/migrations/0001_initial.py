# Generated by Django 4.2.4 on 2023-08-31 09:38

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("team", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Document",
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
                ("name", models.CharField(max_length=63)),
                ("create_at", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "modified_at",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("is_deleted", models.BooleanField(default=False)),
            ],
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
                ("name", models.CharField(max_length=63)),
                ("is_deleted", models.BooleanField(default=False)),
                (
                    "create_time",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("delete_time", models.DateTimeField(null=True)),
                ("cover", models.CharField(max_length=127)),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="team.team"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Prototype",
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
                ("name", models.CharField(max_length=63)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="project.project",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PrototypeContent",
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
                ("content", models.JSONField(null=True)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "prototype",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="project.prototype",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DocumentDir",
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
                ("name", models.CharField(max_length=63)),
                (
                    "par_dir",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="project.documentdir",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="project.project",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DocumentContent",
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
                ("content", models.TextField()),
                ("timestamp", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "document",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="project.document",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="document",
            name="par_dir",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="project.documentdir"
            ),
        ),
        migrations.AddField(
            model_name="document",
            name="project",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="project.project"
            ),
        ),
    ]
