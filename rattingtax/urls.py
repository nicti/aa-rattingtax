"""App URLs"""

# Django
from django.urls import path

# AA RattingTax
# AA RattingTax App
from rattingtax import views

app_name: str = "rattingtax"

urlpatterns = [
    path("", views.index, name="index"),
    path("list_data", views.rattingtax_list_data, name="rattingtax_list_data"),
]
