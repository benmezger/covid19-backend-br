import json

from django import forms
from django.contrib import admin

from rules.models import LogicalCondition, Rule, RuleCondition
from tracking.models import RiskFactor, Symptom
from tracking.selectors import get_risk_factors_list, get_symptoms_list


class CustomRuleConditionBaseViewMixin:
    def extra_context(self) -> dict:
        context = {}

        symptoms = []
        for symptom in get_symptoms_list():
            symptom["text"] = symptom.pop("name")
            symptoms.append(symptom)

        risk_factors = []
        for risk_factor in get_risk_factors_list():
            risk_factor["text"] = risk_factor.pop("name")
            risk_factors.append(risk_factor)

        context["symptoms"] = json.dumps(symptoms)
        context["risk_factors"] = json.dumps(risk_factors)

        return context


class CustomRuleConditionChangeViewMixin(CustomRuleConditionBaseViewMixin):
    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context.update(self.extra_context())
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )


class CustomRuleConditionAddViewMixin(CustomRuleConditionBaseViewMixin):
    def add_view(self, request, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context.update(self.extra_context())
        return super().add_view(request, form_url, extra_context=extra_context)


class RuleCustomForm(forms.ModelForm):
    class Meta:
        model = RuleCondition
        fields = "__all__"

    conditions = forms.ModelMultipleChoiceField(
        queryset=RuleCondition.objects.all(), required=False
    )

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


class RuleConditionCustomForm(forms.ModelForm):
    class Meta:
        model = RuleCondition
        fields = "__all__"

    def clean(self):
        data = self.cleaned_data
        attr = data.get("attribute", None)

        if attr == "symptoms" and data.get("value", None):
            data["symptom_ids"] = list(map(int, data["value"].split(",")))
        elif attr == "risk_factors" and data.get("value", None):
            data["risk_factors_ids"] = list(map(int, data["value"].split(",")))

        self.cleaned_data = data
        return super().clean()

    def save(self, commit):
        if self.cleaned_data.get("symptom_ids", None):
            symptoms = Symptom.objects.filter(
                id__in=self.cleaned_data.pop("symptom_ids")
            )
            self.cleaned_data.pop("value")

            super().save(commit)
            self.instance.symptoms.add(*symptoms)
        elif self.cleaned_data.get("risk_factors_ids", None):
            risk_factors = RiskFactor.objects.filter(
                id__in=self.cleaned_data.pop("risk_factors_ids")
            )
            self.cleaned_data.pop("value")
            super().save(commit)
            self.instance.risk_factors.add(*risk_factors)
        else:
            super().save(commit)
        return self.instance


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
