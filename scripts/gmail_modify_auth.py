from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
]

flow = InstalledAppFlow.from_client_secrets_file(
    "app/credentials/credentials.json",
    SCOPES,
)

creds = flow.run_local_server(port=0)

with open("app/credentials/token_gmail_modify.json", "w", encoding="utf-8") as token_file:
    token_file.write(creds.to_json())

print("✅ token_gmail_modify.json created successfully")
print("SCOPES:", creds.scopes)