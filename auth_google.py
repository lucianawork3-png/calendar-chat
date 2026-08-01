"""
Run once to get Google OAuth tokens.
Output: prints GOOGLE_TOKEN_JSON value to copy into .env
"""
import json
import os
import subprocess
import webbrowser
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/calendar"]
CREDS_FILE = "credentials.json"
PORT = 8765

if not os.path.exists(CREDS_FILE):
    print(f"Error: {CREDS_FILE} not found.")
    exit(1)

# Override webbrowser.open so run_local_server uses macOS `open` command
def _open_browser(url, new=0, autoraise=True):
    print(f"\nOpening browser:\n{url}\n")
    subprocess.Popen(["open", url])
    return True

webbrowser.open = _open_browser

flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)

print("Waiting for browser sign-in... (approve in the browser window that opens)")
creds = flow.run_local_server(port=PORT, open_browser=True, success_message="Done! Return to terminal.")

token_data = {
    "token": creds.token,
    "refresh_token": creds.refresh_token,
    "token_uri": creds.token_uri,
    "client_id": creds.client_id,
    "client_secret": creds.client_secret,
    "scopes": list(creds.scopes),
}

print("\n=== GOOGLE_TOKEN_JSON ===")
print(json.dumps(token_data))
print("\n=== GOOGLE_CREDENTIALS_JSON ===")
with open(CREDS_FILE) as f:
    print(f.read().replace("\n", ""))
