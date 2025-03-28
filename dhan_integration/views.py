import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse

# Replace with your actual credentials
PARTNER_ID = "29ac65b8"
PARTNER_SECRET = "cc07014b-43f7-4846-a0f8-bb28b87c2562"

# Redirect URL set in Dhan Partner Portal
REDIRECT_URL ="https://i4imerged.uniquefinserve.com/APIThankyou"

def index(request):
    """ Home page with Login with Dhan button """
    return render(request, "index.html")

def generate_consent(request):
    """ Step 1: Generate Consent ID and redirect user to Dhan login """
    url = "https://auth.dhan.co/partner/generate-consent"
    headers = {
        "Content-Type": "application/json",
        "partner_id": PARTNER_ID,
        "partner_secret": PARTNER_SECRET
    }
    
    response = requests.get(url, headers=headers)
    data = response.json()

    if response.status_code == 200 and "consentId" in data:
        consent_id = data["consentId"]
        print(f"Generated Consent ID: {consent_id}")  # Print to local terminal
        dhan_login_url = f"https://auth.dhan.co/partner/consent-login?consentId={consent_id}&redirectUrl={REDIRECT_URL}"
        return redirect(dhan_login_url)  # Step 2: Redirect user to Dhan login
    else:
        print("Error generating consent:", data)  # Print error if any
        return JsonResponse({"error": "Failed to generate consent"}, status=400)

def dhan_callback(request):
    """ Step 3: Handle the callback and consume the consent """
    consent_id = request.GET.get("consentId")

    if not consent_id:
        print("Consent ID not found in callback")
        return JsonResponse({"error": "Consent ID not found"}, status=400)

    print(f"Received Consent ID: {consent_id}")  # Print received Consent ID

    url = "https://auth.dhan.co/partner/consume-consent"
    headers = {
        "Content-Type": "application/json",
        "partner_id": PARTNER_ID,
        "partner_secret": PARTNER_SECRET
    }
    payload = {"consentId": consent_id}

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()

    if response.status_code == 200:
        print(f"User ID: {data.get('userId')}, Token: {data.get('token')}")  # Print user details
        return redirect(f"{REDIRECT_URL}?user_id={data.get('userId')}&token={data.get('token')}")
    else:
        print("Error consuming consent:", data)  # Print error if any
        return JsonResponse({"error": "Failed to consume consent"}, status=400)

def api_thankyou(request):
    """ Handles the final redirect from Dhan after successful authentication """
    user_id = request.GET.get("user_id")
    token = request.GET.get("token")

    if user_id and token:
        print(f"User ID: {user_id}, Token: {token}")  # Print user data to local terminal
        return HttpResponse(f"Authentication successful!<br>User ID: {user_id}<br>Token: {token}")
    else:
        return HttpResponse("Authentication failed. No user data received.", status=400)
