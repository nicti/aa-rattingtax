"""App Configuration"""

# Django
from django.apps import AppConfig

# AA RattingTax
# AA RattingTax App
from rattingtax import __version__


class RattingTaxConfig(AppConfig):
    """App Config"""

    name = "rattingtax"
    label = "rattingtax"
    verbose_name = f"RattingTax App v{__version__}"
