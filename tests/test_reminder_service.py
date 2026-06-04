from datetime import date, datetime

import pytest

from app.services.reminder_service import ReminderService


class FakeReminderRepository:
    pass


class FakeReminder:
    def __init__(
        self,
        day_of_month=None,
        is_last_day=False,
        last_triggered_at=None,
    ):
        self.day_of_month = day_of_month
        self.is_last_day = is_last_day
        self.last_triggered_at = last_triggered_at


def test_reminder_is_due_on_specific_day():
    service = ReminderService(FakeReminderRepository())

    reminder = FakeReminder(day_of_month=9, is_last_day=False)

    assert service.is_due_today(reminder, date(2026, 5, 9)) is True
    assert service.is_due_today(reminder, date(2026, 5, 10)) is False


@pytest.mark.parametrize(
    "today, expected",
    [
        (date(2026, 2, 28), True),
        (date(2026, 2, 27), False),
        (date(2028, 2, 29), True),
        (date(2028, 2, 28), False),
        (date(2026, 4, 30), True),
        (date(2026, 4, 29), False),
        (date(2026, 5, 31), True),
        (date(2026, 5, 30), False),
    ],
)
def test_reminder_is_due_on_last_day_of_different_months(today, expected):
    service = ReminderService(FakeReminderRepository())

    reminder = FakeReminder(day_of_month=None, is_last_day=True)

    assert service.is_due_today(reminder, today) is expected


def test_reminder_was_triggered_today():
    service = ReminderService(FakeReminderRepository())

    reminder = FakeReminder(
        day_of_month=9,
        is_last_day=False,
        last_triggered_at=datetime(2026, 5, 9, 10, 0),
    )

    assert service.was_triggered_today(reminder, date(2026, 5, 9)) is True
    assert service.was_triggered_today(reminder, date(2026, 5, 10)) is False


def test_reminder_is_not_due_when_day_does_not_match():
    service = ReminderService(FakeReminderRepository())

    reminder = FakeReminder(day_of_month=15, is_last_day=False)

    assert service.is_due_today(reminder, date(2026, 5, 14)) is False
    assert service.is_due_today(reminder, date(2026, 5, 16)) is False