# import requests
# from django.shortcuts import render, redirect
# from django.http import JsonResponse, HttpResponse

# # Replace with your actual credentials
# PARTNER_ID = "29ac65b8"
# PARTNER_SECRET = "cc07014b-43f7-4846-a0f8-bb28b87c2562"

# # Redirect URL set in Dhan Partner Portal
# REDIRECT_URL = "https://i4imerged.uniquefinserve.com/APIThankyou" 

# def index(request):
#     """ Home page with Login with Dhan button """
#     return render(request, "index.html")

# def generate_consent(request):
#     """ Step 1: Generate Consent ID with date range and redirect user to Dhan login """
#     from_date = request.GET.get("from_date")
#     to_date = request.GET.get("to_date")

#     if not from_date or not to_date:
#         return JsonResponse({"error": "Date range required"}, status=400)

#     url = "https://auth.dhan.co/partner/generate-consent"
#     headers = {
#         "Content-Type": "application/json",
#         "partner_id": PARTNER_ID,
#         "partner_secret": PARTNER_SECRET
#     }

#     response = requests.get(url, headers=headers)
#     data = response.json()

#     if response.status_code == 200 and "consentId" in data:
#         consent_id = data["consentId"]
#         print(f"Generated Consent ID: {consent_id}")

#         # Store dates in session to use after authentication
#         request.session["from_date"] = from_date
#         request.session["to_date"] = to_date

#         dhan_login_url = f"https://auth.dhan.co/consent-login?consentId={consent_id}"
#         return redirect(dhan_login_url)
#     else:
#         print("Error generating consent:", data)
#         return JsonResponse({"error": "Failed to generate consent"}, status=400)

# def dhan_callback(request):
#     """ Step 3: Handle callback, get token, and fetch trade data """
#     consent_id = request.GET.get("consentId")

#     if not consent_id:
#         return JsonResponse({"error": "Consent ID not found"}, status=400)

#     print(f"Received Consent ID: {consent_id}")

#     url = f"https://auth.dhan.co/partner/consume-consent?token-Id={token_id}"
#     headers = {
#         "Content-Type": "application/json",
#         "partner_id": PARTNER_ID,
#         "partner_secret": PARTNER_SECRET
#     }
#     payload = {"consentId": consent_id}

#     response = requests.post(url, json=payload, headers=headers)
#     data = response.json()

#     if response.status_code == 200:
#         user_id = data.get("userId")
#         token_id = data.get("token-Id")  # Updated token name

#         print(f"User ID: {user_id}, Token-ID: {token_id}")

#         # Get stored date range from session
#         from_date = request.session.get("from_date")
#         to_date = request.session.get("to_date")

#         if not from_date or not to_date:
#             return JsonResponse({"error": "Date range not found in session"}, status=400)

#         # Fetch trade data
#         trade_data = fetch_trade_data(token_id, from_date, to_date)

#         return JsonResponse({
#             "user_id": user_id,
#             "token_id": token_id,
#             "trades": trade_data
#         })
#     else:
#         print("Error consuming consent:", data)
#         return JsonResponse({"error": "Failed to consume consent"}, status=400)

# def fetch_trade_data(token_id, from_date, to_date):
#     """ Fetch trade data from Dhan API """
#     url = f"https://api.dhan.co/v2/trades/{from_date}/{to_date}/1"
#     headers = {
#         "Accept": "application/json",
#         "access-token": token_id  # Updated to match token ID
#     }

#     response = requests.get(url, headers=headers)

#     if response.status_code == 200:
#         trade_data = response.json()
#         print(f"Trade Data: {trade_data}")
#         return trade_data
#     else:
#         print("Error fetching trade data:", response.text)
#         return {"error": "Failed to fetch trade data"}

# def api_thankyou(request):
#     """ Final thank-you page after authentication """
#     user_id = request.GET.get("user_id")
#     token_id = request.GET.get("token_id")

#     if user_id and token_id:
#         return HttpResponse(f"Authentication successful!<br>User ID: {user_id}<br>Token-ID: {token_id}")
#     else:
#         return HttpResponse("Authentication failed. No user data received.", status=400)


import requests
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse

# Replace these with your actual Partner credentials
PARTNER_ID = "29ac65b8"
PARTNER_SECRET = "cc07014b-43f7-4846-a0f8-bb28b87c2562"

