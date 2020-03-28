import json

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
