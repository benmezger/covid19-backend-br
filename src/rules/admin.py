from django import forms
from django.contrib import admin

from rules.models import LogicalCondition, Rule, RuleCondition


class RuleCustomForm(forms.ModelForm):
    class Meta:
        model = RuleCondition
        fields = "__all__"

    conditions = forms.ModelMultipleChoiceField(queryset=RuleCondition.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields["conditions"].initial = self.instance.conditions.all()

    def save(self, *args, **kwargs):
        instance = super().save(commit=False)
        instance.save()

        self.fields["conditions"].initial.update(rule=None)
        self.cleaned_data["conditions"].update(rule=instance)
        return instance


class LogicalConditionInlineAdmin(admin.TabularInline):
    model = LogicalCondition


@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    form = RuleCustomForm
    list_display = ("name", "enabled")
    list_filter = ("name", "enabled")
    search_fields = ("name", "message")


@admin.register(RuleCondition)
class RuleConditionAdmin(admin.ModelAdmin):
    list_display = ("get_name",)
    list_filter = ("rule__name",)
    search_fields = ("rule__name",)
    inlines = (LogicalConditionInlineAdmin,)

    def get_name(self, obj):
        return obj.rule

    get_name.short_description = "Name"
