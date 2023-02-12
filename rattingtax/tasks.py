"""App Tasks"""

# Standard Library
import datetime
import logging

# Third Party
from celery import shared_task
from corptools.models import CorporationAudit, CorporationWalletJournalEntry

# Alliance Auth
from esi.clients import EsiClientProvider

# AA RattingTax
from rattingtax.app_settings import RATTING_TAX_RATE
from rattingtax.models import CorpTax

logger = logging.getLogger(__name__)
esi = EsiClientProvider()

# Create your tasks here


@shared_task
def calculate_current_tax():
    # Find range
    today = datetime.date.today()
    monday = today - datetime.timedelta(days=today.weekday())
    sunday = monday + datetime.timedelta(days=6)
    corps = CorporationAudit.objects.all()
    corp: CorporationAudit
    for corp in corps:
        esiInfo = esi.client.Corporation.get_corporations_corporation_id(
            corporation_id=corp.corporation.corporation_id
        ).results()
        taxRate = round(esiInfo["tax_rate"], 2)
        entries = []
        wallet_journal = CorporationWalletJournalEntry.objects.filter(
            division__corporation__corporation__corporation_id=corp.corporation.corporation_id
        ).filter(date__range=[monday, sunday])
        for w in wallet_journal:
            # Filter all relevant payments
            if w.ref_type == "bounty_prizes" or w.ref_type == "ess_escrow_transfer":
                entries.append(w)
        # All relevant entries have been found, start calculating now
        corpTotal = 0
        for entry in entries:
            corpTotal += (float(entry.amount) / taxRate) * RATTING_TAX_RATE
        # Covert to integer
        corpTotal = int(corpTotal)
        CorpTax.objects.update_or_create(corporation=corp.corporation, amount=corpTotal)
    pass
