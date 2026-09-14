from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, ValidationError, model_validator


class ContactType(str, Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: str | None = Field(default=None, max_length=500)
    is_verified: bool = False

    @model_validator(mode="after")
    def validate_event_constraints(self) -> "AlienContact":
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact ID must start with 'AC'")
        if self.contact_type == ContactType.PHYSICAL and not self.is_verified:
            raise ValueError("Physical contacts must be verified")
        if (
            self.contact_type == ContactType.TELEPATHIC
            and self.witness_count < 3
        ):
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses"
            )
        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError("Strong signals must include a received message")
        return self


def create_contact(data: dict[str, Any]) -> AlienContact | None:
    """Validate incoming contact data and return a contact model."""
    try:
        return AlienContact(**data)
    except ValidationError as exc:
        print("======================================")
        print("Expected validation error:")
        for err in exc.errors():
            print(err["msg"])
        return None


def report(alien_c: AlienContact) -> None:
    print("Alien Contact Log Validation")
    print("======================================")
    print("Valid contact report:")
    print(f"ID: {alien_c.contact_id}")
    print(f"Type: {alien_c.contact_type.value}")
    print(f"Location: {alien_c.location}")
    print(f"Signal: {alien_c.signal_strength}/10")
    print(f"Duration: {alien_c.duration_minutes} minutes")
    print(f"Witnesses: {alien_c.witness_count}")
    if alien_c.message_received:
        print(f"Message: '{alien_c.message_received}'")


if __name__ == "__main__":
    contact_data = {
        "contact_id": "AC_2024_001",
        "timestamp": datetime(2024, 1, 1, 10, 0, 0),
        "contact_type": ContactType.RADIO,
        "location": "Area 51, Nevada",
        "signal_strength": 8.5,
        "duration_minutes": 45,
        "witness_count": 5,
        "message_received": "Greetings from Zeta Reticuli",
    }
    ok_contact = create_contact(contact_data)
    if isinstance(ok_contact, AlienContact):
        report(ok_contact)

    failed_contact = {
        "contact_id": "AC_2013_002",
        "timestamp": datetime(2024, 1, 1, 10, 0, 0),
        "contact_type": ContactType.TELEPATHIC,
        "location": "Area 51, Nevada",
        "signal_strength": 8.5,
        "duration_minutes": 45,
        "witness_count": 1,
        "message_received": "Greetings from Nevermore",
    }
    ko_contact = create_contact(failed_contact)
    if isinstance(ko_contact, AlienContact):
        report(ko_contact)
