from django.urls import path
from .views import index, generate_consent, dhan_callback, api_thankyou

urlpatterns = [
    path("", index, name="index"),  
    path("generate-consent/", generate_consent, name="generate_consent"),
    path("dhan-callback/", dhan_callback, name="dhan_callback"),
    path("APIThankyou/", api_thankyou, name="api_thankyou"),
]
