"""App Tasks"""

# Standard Library
import datetime
import logging

# Third Party
from celery import shared_task
from corptools.models import CorporationAudit, CorporationWalletJournalEntry
from invoices.models import Invoice

# Alliance Auth
from allianceauth.eveonline.models import EveCharacter
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
    today = datetime.datetime.today()
    monday = today - datetime.timedelta(days=today.weekday())
    sunday = monday + datetime.timedelta(days=6)
    monday = monday.replace(hour=0, minute=0)
    sunday = sunday.replace(hour=23, minute=59)
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
        CorpTax.objects.update_or_create(
            corporation=corp.corporation,
            defaults={"tax_rate": taxRate, "amount": corpTotal},
        )
    pass


@shared_task
def generate_invoice():
    today = datetime.datetime.today() - datetime.timedelta(days=7)
    monday = today - datetime.timedelta(days=today.weekday())
    sunday = monday + datetime.timedelta(days=6)
    monday = monday.replace(hour=0, minute=0)
    sunday = sunday.replace(hour=23, minute=59)
    due = sunday + datetime.timedelta(days=7)
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
        # Only do taxes if they are more then 10m
        if corpTotal > 10000000:
            ref = f"RT{corp.id}-{monday.year}{monday.month:02}{monday.day:02}-{sunday.year}{sunday.month:02}{sunday.day:02}"
            # Check existance of ref
            if Invoice.objects.filter(invoice_ref=ref).exists():
                logger.info(f"Invoice {ref} already exists!")
            else:
                msg = f"Ratting Tax for {esiInfo['name']}: {monday.year}.{monday.month:02}.{monday.day:02} - {sunday.year}.{sunday.month:02}.{sunday.day:02}"
                try:
                    ceo = EveCharacter.objects.get(character_id=esiInfo["ceo_id"])
                except EveCharacter.DoesNotExist:
                    ceo = EveCharacter.objects.create_character(
                        character_id=esiInfo["ceo_id"]
                    )
                inv = Invoice.objects.create(
                    character_id=ceo.id,
                    amount=corpTotal,
                    invoice_ref=ref,
                    note=msg,
                    due_date=due,
                )
                inv.save()
    pass
