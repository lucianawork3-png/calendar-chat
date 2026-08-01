import json
import os
from datetime import datetime, timedelta, timezone

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def _get_creds() -> Credentials:
    token_json = os.environ.get("GOOGLE_TOKEN_JSON", "")
    creds_json = os.environ.get("GOOGLE_CREDENTIALS_JSON", "")

    if not token_json:
        raise RuntimeError("GOOGLE_TOKEN_JSON not set")

    # Strip whitespace and control characters that can sneak in via Streamlit secrets
    import re
    token_json_clean = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', token_json.strip())
    token_data = json.loads(token_json_clean)
    creds = Credentials.from_authorized_user_info(token_data, SCOPES)

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())

    return creds


def _service():
    return build("calendar", "v3", credentials=_get_creds(), cache_discovery=False)


def list_calendars() -> list[dict]:
    items = _service().calendarList().list().execute().get("items", [])
    return [
        {"id": c["id"], "label": c.get("summary", c["id"]), "provider": "google"}
        for c in items
        if c.get("accessRole") in ("owner", "writer")
    ]


def list_upcoming(calendar_id: str = "primary", max_results: int = 10) -> list[dict]:
    now = datetime.now(timezone.utc).isoformat()
    events = (
        _service()
        .events()
        .list(
            calendarId=calendar_id,
            timeMin=now,
            maxResults=max_results,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
        .get("items", [])
    )
    return [
        {
            "title": e.get("summary", "(no title)"),
            "start": e["start"].get("dateTime", e["start"].get("date")),
            "location": e.get("location"),
        }
        for e in events
    ]


def create_event(event_dict: dict) -> str:
    calendar_id = event_dict.get("calendar_id", "primary")
    body = {
        "summary": event_dict["title"],
        "start": {"dateTime": event_dict["start"], "timeZone": "Europe/Amsterdam"},
        "end": {"dateTime": event_dict["end"], "timeZone": "Europe/Amsterdam"},
    }
    if event_dict.get("location"):
        body["location"] = event_dict["location"]
    if event_dict.get("description"):
        body["description"] = event_dict["description"]

    result = _service().events().insert(calendarId=calendar_id, body=body).execute()
    return result.get("htmlLink", "")
