from django import forms

from rules.models import RuleCondition
from rules.selectors import rule_condition_has_logical
from tracking.models import RiskFactor, Symptom


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
