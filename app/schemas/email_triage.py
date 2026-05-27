from pydantic import BaseModel, Field


class EmailInput(BaseModel):
    id: str | None = None
    from_email: str
    subject: str
    snippet: str
    received_at: str | None = None


class EmailTriageResult(BaseModel):
    priority: str = Field(description="urgent | important | can_wait | ignore")
    reply_required: bool
    summary: str
    reason: str
