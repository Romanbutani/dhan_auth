# from django.urls import path
# from .views import index, generate_consent, dhan_callback, api_thankyou

# urlpatterns = [
#     path("", index, name="index"),  
#     path("generate-consent/", generate_consent, name="generate_consent"),
#     path("dhan-callback/", dhan_callback, name="dhan_callback"),
#     path("APIThankyou/", api_thankyou, name="api_thankyou"),
# ]


from django.urls import path
from .views import generate_consent, dhan_callback, fetch_access_token, fetch_trade_data, api_thankyou

urlpatterns = [
    path("generate_consent/", generate_consent, name="generate_consent"),
    path("dhan_callback/", dhan_callback, name="dhan_callback"),
    path("fetch_access_token/", fetch_access_token, name="fetch_access_token"),
    path("fetch_trade_data/", fetch_trade_data, name="fetch_trade_data"),
    path("APIThankyou/", api_thankyou, name="api_thankyou")
]
