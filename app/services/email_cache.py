from typing import List, Tuple
from app.schemas.email_triage import EmailInput, EmailTriageResult


class EmailCache:
    def __init__(self):
        self._data: List[Tuple[EmailInput, EmailTriageResult]] = []

    def set(self, data: List[Tuple[EmailInput, EmailTriageResult]]):
        self._data = data

    def get(self) -> List[Tuple[EmailInput, EmailTriageResult]]:
        return self._data


email_cache = EmailCache()
