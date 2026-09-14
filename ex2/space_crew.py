from datetime import datetime
from enum import Enum
from math import ceil
from typing import Any

from pydantic import BaseModel, Field, ValidationError, model_validator


class Rank(str, Enum):
    """Supported crew ranks."""

    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    """Single crew member information."""

    member_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=2, max_length=50)
    rank: Rank
    age: int = Field(..., ge=18, le=80)
    specialization: str = Field(..., min_length=3, max_length=30)
    years_experience: int = Field(..., ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    """Mission configuration with a nested crew list."""

    mission_id: str = Field(..., min_length=5, max_length=15)
    mission_name: str = Field(..., min_length=3, max_length=100)
    destination: str = Field(..., min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(..., ge=1, le=3650)
    crew: list[CrewMember] = Field(..., min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(..., ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def validate_mission_rules(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")

        has_leadership = any(
            member.rank in {Rank.CAPTAIN, Rank.COMMANDER}
            for member in self.crew
        )
        if not has_leadership:
            raise ValueError(
                "Mission must have at least one Commander or Captain"
            )

        if self.duration_days > 365:
            required_experienced = ceil(len(self.crew) * 0.5)
            experienced_count = sum(
                1 for member in self.crew if member.years_experience >= 5
            )
            if experienced_count < required_experienced:
                raise ValueError(
                    "Long missions (> 365 days) need 50% experienced crew "
                    "(5+ years)"
                )

        if any(not member.is_active for member in self.crew):
            raise ValueError("All crew members must be active")

        return self


def create_mission(data: dict[str, Any]) -> SpaceMission | None:
    """Create a valid mission or print the validation error."""
    try:
        return SpaceMission(**data)
    except ValidationError as exc:
        print("=========================================")
        print("Expected validation error:")
        for err in exc.errors():
            print(err["msg"])
        return None


def report(space_m: SpaceMission) -> None:
    """Display a mission validation result in the terminal."""
    print("Space Mission Crew Validation")
    print("=========================================")
    print("Valid mission created:")
    print(f"Mission: {space_m.mission_name}")
    print(f"ID: {space_m.mission_id}")
    print(f"Destination: {space_m.destination}")
    print(f"Duration: {space_m.duration_days} days")
    print(f"Budget: ${space_m.budget_millions}M")
    print(f"Crew size: {len(space_m.crew)}")
    print("Crew members:")
    for member in space_m.crew:
        print(
            f"- {member.name} ({member.rank.value}) - "
            f"{member.specialization}"
        )


def main() -> None:
    """Run a valid example and a failed validation case."""
    valid_mission_data = {
        "mission_id": "M2024_MARS",
        "mission_name": "Mars Colony Establishment",
        "destination": "Mars",
        "launch_date": datetime(2024, 1, 1, 10, 0, 0),
        "duration_days": 900,
        "budget_millions": 2500.0,
        "crew": [
            {
                "member_id": "CM001",
                "name": "Sarah Connor",
                "rank": Rank.COMMANDER,
                "age": 48,
                "specialization": "Mission Command",
                "years_experience": 18,
                "is_active": True,
            },
            {
                "member_id": "CM002",
                "name": "John Smith",
                "rank": Rank.LIEUTENANT,
                "age": 34,
                "specialization": "Navigation",
                "years_experience": 9,
                "is_active": True,
            },
            {
                "member_id": "CM003",
                "name": "Alice Johnson",
                "rank": Rank.OFFICER,
                "age": 29,
                "specialization": "Engineering",
                "years_experience": 7,
                "is_active": True,
            },
        ],
    }
    valid_mission = create_mission(valid_mission_data)
    if valid_mission is not None:
        report(valid_mission)

    failed_mission_data = {
        "mission_id": "M2024_FAIL",
        "mission_name": "Mars Colony Establishment",
        "destination": "Mars",
        "launch_date": datetime(2024, 1, 1, 10, 0, 0),
        "duration_days": 900,
        "budget_millions": 2500.0,
        "crew": [
            {
                "member_id": "CM004",
                "name": "John Smith",
                "rank": Rank.LIEUTENANT,
                "age": 35,
                "specialization": "Navigation",
                "years_experience": 10,
                "is_active": True,
            },
            {
                "member_id": "CM005",
                "name": "Alice Johnson",
                "rank": Rank.OFFICER,
                "age": 30,
                "specialization": "Engineering",
                "years_experience": 8,
                "is_active": True,
            },
        ],
    }
    invalid_mission = create_mission(failed_mission_data)
    if invalid_mission is not None:
        report(invalid_mission)


if __name__ == "__main__":
    main()
