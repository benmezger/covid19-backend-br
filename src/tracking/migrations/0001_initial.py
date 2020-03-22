# Generated by Django 2.2.10 on 2020-03-21 23:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Person",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("age", models.PositiveIntegerField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("D", "Desconhecido"),
                            ("S", "Suspeita de Corona Vírus"),
                            ("R", "Recuperado"),
                            ("C", "Corona Vírus Confirmado"),
                            ("N", "Negativado"),
                        ],
                        default="D",
                        max_length=1,
                    ),
                ),
                ("beacon_id", models.CharField(max_length=36, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="PersonStatusChange",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                (
                    "previous",
                    models.CharField(
                        choices=[
                            ("D", "Desconhecido"),
                            ("S", "Suspeita de Corona Vírus"),
                            ("R", "Recuperado"),
                            ("C", "Corona Vírus Confirmado"),
                            ("N", "Negativado"),
                        ],
                        default="D",
                        max_length=1,
                    ),
                ),
                (
                    "next",
                    models.CharField(
                        choices=[
                            ("D", "Desconhecido"),
                            ("S", "Suspeita de Corona Vírus"),
                            ("R", "Recuperado"),
                            ("C", "Corona Vírus Confirmado"),
                            ("N", "Negativado"),
                        ],
                        default="D",
                        max_length=1,
                    ),
                ),
                (
                    "health_professional",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "person",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="person_status_change",
                        to="tracking.Person",
                    ),
                ),
            ],
            options={
                "ordering": ("-modified", "-created"),
                "get_latest_by": "modified",
                "abstract": False,
            },
        ),
    ]
