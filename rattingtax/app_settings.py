"""App Settings"""

# Django
from django.conf import settings

# put your app settings here


RATTING_TAX_RATE = getattr(settings, "RATTING_TAX_RATE", 0.05)
