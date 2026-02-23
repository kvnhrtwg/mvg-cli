import json
import time as time_mod

import typer
from rich.console import Console
from rich.live import Live

from mvg_cli import favorites
from mvg_cli.api import find_station, get_departures, get_routes, parse_time
from mvg_cli.display import (
    build_departures_table,
    build_routes_table,
    format_departures,
    format_routes,
    print_departures,
    print_routes,
)

app = typer.Typer(add_completion=False, context_settings={"help_option_names": ["-h", "--help"]})


@app.command()
def main(
    args: list[str] = typer.Argument(None, help="Arguments for --save: <alias> <station>"),
    station: str | None = typer.Option(None, "-f", "--from", help="Origin station name or favorite"),
    to: str | None = typer.Option(None, "-t", "--to", help="Destination station name or favorite"),
    only: str | None = typer.Option(None, "--only", help="Filter transport types (e.g. ubahn, bus, sbahn,tram)"),
    time: str | None = typer.Option(None, "--time", help="Departure time in HH:mm format (e.g. 23:12)"),
    speed: str | None = typer.Option(None, "--speed", help="Walking speed for routes: slow, normal, fast"),
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON instead of a table"),
    live: bool = typer.Option(False, "--live", help="Auto-refresh every 10 seconds"),
    save: bool = typer.Option(False, "--save", help="Save a favorite: --save <alias> <station>"),
    delete: str | None = typer.Option(None, "--delete", help="Delete a favorite by alias"),
    list_favorites: bool = typer.Option(False, "--favorites", help="List all saved favorites"),
) -> None:
    """Show next departures or routes from Munich public transport stations."""
    console = Console()

    if live and json_output:
        raise SystemExit("--live and --json cannot be used together.")

    if list_favorites:
        favs = favorites.load()
        if not favs:
            console.print("No favorites saved yet. Use --save <alias> <station> to add one.")
        else:
            for alias, station_name in favs.items():
                console.print(f"  {alias} → {station_name}")
        return

    if delete:
        favs = favorites.load()
        if delete not in favs:
            raise SystemExit(f"Favorite '{delete}' not found.")
        del favs[delete]
        favorites.save(favs)
        console.print(f"Deleted favorite '{delete}'.")
        return

    if save:
        if not args or len(args) < 2:
            raise SystemExit("Usage: mvg --save <alias> <station>")
        alias = args[0]
        station_name = " ".join(args[1:])
        find_station(station_name)  # validate station exists
        favs = favorites.load()
        favs[alias] = station_name
        favorites.save(favs)
        console.print(f"Saved favorite '{alias}' → {station_name}")
        return

    if not station:
        raise SystemExit("Missing required option: -f / --from")

    departure_time = parse_time(time) if time else None

    station = favorites.resolve(station)
    origin = find_station(station)

    if to:
        to = favorites.resolve(to)
        dest = find_station(to)

    def fetch_table():
        if to:
            routes = get_routes(origin["globalId"], dest["globalId"], transport_types=only, time=departure_time, speed=speed)
            return build_routes_table(routes, origin["name"], dest["name"])
        else:
            deps = get_departures(origin["globalId"], transport_types=only, time=departure_time)
            return build_departures_table(deps, origin["name"])

    if live:
        try:
            console.clear()
            with Live(fetch_table(), console=console, refresh_per_second=1) as live_display:
                while True:
                    time_mod.sleep(10)
                    live_display.update(fetch_table())
        except KeyboardInterrupt:
            pass
    elif to:
        routes = get_routes(origin["globalId"], dest["globalId"], transport_types=only, time=departure_time, speed=speed)
        if json_output:
            print(json.dumps(format_routes(routes), indent=2, ensure_ascii=False))
        else:
            print_routes(routes, origin["name"], dest["name"])
    else:
        deps = get_departures(origin["globalId"], transport_types=only, time=departure_time)
        if json_output:
            print(json.dumps(format_departures(deps), indent=2, ensure_ascii=False))
        else:
            print_departures(deps, origin["name"])


if __name__ == "__main__":
    app()
