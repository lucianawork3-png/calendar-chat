"""
Run once to get Microsoft OAuth refresh token via device flow.
Output: prints MS_REFRESH_TOKEN and MS_CLIENT_ID to copy into .env

Setup:
1. Go to https://portal.azure.com → App registrations → New registration
2. Name it anything, Accounts: "Personal Microsoft accounts only"
3. Add redirect URI: https://login.microsoftonline.com/common/oauth2/nativeclient (Mobile/Desktop)
4. Copy the Application (client) ID — that's your MS_CLIENT_ID
"""
import msal

CLIENT_ID = input("Paste your Azure App Client ID: ").strip()
SCOPES = ["Calendars.ReadWrite", "offline_access"]

app = msal.PublicClientApplication(
    CLIENT_ID,
    authority="https://login.microsoftonline.com/consumers",
)

flow = app.initiate_device_flow(scopes=SCOPES)
print("\n" + flow["message"])  # Tells user to visit URL and enter code

result = app.acquire_token_by_device_flow(flow)

if "refresh_token" in result:
    print("\n=== Copy these into your .env ===")
    print(f"MS_CLIENT_ID={CLIENT_ID}")
    print(f"MS_TENANT_ID=consumers")
    print(f"MS_REFRESH_TOKEN={result['refresh_token']}")
else:
    print("Auth failed:", result.get("error_description"))
