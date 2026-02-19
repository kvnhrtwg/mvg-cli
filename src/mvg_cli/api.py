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


def get_departures(global_id: str, limit: int = 10, transport_types: str | None = None) -> list[dict]:
    response = httpx.get(
        f"{BASE_URL}/departures",
        params={
            "globalId": global_id,
            "limit": limit,
            "transportTypes": resolve_transport_types(transport_types),
        },
    )
    response.raise_for_status()
    return response.json()


ROUTE_TRANSPORT_TYPES = "SCHIFF,UBAHN,TRAM,SBAHN,BUS,REGIONAL_BUS,BAHN"


def get_routes(origin_id: str, destination_id: str) -> list[dict]:
    from datetime import datetime, timezone

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    response = httpx.get(
        f"{BASE_URL}/routes",
        params={
            "originStationGlobalId": origin_id,
            "destinationStationGlobalId": destination_id,
            "routingDateTime": now,
            "routingDateTimeIsArrival": "false",
            "transportTypes": ROUTE_TRANSPORT_TYPES,
            "changeSpeed": "NORMAL",
            "routeType": "LEAST_TIME",
        },
    )
    response.raise_for_status()
    return response.json()
