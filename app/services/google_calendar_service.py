from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo
import json

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from app.core.config import settings

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]


@dataclass
class CalendarEventResult:
    summary: str
    start_time: str
    html_link: str


class GoogleCalendarService:
    def _get_credentials(self) -> Credentials:
        token_path = Path(settings.google_token_path)
        credentials_path = Path(settings.google_credentials_path)

        creds = None

        if token_path.exists():
            try:
                creds = Credentials.from_authorized_user_file(
                    str(token_path),
                    SCOPES,
                )
            except (json.JSONDecodeError, ValueError):
                token_path.unlink(missing_ok=True)
                creds = None

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(credentials_path),
                    SCOPES,
                )
                creds = flow.run_local_server(port=0, open_browser=False)

            token_path.write_text(creds.to_json(), encoding="utf-8")

        return creds

    async def create_event(
        self,
        start_dt: datetime,
        summary: str,
    ) -> CalendarEventResult:
        creds = self._get_credentials()
        service = build("calendar", "v3", credentials=creds)

        tz = ZoneInfo(settings.google_timezone)

        start_dt = start_dt.replace(tzinfo=tz)
        end_dt = (start_dt + timedelta(hours=1))

        event_body = {
            "summary": summary,
            "start": {
                "dateTime": start_dt.isoformat(),
            },
            "end": {
                "dateTime": end_dt.isoformat(),
            },
        }

        created_event = (
            service.events()
            .insert(calendarId=settings.google_calendar_id, body=event_body)
            .execute()
        )

        return CalendarEventResult(
            summary=created_event["summary"],
            start_time=start_dt.strftime("%Y-%m-%d %H:%M"),
            html_link=created_event["htmlLink"],
        )