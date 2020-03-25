# Generated by Django 2.2.10 on 2020-03-24 00:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("rules", "0003_auto_20200324_0028"),
        ("tracking", "0003_auto_20200322_0444"),
    ]

    operations = [
        migrations.AddField(
            model_name="symptom",
            name="rule",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="symptoms",
                to="rules.LogicalCondition",
            ),
        ),
    ]
