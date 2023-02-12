"""App Views"""

# Django
from django.contrib.auth.decorators import login_required, permission_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# AA RattingTax
from rattingtax.helper.serializer import CorpTaxSerializer
from rattingtax.models import CorpTax


@login_required
@permission_required("rattingtax.basic_access")
def index(request: WSGIRequest) -> HttpResponse:
    return render(request, "rattingtax/index.html")


@login_required
@permission_required("rattingtax.basic_access")
def rattingtax_list_data(request: WSGIRequest) -> JsonResponse:
    """Fetch view for tax list"""
    if request.user.has_perm("rattingtax.alliance_access"):
        corptax = CorpTax.objects.all()
    elif request.user.has_perm("rattingtax.corp_access"):
        corp = request.user.profile.main_character.corporation
        corptax = CorpTax.objects.filter(corporation=corp)
    else:
        return JsonResponse({"data": []})
    serializer = CorpTaxSerializer(corptax)
    return JsonResponse({"data": serializer.to_list(request)})