def index(request):
    """ Home page with Login with Dhan button """
    return render(request, "index.html")

def generate_consent(request):
    """ Step 1: Generate Consent ID and Redirect User to Dhan Login """
    url = "https://auth.dhan.co/partner/generate-consent"
    headers = {
        "Content-Type": "application/json",
        "partner_id": PARTNER_ID,
        "partner_secret": PARTNER_SECRET
    }

    print(f"\n[REQUEST] POST {url}")
    print(f"Headers: {headers}")

    response = requests.post(url, headers=headers)
    data = response.json()

    print(f"[RESPONSE] Status: {response.status_code}")
    print(f"Response Body: {data}")

    if response.status_code == 200 and "consentId" in data:
        consent_id = data["consentId"]
        print(f"[SUCCESS] Generated Consent ID: {consent_id}")

        # Redirect user to Dhan login
        dhan_login_url = f"https://auth.dhan.co/consent-login?consentId={consent_id}"
        return redirect(dhan_login_url)
    else:
        print("[ERROR] Failed to generate consent:", data)
        return JsonResponse({"error": "Failed to generate consent", "details": data}, status=400)

def dhan_callback(request):
    """ Step 2: Handle Callback after Dhan Login """
    token_id = request.GET.get("tokenid")

    print(f"\n[CALLBACK] Received Token ID: {token_id}")

    if not token_id:
        print("[ERROR] Token ID not found in callback URL")
        return JsonResponse({"error": "Token ID not found"}, status=400)

    # Redirect to fetch user details & access token
    return redirect(f"/fetch_access_token?tokenId={token_id}")

def fetch_access_token(request):
    """ Step 3: Fetch Access Token using Token ID """
    token_id = request.GET.get("tokenId")

    if not token_id:
        print("[ERROR] Token ID is missing")
        return JsonResponse({"error": "Token ID is missing"}, status=400)

    url = f"https://auth.dhan.co/partner/consume-consent?tokenId={token_id}"
    headers = {
        "Content-Type": "application/json",
        "partner_id": PARTNER_ID,
        "partner_secret": PARTNER_SECRET
    }

    print(f"\n[REQUEST] GET {url}")
    print(f"Headers: {headers}")

    response = requests.get(url, headers=headers)
    data = response.json()

    print(f"[RESPONSE] Status: {response.status_code}")
    print(f"Response Body: {data}")

    if response.status_code == 200 and "access_token" in data:
        user_id = data.get("userId")
        access_token = data.get("access_token")

        print(f"[SUCCESS] User ID: {user_id}, Access Token: {access_token}")

        return JsonResponse({
            "user_id": user_id,
            "access_token": access_token,
            "user_details": data
        })
    else:
        print("[ERROR] Failed to fetch access token:", data)
        return JsonResponse({"error": "Failed to fetch access token", "details": data}, status=400)

def fetch_trade_data(request):
    """ Fetch Trade Data from Dhan API """
    access_token = request.GET.get("access_token")
    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")

    if not access_token or not from_date or not to_date:
        print("[ERROR] Missing required parameters")
        return JsonResponse({"error": "Missing required parameters"}, status=400)

    url = f"https://api.dhan.co/v2/trades/{from_date}/{to_date}/0"
    headers = {
        "Accept": "application/json",
        "access-token": access_token
    }

    print(f"\n[REQUEST] GET {url}")
    print(f"Headers: {headers}")

    response = requests.get(url, headers=headers)
    data = response.json()

    print(f"[RESPONSE] Status: {response.status_code}")
    print(f"Response Body: {data}")

    if response.status_code == 200:
        print("[SUCCESS] Trade Data Fetched")
        return JsonResponse(data)
    else:
        print("[ERROR] Failed to fetch trade data:", data)
        return JsonResponse({"error": "Failed to fetch trade data", "details": data}, status=400)


def api_thankyou(request):
    """ Display authentication success or failure message """
    user_id = request.GET.get("user_id")
    token_id = request.GET.get("token_id")

    if user_id and token_id:
        return HttpResponse(f"Authentication successful!<br>User ID: {user_id}<br>Token-ID: {token_id}")
    else:
        return HttpResponse("Authentication failed. No user data received.", status=400)
