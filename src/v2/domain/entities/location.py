from dataclasses import dataclass


@dataclass(repr=False)
class Location:
    name: str
    latitude: float
    longitude: float

    def __repr__(self) -> str:
        return f"lat/long={self.latitude:.4}/{self.longitude:.4}"
