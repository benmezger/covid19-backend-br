from django.contrib import admin

from rules.forms import RuleConditionCustomForm, RuleCustomForm
from rules.models import LogicalCondition, Rule, RuleCondition
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
    list_display = ("name", "enabled", "any")
    list_filter = ("name", "enabled", "any")
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
