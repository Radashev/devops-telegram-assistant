import json

from app.bot.llm import call_llm
from app.schemas.email_triage import EmailInput, EmailTriageResult


class EmailTriageAgentService:
    async def triage_email(self, email: EmailInput) -> EmailTriageResult:
        prompt = self._build_prompt(email)
        raw_response = await call_llm(prompt)
        return self._parse_response(raw_response)

    async def triage_batch(
        self,
        emails: list[EmailInput],
    ) -> list[tuple[EmailInput, EmailTriageResult]]:
        results: list[tuple[EmailInput, EmailTriageResult]] = []

        for email in emails:
            result = await self.triage_email(email)

            sender = email.from_email.lower() if email.from_email else ""
            subject = email.subject.lower() if email.subject else ""
            snippet = email.snippet.lower() if email.snippet else ""
            summary = result.summary.lower() if result.summary else ""
            full_text = f"{subject} {snippet} {summary}"

            # 🎯 URGENT
            if "interview" in full_text:
                result.priority = "urgent"

            # 🎯 Job / career — top priority for you
            elif "pracuj" in sender:
                result.priority = "important"

            elif "epam" in sender:
                result.priority = "important"

            elif "linkedin" in sender and any(word in full_text for word in [
                "devops",
                "backend",
                "python",
                "cloud",
                "sre",
                "platform",
                "engineer",
            ]):
                result.priority = "important"

            # 🎯 Payments / orders / confirmations
            elif any(word in full_text for word in [
                "payment",
                "transaction",
                "top-up",
                "order",
                "confirmation",
                "invoice",
                "bill",
                "przelew",
                "przelewy24",
                "t-mobile",
            ]):
                result.priority = "important"

            # 🎯 Learning / growth
            elif any(word in full_text for word in [
                "real python",
                "python",
                "devops",
                "cloud",
                "learning",
                "course",
                "trial",
            ]):
                if result.priority == "ignore":
                    result.priority = "important"

            # 🎯 LinkedIn generic
            elif "linkedin" in sender:
                result.priority = "can_wait"

            results.append((email, result))

        return results

    def _build_prompt(self, email: EmailInput) -> str:
        received_at = email.received_at or "unknown"

        return f"""
You are an Email Triage Agent.

Your task is to analyze an email and classify it.

Categories:
- urgent: requires immediate attention or has a deadline
- important: relevant and requires attention, but not urgent
- can_wait: useful but not time-sensitive
- ignore: spam, ads, irrelevant emails

Also determine:
- reply_required: true or false

Rules:
- Be strict: most emails are NOT urgent
- Marketing emails = ignore
- Notifications without action = can_wait or ignore
- Work-related or personal important topics = important or urgent

Return ONLY valid JSON:

{{
  "priority": "urgent | important | can_wait | ignore",
  "reply_required": true,
  "summary": "short summary",
  "reason": "short reason"
}}

Email:
From: {email.from_email}
Subject: {email.subject}
Received at: {received_at}
Snippet: {email.snippet}
""".strip()

    def _parse_response(self, raw_response: str) -> EmailTriageResult:
        try:
            data = json.loads(raw_response)
            return EmailTriageResult(**data)
        except Exception as e:
            raise ValueError(f"Failed to parse LLM response: {e}") from e