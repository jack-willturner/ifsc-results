from dataclasses import dataclass


@dataclass
class AthleteScore:
    athlete_id: int
    athlete_firstname: str
    athlete_lastname: str

    tops: int
    zones: int
    top_attempts: int
    zone_attempts: int
