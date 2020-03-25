from django.contrib import admin

from tracking.models import (
    Encounter,
    Person,
    PersonRiskFactor,
    PersonStatusChange,
    RiskFactor,
    Symptom,
)


@admin.register(PersonRiskFactor)
class PersonRiskFactorAdmin(admin.ModelAdmin):
    list_display = ("risk_factor", "person")
    search_fields = ("risk_factor", "person")


@admin.register(RiskFactor)
class RiskFactorAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    exclude = ("rule",)


class PersonStatusChangeInline(admin.TabularInline):
    model = PersonStatusChange
    extra = 0


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("id", "age", "status", "beacon_id")
    search_fields = ("beacon_id",)
    list_filter = ("status",)

    inlines = (PersonStatusChangeInline,)


@admin.register(Symptom)
class SymptomAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    exclude = ("rule",)


@admin.register(Encounter)
class EncounterAdmin(admin.ModelAdmin):
    list_display = (
        "person_one",
        "person_two",
        "start_date",
        "end_date",
        "duration",
        "min_distance",
    )

    search_fields = ("person_one", "person_two")
