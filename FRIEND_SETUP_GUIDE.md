# Calendar Chat — Setup Guide
*Follow these steps to get your own Calendar Chat running. No coding needed.*

---

## What you'll need
- A computer (Mac or Windows)
- A Google account (the one connected to your calendar)
- A GitHub account (free) → sign up at github.com
- A Streamlit account (free) → sign up at share.streamlit.io

Estimated time: **20–30 minutes**

---

## Step 1 — Copy the app code

1. Go to: **github.com/lucianawork3-png/calendar-chat**
2. Click the **Fork** button (top right)
3. Click **Create fork**

You now have your own copy of the app. ✅

---

## Step 2 — Set up Google Calendar access

This gives the app permission to add events to your calendar.

### 2a — Create a Google Cloud project

1. Go to **console.cloud.google.com** and sign in with your Google account
2. Click **Select a project** (top left) → **New Project**
3. Name it anything (e.g. `My Calendar Chat`) → click **Create**
4. Make sure the new project is selected in the top bar

### 2b — Enable the Calendar API

1. Click the search bar at the top → type **Google Calendar API** → click it
2. Click **Enable**

### 2c — Set up the consent screen

1. In the left menu click **Google Auth Platform** → click **Get started**
2. Fill in:
   - App name: `Calendar Chat`
   - User support email: your email
3. Click **Next** → **Audience** → select **External** → **Next**
4. Click **Data Access** → **Add or Remove Scopes** → search `calendar` → check **Google Calendar API** (the full access one) → **Update** → **Next**
5. Click **Finish**
6. Now click **Audience** in the left menu → scroll to **Test users** → **+ Add users** → add your Gmail address → **Save**

### 2d — Create credentials

1. Click **Clients** in the left menu → **+ Create Client**
2. Application type: **Desktop app**
3. Name: `Calendar Chat`
4. Click **Create** → then click **Download JSON**
5. Save the file as `credentials.json` somewhere easy to find (e.g. your Desktop)

---

## Step 3 — Get your Google token

This step connects your specific Google account to the app.

### 3a — Install Python (if you don't have it)

- **Mac:** open Terminal (search "Terminal" in Spotlight) and run:
  ```
  python3 --version
  ```
  If you see a version number, you're good. If not, go to **python.org/downloads** and install Python 3.

- **Windows:** go to **python.org/downloads**, download and install Python 3. During installation check **"Add Python to PATH"**.

### 3b — Install required libraries

Open Terminal (Mac) or Command Prompt (Windows) and run:
```
pip3 install google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### 3c — Run the auth script

1. In your forked GitHub repo, find the file **auth_google.py** → click it → click the **download** icon (or copy the raw content into a file called `auth_google.py` on your Desktop)
2. Move your `credentials.json` to the same folder as `auth_google.py`
3. In Terminal / Command Prompt, navigate to that folder:
   - Mac: `cd ~/Desktop` (or wherever you saved the files)
   - Windows: `cd C:\Users\YourName\Desktop`
4. Run:
   ```
   python3 auth_google.py
   ```
5. A browser window opens → sign in with your Google account → click **Allow**
6. Back in Terminal you'll see output starting with `=== GOOGLE_TOKEN_JSON ===`

**Copy and save these three values** (you'll need them in Step 5):
- Everything after `=== GOOGLE_TOKEN_JSON ===` → that's your **GOOGLE_REFRESH_TOKEN** (the `refresh_token` value inside the JSON)
- The `client_id` value
- The `client_secret` value

> **Tip:** To find the values, look inside the printed JSON for:
> `"refresh_token": "1//03..."` → copy everything between the quotes
> `"client_id": "511..."` → copy that
> `"client_secret": "GOCSPX-..."` → copy that

---

## Step 4 — Deploy to Streamlit Cloud

1. Go to **share.streamlit.io** → sign in with GitHub
2. Click **Create app**
3. Fill in:
   - Repository: `YOUR_GITHUB_USERNAME/calendar-chat`
   - Branch: `main`
   - Main file path: `app.py`
4. Click **Advanced settings** → **Secrets**
5. Paste the following (replacing the values with YOUR tokens from Step 3):

```
ANTHROPIC_API_KEY = "ask Luciana for this key"
GOOGLE_REFRESH_TOKEN = "paste your refresh_token value here"
GOOGLE_CLIENT_ID = "paste your client_id value here"
GOOGLE_CLIENT_SECRET = "paste your client_secret value here"
MS_CLIENT_ID = ""
MS_TENANT_ID = "consumers"
MS_REFRESH_TOKEN = ""
```

> **Note:** The ANTHROPIC_API_KEY above is shared — you can use the same one or create your own free at console.anthropic.com

6. Click **Save** → then click **Deploy**
7. Wait ~2 minutes for the app to build

---

## Step 5 — Add to your iPhone home screen

1. Open the app URL (from Streamlit Cloud) in **Safari** on your iPhone
2. Tap the **Share** button (box with arrow at the bottom of Safari)
3. Tap **Add to Home Screen**
4. Tap **Add**

The app now appears as an icon on your home screen. ✅

---

## Step 6 — Add your contacts (optional)

If you want to type "meet with [name]" and have it auto-send a calendar invite:

1. In your forked GitHub repo, click the file **contacts.py**
2. Click the **pencil icon** (Edit) 
3. Add your contacts in this format:
   ```python
   CONTACTS = {
       "sara": "sara@email.com",
       "john": "john@email.com",
   }
   ```
4. Click **Commit changes**

The app will update automatically within 30 seconds.

---

## Need help?

Contact Luciana — she set up the original app and can help you troubleshoot any step.
