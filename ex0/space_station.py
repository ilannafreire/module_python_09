from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, ValidationError


class SpaceStation(BaseModel):
    """Validated model for a space station monitoring record."""

    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: str | None = Field(default=None, max_length=200)


def create_station(data: dict[str, Any]) -> SpaceStation | None:
    """Create a valid station or print the validation error."""
    try:
        return SpaceStation(**data)
    except ValidationError as exc:
        print("========================================")
        print("Expected validation error:")
        for err in exc.errors():
            print(err["msg"])
        return None


def report(station: SpaceStation) -> None:
    """Display a station validation result in the terminal."""
    print("Space Station Data Validation")
    print("========================================")
    print("Valid station created:")
    print(f"ID: {station.station_id}")
    print(f"Name: {station.name}")
    print(f"Crew: {station.crew_size} people")
    print(f"Power: {station.power_level}%")
    print(f"Oxygen: {station.oxygen_level}%")
    status = "Operational" if station.is_operational else "Not operational"
    print(f"Status: {status}")


def main() -> None:
    """Run a valid example and a failed validation case."""
    valid_station_data = {
        "station_id": "ISS001",
        "name": "International Space Station",
        "crew_size": 6,
        "power_level": 85.5,
        "last_maintenance": datetime(2024, 1, 1, 10, 0, 0),
        "oxygen_level": 92.3,
        "is_operational": True,
    }
    valid_station = create_station(valid_station_data)
    if valid_station is not None:
        report(valid_station)

    failed_station_data = {
        "station_id": "ISS001",
        "name": "International Space Station",
        "crew_size": 25,
        "power_level": 85.5,
        "last_maintenance": datetime(2024, 1, 1, 10, 0, 0),
        "oxygen_level": 92.3,
        "is_operational": True,
    }
    invalid_station = create_station(failed_station_data)
    if invalid_station is not None:
        report(invalid_station)


if __name__ == "__main__":
    main()
