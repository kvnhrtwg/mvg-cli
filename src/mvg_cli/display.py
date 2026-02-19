import time
from datetime import datetime

from rich.console import Console
from rich.table import Table

LINE_COLORS = {
    "UBAHN": "#007AD1",
    "SBAHN": "#008D4F",
    "TRAM": "#E30613",
    "BUS": "#0088A3",
    "REGIONAL_BUS": "#0088A3",
    "BAHN": "#ffffff",
}
DEFAULT_LINE_COLOR = "cyan"


def _color_line(label: str, transport_type: str) -> str:
    color = LINE_COLORS.get(transport_type, DEFAULT_LINE_COLOR)
    return f"[{color}]{label}[/{color}]"


def print_departures(departures: list[dict], station_name: str) -> None:
    console = Console()
    now_ms = int(time.time() * 1000)

    table = Table(title=f"Departures from {station_name}", show_header=True)
    table.add_column("In", justify="right", style="bold")
    table.add_column("Line")
    table.add_column("Destination")
    table.add_column("Delay", justify="right")

    for dep in departures[:10]:
        minutes = max(0, (dep["realtimeDepartureTime"] - now_ms) // 60_000)
        in_col = f"{minutes} min"

        label = _color_line(dep["label"], dep["transportType"])

        destination = dep["destination"]

        delay = dep.get("delayInMinutes", 0) or 0
        if delay > 0:
            delay_col = f"[red]+{delay}[/red]"
        elif delay < 0:
            delay_col = f"[green]{delay}[/green]"
        else:
            delay_col = ""

        style = "dim" if dep.get("cancelled") else None
        if dep.get("cancelled"):
            delay_col = "[red]cancelled[/red]"

        table.add_row(in_col, label, destination, delay_col, style=style)

    console.print(table)


def print_routes(routes: list[dict], origin: str, destination: str) -> None:
    console = Console()

    table = Table(title=f"Routes from {origin} to {destination}", show_header=True)
    table.add_column("In", justify="right", style="bold")
    table.add_column("Departure", justify="center")
    table.add_column("Arrival", justify="center")
    table.add_column("Duration", justify="right")
    table.add_column("Lines")

    for route in routes:
        parts = route["parts"]
        first_dep = parts[0]["from"]["plannedDeparture"]
        last_arr = parts[-1]["to"]["plannedDeparture"]

        dep_time = datetime.fromisoformat(first_dep)
        arr_time = datetime.fromisoformat(last_arr)
        duration = int((arr_time - dep_time).total_seconds() // 60)

        now = datetime.now(dep_time.tzinfo)
        in_minutes = max(0, int((dep_time - now).total_seconds() // 60))

        legs = []
        for part in parts:
            transport = part["line"]["transportType"]
            label = part["line"]["label"]
            if transport == "PEDESTRIAN":
                legs.append("[dim]walk[/dim]")
            else:
                legs.append(_color_line(label, transport))

        table.add_row(
            f"{in_minutes} min",
            f"{dep_time:%H:%M}",
            f"{arr_time:%H:%M}",
            f"{duration} min",
            " → ".join(legs),
        )

    console.print(table)
