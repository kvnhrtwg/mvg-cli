import typer

from mvg_cli.api import find_station, get_departures, get_routes
from mvg_cli.display import print_departures, print_routes

app = typer.Typer(add_completion=False)


@app.command()
def main(
    station: str = typer.Option(..., "-f", "--from", help="Origin station name"),
    to: str | None = typer.Option(None, "-t", "--to", help="Destination station name"),
    only: str | None = typer.Option(None, "--only", help="Filter transport types (e.g. ubahn, bus, sbahn,tram)"),
) -> None:
    """Show next departures or routes from Munich public transport stations."""
    origin = find_station(station)

    if to:
        dest = find_station(to)
        routes = get_routes(origin["globalId"], dest["globalId"])
        print_routes(routes, origin["name"], dest["name"])
    else:
        deps = get_departures(origin["globalId"], transport_types=only)
        print_departures(deps, origin["name"])


if __name__ == "__main__":
    app()
