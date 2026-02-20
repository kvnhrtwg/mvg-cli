import re
from datetime import datetime, timezone

import httpx

BASE_URL = "https://www.mvg.de/api/bgw-pt/v3"
ALL_TRANSPORT_TYPES = ["UBAHN", "TRAM", "SBAHN", "BUS", "REGIONAL_BUS", "BAHN"]

TRANSPORT_TYPE_ALIASES = {
    "ubahn": ["UBAHN"],
    "u": ["UBAHN"],
    "sbahn": ["SBAHN"],
    "s": ["SBAHN"],
    "tram": ["TRAM"],
    "bus": ["BUS", "REGIONAL_BUS"],
    "bahn": ["BAHN"],
}


def resolve_transport_types(only: str | None) -> str:
    if not only:
        return ",".join(ALL_TRANSPORT_TYPES)
    types: set[str] = set()
    for token in only.lower().split(","):
        token = token.strip()
        if token in TRANSPORT_TYPE_ALIASES:
            types.update(TRANSPORT_TYPE_ALIASES[token])
        else:
            raise SystemExit(
                f"Unknown transport type '{token}'. "
                f"Valid types: {', '.join(TRANSPORT_TYPE_ALIASES)}"
            )
    return ",".join(types)


def parse_time(value: str) -> datetime:
    if not re.match(r"^\d{1,2}:\d{2}$", value):
        raise SystemExit("Invalid time format. Use HH:mm (e.g. 23:12).")
    hours, minutes = value.split(":")
    hours, minutes = int(hours), int(minutes)
    if hours > 23 or minutes > 59:
        raise SystemExit("Invalid time. Hours must be 0-23, minutes 0-59.")
    now = datetime.now().astimezone()
    return now.replace(hour=hours, minute=minutes, second=0, microsecond=0)


def find_station(name: str) -> dict:
    response = httpx.get(
        f"{BASE_URL}/locations",
        params={"query": name, "locationTypes": "STATION"},
    )
    response.raise_for_status()
    stations = response.json()

    for station in stations:
        if station["name"].lower() == name.lower():
            return station

    raise SystemExit(f"Station '{name}' not found. Did you mean one of these?\n"
                     + "\n".join(f"  - {s['name']}" for s in stations[:5]))


def get_departures(
    global_id: str,
    limit: int = 10,
    transport_types: str | None = None,
    time: datetime | None = None,
) -> list[dict]:
    params = {
        "globalId": global_id,
        "limit": limit,
        "transportTypes": resolve_transport_types(transport_types),
    }
    if time:
        offset = int((time - datetime.now().astimezone()).total_seconds() / 60)
        if offset > 0:
            params["offsetInMinutes"] = offset
    response = httpx.get(f"{BASE_URL}/departures", params=params)
    response.raise_for_status()
    return response.json()



VALID_SPEEDS = {"slow": "SLOW", "normal": "NORMAL", "fast": "FAST"}


def resolve_speed(speed: str | None) -> str:
    if not speed:
        return "NORMAL"
    key = speed.lower().strip()
    if key not in VALID_SPEEDS:
        raise SystemExit(
            f"Unknown speed '{speed}'. Valid options: slow, normal, fast"
        )
    return VALID_SPEEDS[key]


def get_routes(
    origin_id: str,
    destination_id: str,
    transport_types: str | None = None,
    time: datetime | None = None,
    speed: str | None = None,
) -> list[dict]:
    routing_time = (time or datetime.now()).astimezone(timezone.utc)
    routing_dt = routing_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    response = httpx.get(
        f"{BASE_URL}/routes",
        params={
            "originStationGlobalId": origin_id,
            "destinationStationGlobalId": destination_id,
            "routingDateTime": routing_dt,
            "routingDateTimeIsArrival": "false",
            "transportTypes": resolve_transport_types(transport_types),
            "changeSpeed": resolve_speed(speed),
            "routeType": "LEAST_TIME",
        },
    )
    response.raise_for_status()
    return response.json()
