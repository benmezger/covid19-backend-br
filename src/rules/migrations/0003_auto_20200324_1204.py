# Generated by Django 2.2.10 on 2020-03-24 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("rules", "0002_logicalcondition_rulecondition"),
    ]

    operations = [
        migrations.AlterField(
            model_name="logicalcondition",
            name="attribute",
            field=models.CharField(
                choices=[("age", "Age"), ("symptoms", "Symptoms")],
                max_length=10,
                verbose_name="Attribute",
            ),
        ),
        migrations.AlterField(
            model_name="logicalcondition",
            name="operator",
            field=models.CharField(
                choices=[
                    ("gt", ">"),
                    ("gte", ">="),
                    ("lt", "<"),
                    ("lte", "=<"),
                    ("IN", "in"),
                    ("NOT IN", "not in"),
                ],
                max_length=10,
                verbose_name="Operator",
            ),
        ),
        migrations.AlterField(
            model_name="logicalcondition",
            name="rule_condition",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="logical_conditions",
                to="rules.RuleCondition",
                verbose_name="Condition",
            ),
        ),
        migrations.AlterField(
            model_name="logicalcondition",
            name="value",
            field=models.CharField(max_length=100, verbose_name="Value"),
        ),
        migrations.AlterField(
            model_name="rule",
            name="message",
            field=models.CharField(max_length=255, verbose_name="Message"),
        ),
        migrations.AlterField(
            model_name="rule",
            name="name",
            field=models.CharField(max_length=255, verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="rulecondition",
            name="rule",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="conditions",
                to="rules.Rule",
                verbose_name="Rule",
            ),
        ),
    ]
