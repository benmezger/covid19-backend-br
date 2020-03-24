# Generated by Django 2.2.10 on 2020-03-24 13:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0003_auto_20200324_0028'),
        ('tracking', '0004_symptom_rule'),
    ]

    operations = [
        migrations.AddField(
            model_name='riskfactor',
            name='rule',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='risk_factors', to='rules.LogicalCondition'),
        ),
    ]
