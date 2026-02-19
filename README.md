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
┏━━━━━━━━┳━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┓
┃     In ┃ Line ┃ Destination                     ┃ Delay ┃
┡━━━━━━━━╇━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━┩
│  3 min │ U6   │ Klinikum Großhadern             │    +1 │
│  5 min │ 292  │ Oberschleißheim, Sonnenstraße   │       │
│  5 min │ 230  │ Haar (S)                        │       │
│  ...   │      │                                 │       │
└────────┴──────┴─────────────────────────────────┴───────┘
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
┏━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃     In ┃ Departure ┃ Arrival ┃ Duration ┃ Lines        ┃
┡━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│  5 min │   19:49   │  20:11  │   22 min │ U6           │
│ 12 min │   19:56   │  20:18  │   22 min │ U6           │
│  ...   │           │         │          │              │
└────────┴───────────┴─────────┴──────────┴──────────────┘
```

### Filter by transport type

Use `--only` to filter departures by transport type:

```bash
mvg -f Garching --only ubahn
mvg -f Garching --only ubahn,bus
mvg -f "Münchner Freiheit" --only tram
```

Available filters: `ubahn` / `u`, `sbahn` / `s`, `tram`, `bus`, `bahn`

## Options

| Option    | Short | Description                          |
|-----------|-------|--------------------------------------|
| `--from`  | `-f`  | Origin station name (required)       |
| `--to`    | `-t`  | Destination station (enables routes) |
| `--only`  |       | Filter by transport type             |
| `--help`  |       | Show help                            |
