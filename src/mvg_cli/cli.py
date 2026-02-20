import typer
from rich.console import Console

from mvg_cli import favorites
from mvg_cli.api import find_station, get_departures, get_routes
from mvg_cli.display import print_departures, print_routes

app = typer.Typer(add_completion=False)


@app.command()
def main(
    args: list[str] = typer.Argument(None, help="Arguments for --save: <alias> <station>"),
    station: str | None = typer.Option(None, "-f", "--from", help="Origin station name or favorite"),
    to: str | None = typer.Option(None, "-t", "--to", help="Destination station name or favorite"),
    only: str | None = typer.Option(None, "--only", help="Filter transport types (e.g. ubahn, bus, sbahn,tram)"),
    save: bool = typer.Option(False, "--save", help="Save a favorite: --save <alias> <station>"),
    delete: str | None = typer.Option(None, "--delete", help="Delete a favorite by alias"),
    list_favorites: bool = typer.Option(False, "--favorites", help="List all saved favorites"),
) -> None:
    """Show next departures or routes from Munich public transport stations."""
    console = Console()

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

    station = favorites.resolve(station)
    origin = find_station(station)

    if to:
        to = favorites.resolve(to)
        dest = find_station(to)
        routes = get_routes(origin["globalId"], dest["globalId"])
        print_routes(routes, origin["name"], dest["name"])
    else:
        deps = get_departures(origin["globalId"], transport_types=only)
        print_departures(deps, origin["name"])


if __name__ == "__main__":
    app()
