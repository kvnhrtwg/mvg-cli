# mvg-cli

A command-line tool for Munich public transport (MVG) departures and route planning.

## Installation

```bash
pipx install -e .
```

## Usage

### Departures

Show next departures from a station:

```bash
mvg -f Garching
```

```
                       Departures from Garching
┏━━━━━━━━┳━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┓
┃     In ┃ Departure ┃ Line ┃ Destination                     ┃ Delay ┃
┡━━━━━━━━╇━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━┩
│  3 min │   19:52   │ U6   │ Klinikum Großhadern             │    +1 │
│  5 min │   19:54   │ 292  │ Oberschleißheim, Sonnenstraße   │       │
│  5 min │   19:54   │ 230  │ Haar (S)                        │       │
│  ...   │           │      │                                 │       │
└────────┴───────────┴──────┴─────────────────────────────────┴───────┘
```

Station names with spaces need quotes:

```bash
mvg -f "Münchner Freiheit"
```

### Routes

Plan a route with `-t`:

```bash
mvg -f Garching -t Marienplatz
```

```
            Routes from Garching to Marienplatz
┏━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━┓
┃     In ┃ Departure ┃ Arrival ┃ Duration ┃ Lines        ┃ Delay ┃
┡━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━┩
│  5 min │   19:49   │  20:11  │   22 min │ U6           │    +2 │
│ 12 min │   19:56   │  20:18  │   22 min │ U6           │       │
│  ...   │           │         │          │              │       │
└────────┴───────────┴─────────┴──────────┴──────────────┴───────┘
```

### Filter by transport type

Use `--only` to filter departures by transport type:

```bash
mvg -f Garching --only ubahn
mvg -f Garching --only ubahn,bus
mvg -f "Münchner Freiheit" --only tram
```

Available filters: `ubahn` / `u`, `sbahn` / `s`, `tram`, `bus`, `bahn`

### Favorites

Save stations under custom aliases:

```bash
mvg --save home Garching
mvg --save office Marienplatz
mvg --save benny "Münchner Freiheit"
```

Then use them anywhere instead of station names:

```bash
mvg -f home
mvg -f home -t office
mvg -f home --only ubahn
```

List all favorites:

```bash
mvg --favorites
```

Delete a favorite:

```bash
mvg --delete home
```

Favorites are stored in `~/.config/mvg-cli/favorites.json`.

## Options

| Option        | Short | Description                                |
|---------------|-------|--------------------------------------------|
| `--from`      | `-f`  | Origin station name or favorite            |
| `--to`        | `-t`  | Destination station (enables routes)       |
| `--only`      |       | Filter by transport type                   |
| `--save`      |       | Save a favorite: `--save <alias> <station>`|
| `--delete`    |       | Delete a favorite by alias                 |
| `--favorites` |       | List all saved favorites                   |
| `--help`      |       | Show help                                  |
