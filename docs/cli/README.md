# Command-line interface

Use the application through a terminal.

## Requirements

1. Install Python 3 and pip.
2. Clone the repository.
3. Move to the repository.
4. Install the dependencies.
```bash
pip install -r requirements.txt
```

## Usage

1. Available classrooms right now:
```bash
python cli.py
```

2. Available classrooms at a specified location:
```bash
python cli.py -l Templiers
```

3. Available classrooms on a specified date:
```bash
python cli.py -d "01/01/1970 00h00"
```

4. Available classrooms for at least a specified duration:
```bash
python cli.py -t 5h
```

## Arguments

| Name                                             | Type   | Default               | Description                                            |
|--------------------------------------------------|--------|-----------------------|--------------------------------------------------------|
| `--all`                                          | `bool` | `all=False`           | Show all classrooms.                                   |
| `-a`, `--available`                              | `bool` | `available=True`      | Show available classrooms only.                        |
| `-u`, `--unavailable`                            | `bool` | `available=True`      | Show unavailable classrooms only.                      |
| `-d DATE`, `--date DATE`                         | `str`  | `date=datetime.now()` | Filter classrooms by availability at a specified date. |
| `-t DURATION`, `--duration DURATION`             | `str`  | `duration=None`       | Filter classrooms by minimum availability duration.    |
| `-n NAME`, `--name NAME`                         | `str`  | `name=None`           | Filter classrooms by name.                             |
| `-f FLOOR`, `--floor FLOOR`                      | `int`  | `floor=None`          | Filter classrooms by floor.                            |
| `-s SUB_BUILDING`, `--sub-building SUB_BUILDING` | `str`  | `sub_building=None`   | Filter classrooms by sub-building.                     |
| `-b BUILDING`, `--building BUILDING`             | `str`  | `building=None`       | Filter classrooms by building.                         |
| `-l LOCATION`, `--location LOCATION`             | `str`  | `location=None`       | Filter classrooms by location.                         |
| `-p PLACES`, `--places PLACES`                   | `int`  | `places=None`         | Filter classrooms by minimum number of places.         |
| `-o OUTLETS`, `--outlets OUTLETS`                | `int`  | `outlets=None`        | Filter classrooms by minimum number of outlets.        |
| `-c COMPUTERS`, `--computers COMPUTERS`          | `int`  | `computers=None`      | Filter classrooms by minimum number of computers.      |
| `--projector`                                    | `bool` | `projector=None`      | Show classrooms with a projector.                      |
| `--no-projector`                                 | `bool` | `projector=None`      | Show classrooms without a projector.                   |
| `--audio`                                        | `bool` | `audio=None`          | Show classrooms with an audio system.                  |
| `--no-audio`                                     | `bool` | `audio=None`          | Show classrooms without an audio system.               |
| `--color`                                        | `bool` | `color=None`          | Enable the use of colors on the output.                |
| `--no-color`                                     | `bool` | `color=None`          | Disable the use of colors on the output.               |
| `--reload`                                       | `bool` | `reload=True`         | Force the reloading of schedules.                      |
| `--no-reload`                                    | `bool` | `reload=True`         | Disable the reloading of schedules.                    |
| `-v`, `--verbose`                                | `int`  | `verbose=0`           | Enable a more detailed output.                         |

## Preview

<img src="../preview/cli.png" width="500" alt="CLI preview"/>
<img src="../preview/cli2.png" width="500" alt="CLI preview 2"/>