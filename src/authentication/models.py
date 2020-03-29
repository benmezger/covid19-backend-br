import binascii
import os

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


# Addapted from rest_frammework.authtoken.models.Token
class PersonToken(models.Model):
    """
    The default authorization token model for person.
    """

    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    person = models.OneToOneField(
        "tracking.Person",
        related_name="auth_token",
        on_delete=models.CASCADE,
        verbose_name=_("Person"),
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    class Meta:
        # Work around for a bug in Django:
        # https://code.djangoproject.com/ticket/19422
        #
        # Also see corresponding ticket:
        # https://github.com/encode/django-rest-framework/issues/705
        abstract = "rest_framework.authtoken" not in settings.INSTALLED_APPS
        verbose_name = _("PersonToken")
        verbose_name_plural = _("PersonTokens")

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key
