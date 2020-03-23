from django.db import models


class EncounterManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("person_one", "person_two")
