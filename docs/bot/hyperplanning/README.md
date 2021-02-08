# Hyperplanning command

Shows a list of available classrooms according to the specified filters.

## Usage

- Available classrooms right now:
```
!hyperplanning 
```

- Available classrooms at a specified [location](../../locations/README.md):
```
!hyperplanning location=Templiers
```

- Available classrooms on a specified date:
```
!hyperplanning date="01/01/1970 00h00"
```

- Available classrooms for at least a specified duration:
```
!hyperplanning duration=5h
```

- And so much more !

## Arguments

| Name           | Type   | Default          | Description                                             |
|----------------|--------|------------------|---------------------------------------------------------|
| all            | `bool` | `False`          | Shows all classrooms.                                   |
| available      | `bool` | `True`           | Filters classrooms by availability.                     |
| date           | `str`  | `datetime.now()` | Filters classrooms by availability at a specified date. |
| duration       | `str`  | `None`           | Filters classrooms by minimum availability duration.    |
| name           | `str`  | `None`           | Filters classrooms by name.                             |
| floor          | `int`  | `None`           | Filters classrooms by floor.                            |
| sub_building   | `str`  | `None`           | Filters classrooms by [sub-building](../../locations/README.md).                     |
| building       | `str`  | `None`           | Filters classrooms by [building](../../locations/README.md).                         |
| location       | `str`  | `None`           | Filters classrooms by [location](../../locations/README.md).                         |
| places         | `int`  | `None`           | Filters classrooms by minimum number of places.         |
| outlets        | `int`  | `None`           | Filters classrooms by minimum number of outlets.        |
| computers      | `int`  | `None`           | Filters classrooms by minimum number of computers.      |
| projector      | `bool` | `None`           | Filters classrooms by projector availability.           |
| audio          | `bool` | `None`           | Filters classrooms by audio system availability.        |
| reload         | `bool` | `True`           | Forces the reloading of schedules.                      |
| verbose        | `int`  | `0`              | Enables a more detailed output (from 0 to 2).           |
