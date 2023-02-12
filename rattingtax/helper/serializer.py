# Django
from django.utils.html import format_html

# Alliance Auth
from allianceauth.eveonline.evelinks.eveimageserver import corporation_logo_url
from allianceauth.eveonline.evelinks.evewho import corporation_url

# AA RattingTax
from rattingtax.models import CorpTax


class CorpTaxSerializer:
    def __init__(self, queryset) -> None:
        self.queryset = queryset

    def to_list(self, request) -> list:
        return [self.serialize_obj(obj, request) for obj in self.queryset]

    def serialize_obj(self, corptax: CorpTax, request) -> dict:
        return {
            "corp_icon": format_html(
                '<img src="{}" width="{}" height="{}"/>',
                corporation_logo_url(corptax.corporation.corporation_id, 32),
                32,
                32,
            ),
            "corporation_id": corptax.corporation.corporation_id,
            "corporation_name": format_html(
                '<a href="{}" target="_blank">{}</a>',
                corporation_url(corptax.corporation.corporation_id),
                corptax.corporation.corporation_name,
            ),
            "corporation_ticker": corptax.corporation.corporation_ticker,
            "amount": f"{corptax.amount:,.2f} ISK",
            "last_updated": corptax.last_updated_at,
        }
