"""
App Models
Create your models in here
"""

# Django
from django.db import models

# Alliance Auth
from allianceauth.eveonline.models import EveCorporationInfo


class General(models.Model):
    """Meta model for app permissions"""

    class Meta:
        """Meta definitions"""

        managed = False
        default_permissions = ()
        permissions = (
            ("basic_access", "Can access the corp tax overview"),
            ("corp_access", "Can access tax info for own corp"),
            ("alliance_access", "Can access tax info for alliance corps"),
        )


class CorpTax(models.Model):
    """Corp Tax object"""

    corporation = models.OneToOneField(
        EveCorporationInfo, on_delete=models.CASCADE, primary_key=True
    )
    amount = models.BigIntegerField(
        null=False,
        default=0,
    )
    tax_rate = models.FloatField(null=False, default=0)
    last_updated_at = models.DateTimeField(null=False, auto_now=True)
