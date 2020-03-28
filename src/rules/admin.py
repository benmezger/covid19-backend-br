import json

from django import forms
from django.contrib import admin

from rules.forms import RuleConditionCustomForm, RuleCustomForm
from rules.models import LogicalCondition, Rule, RuleCondition
from tracking.models import RiskFactor, Symptom
from tracking.selectors import get_risk_factors_list, get_symptoms_list
from utils.django.mixins import (
    CustomRuleConditionAddViewMixin,
    CustomRuleConditionChangeViewMixin,
)


class LogicalConditionInlineAdmin(admin.TabularInline):
    model = LogicalCondition
    form = RuleConditionCustomForm
    extra = 1


@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    form = RuleCustomForm
    list_display = ("name", "enabled")
    list_filter = ("name", "enabled")
    search_fields = ("name", "message")


@admin.register(RuleCondition)
class RuleConditionAdmin(
    CustomRuleConditionChangeViewMixin,
    CustomRuleConditionAddViewMixin,
    admin.ModelAdmin,
):
    list_display = ("get_name",)
    list_filter = ("rule__name",)
    search_fields = ("rule__name",)
    inlines = (LogicalConditionInlineAdmin,)

    def get_name(self, obj):
        return obj.rule

    get_name.short_description = "Name"
