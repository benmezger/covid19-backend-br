# Generated by Django 2.2.10 on 2020-03-22 04:10

import django.db.models.deletion
import django_extensions.db.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rules", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="RuleCondition",
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
                    "rule",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="conditions",
                        to="rules.Rule",
                        verbose_name="Regra",
                    ),
                ),
            ],
            options={
                "ordering": ("-modified", "-created"),
                "get_latest_by": "modified",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="LogicalCondition",
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
                    "attribute",
                    models.CharField(
                        choices=[("age", "Idade")],
                        max_length=10,
                        verbose_name="Atributo",
                    ),
                ),
                (
                    "operator",
                    models.CharField(
                        choices=[
                            ("gt", ">"),
                            ("gte", ">="),
                            ("lt", "<"),
                            ("lte", "=<"),
                        ],
                        max_length=10,
                        verbose_name="Operador",
                    ),
                ),
                ("value", models.CharField(max_length=100, verbose_name="Valor")),
                (
                    "rule_condition",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="logical_conditions",
                        to="rules.RuleCondition",
                        verbose_name="Condicao",
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