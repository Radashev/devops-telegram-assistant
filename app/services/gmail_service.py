from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

from app.core.config import settings


class GmailService:
    def __init__(self):
        read_creds = Credentials.from_authorized_user_file(settings.gmail_token_path)
        self.service = build("gmail", "v1", credentials=read_creds)

    def fetch_messages(self, max_results: int = 10) -> list[dict]:
        results = self.service.users().messages().list(
            userId="me",
            maxResults=max_results,
            labelIds=["INBOX"],
        ).execute()

        messages = results.get("messages", [])
        emails = []

        for msg in messages:
            full_msg = self.service.users().messages().get(
                userId="me",
                id=msg["id"],
                format="metadata",
                metadataHeaders=["Subject", "From"],
            ).execute()

            headers = full_msg["payload"]["headers"]

            subject = ""
            sender = ""

            for h in headers:
                if h["name"] == "Subject":
                    subject = h["value"]
                if h["name"] == "From":
                    sender = h["value"]

            snippet = full_msg.get("snippet", "")

            emails.append(
                {
                    "id": msg["id"],
                    "from": sender,
                    "subject": subject,
                    "snippet": snippet,
                }
            )

        return emails

    def archive_message(self, message_id: str):
        modify_creds = Credentials.from_authorized_user_file(
            settings.gmail_modify_token_path
        )
        modify_service = build("gmail", "v1", credentials=modify_creds)

        modify_service.users().messages().modify(
            userId="me",
            id=message_id,
            body={"removeLabelIds": ["INBOX"]},
        ).execute()