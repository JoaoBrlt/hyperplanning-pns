# Hyperplanning command

Shows a list of available classrooms according to the specified filters.

## Usage

1. Available classrooms right now:
```
!hyperplanning 
```

2. Available classrooms at a specified location:
```
!hyperplanning location=Templiers
```

3. Available classrooms on a specified date:
```
!hyperplanning date="01/01/1970 00h00"
```

4. Available classrooms for at least a specified duration:
```
!hyperplanning duration=5h
```

## Arguments

| Name           | Type   | Default          | Description                                             |
|----------------|--------|------------------|---------------------------------------------------------|
| all            | `bool` | `False`          | Shows all classrooms.                                   |
| available      | `bool` | `True`           | Filters classrooms by availability.                     |
| date           | `str`  | `datetime.now()` | Filters classrooms by availability at a specified date. |
| duration       | `str`  | `None`           | Filters classrooms by minimum availability duration.    |
| name           | `str`  | `None`           | Filters classrooms by name.                             |
| floor          | `int`  | `None`           | Filters classrooms by floor.                            |
| sub_building   | `str`  | `None`           | Filters classrooms by sub-building.                     |
| building       | `str`  | `None`           | Filters classrooms by building.                         |
| location       | `str`  | `None`           | Filters classrooms by location.                         |
| places         | `int`  | `None`           | Filters classrooms by minimum number of places.         |
| outlets        | `int`  | `None`           | Filters classrooms by minimum number of outlets.        |
| computers      | `int`  | `None`           | Filters classrooms by minimum number of computers.      |
| projector      | `bool` | `None`           | Filters classrooms by projector availability.           |
| audio          | `bool` | `None`           | Filters classrooms by audio system availability.        |
| reload         | `bool` | `True`           | Forces the reloading of schedules.                      |
| verbose        | `int`  | `0`              | Enables a more detailed output (from 0 to 2).           |
