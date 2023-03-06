"""App Views"""

# Django
from django.contrib.auth.decorators import login_required, permission_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# AA RattingTax
from rattingtax.app_settings import RATTING_TAX_RATE
from rattingtax.helper.serializer import CorpTaxSerializer
from rattingtax.models import CorpTax


@login_required
@permission_required("rattingtax.basic_access")
def index(request: WSGIRequest) -> HttpResponse:
    context = {"tax": (RATTING_TAX_RATE * 100)}
    return render(request, "rattingtax/index.html", context)


@login_required
@permission_required("rattingtax.basic_access")
def rattingtax_list_data(request: WSGIRequest) -> JsonResponse:
    """Fetch view for tax list"""
    if request.user.has_perm("rattingtax.alliance_access"):
        corptax = CorpTax.objects.all()
    elif request.user.has_perm("rattingtax.corp_access"):
        # TODO: Fix filtering for none main chars, e.g. CEO alts
        corp = request.user.profile.main_character.corporation
        corptax = CorpTax.objects.filter(corporation=corp)
    else:
        return JsonResponse({"data": []})
    serializer = CorpTaxSerializer(corptax)
    return JsonResponse({"data": serializer.to_list(request)})
