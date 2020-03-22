from django.contrib import admin

from tracking.models import Person, PersonRiskFactor, PersonStatusChange, RiskFactor


@admin.register(PersonRiskFactor)
class PersonRiskFactorAdmin(admin.ModelAdmin):
    list_display = ("risk_factor", "person")
    search_fields = ("risk_factor", "person")


@admin.register(RiskFactor)
class RiskFactorAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


class PersonStatusChangeInline(admin.TabularInline):
    model = PersonStatusChange
    extra = 0


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("id", "age", "status", "beacon_id")
    search_fields = ("beacon_id",)
    list_filter = ("status",)

    inlines = (PersonStatusChangeInline,)
