import pygame
import random
from enum import Enum, auto
from system.constants import Main, Floor as fl, ColorPalette as cp
from game.tile import TileConfiguration, Tile
import math


class FloorManager:
    def __init__(self, surface: pygame.Surface, grid_constant: int):
        self.surface: pygame.Surface = surface
        self.grid_constant: int = grid_constant

        self.floor_config: FloorConfiguration = FloorConfiguration(
            surface=self.surface, grid_constant=self.grid_constant
        )

        self.first_floor: Floor = Floor(
            surface=self.surface, path=self.floor_config.generate_path(), grid_constant=self.grid_constant
        )
        self.floors: list[Floor] = [self.first_floor]

        self.floor_margin: int = self.grid_constant

    def update(self, camera_offset: tuple[float, float]):
        for floor in self.floors:
            floor.update(camera_offset=camera_offset)

    def draw(self):
        for floor in self.floors:
            floor.draw()


class FloorConfiguration:
    def __init__(self, surface: pygame.Surface, grid_constant: int, rows: int = 4, columns: int = 4) -> None:
        self.surface: pygame.Surface = surface
        self.grid_constant: int = grid_constant
        self.rows: int = rows
        self.cols: int = columns

        self.movement_dict: dict[Direction, tuple[int, int]] = {
            Direction.SOUTH: (1, 0),
            Direction.NORTH: (-1, 0),
            Direction.WEST: (0, -1),
            Direction.EAST: (0, 1),
        }

        self.door_connections_dict: dict[Direction, Direction] = {
            Direction.SOUTH: Direction.NORTH,
            Direction.NORTH: Direction.SOUTH,
            Direction.WEST: Direction.EAST,
            Direction.EAST: Direction.WEST,
        }

    def select_entrance_exit(self) -> tuple[int, int, int, int]:
        entrance_row: int = 0
        entrance_col: int = 0
        exit_row: int = self.rows - 1
        exit_col: int = self.cols - 1  # temp placeholders

        return entrance_row, entrance_col, exit_row, exit_col

    def get_valid_directions(self, current_row: int, current_col: int) -> list[Direction]:
        valid: list[Direction] = []
        row: int = current_row
        col: int = current_col

        if row - 1 >= 0:
            valid.append(Direction.NORTH)

        if row + 1 < self.rows:
            valid.append(Direction.SOUTH)

        if col - 1 >= 0:
            valid.append(Direction.WEST)

        if col + 1 < self.cols:
            valid.append(Direction.EAST)

        return valid

    # TODO in the future, make generate_path retrace it's steps if it has no empty rooms to go to next.
    # Maybe convert to BSP generation later (if you have more time than you bargained for)
    def generate_path(self) -> dict[tuple[int, int], Room]:
        room_dict: dict[tuple[int, int], Room] = {}
        ent_row, ent_col, ex_row, ex_col = self.select_entrance_exit()

        entrance_room: Room = Room(
            surface=self.surface,
            grid_constant=self.grid_constant,
            row=ent_row,
            col=ent_col,
            room_type=RoomType.ENTRANCE,
        )
        exit_room: Room = Room(
            surface=self.surface, grid_constant=self.grid_constant, row=ex_row, col=ex_col, room_type=RoomType.EXIT
        )

        room_dict[entrance_room.get_loc()] = entrance_room

        current_row: int = ent_row
        current_col: int = ent_col

        calculating: bool = True
        while calculating:
            valid_dirs: list[Direction] = self.get_valid_directions(current_row=current_row, current_col=current_col)
            random_dir: Direction = random.choice(valid_dirs)
            move_dir: tuple[int, int] = self.movement_dict[random_dir]

            next_row: int = current_row + move_dir[0]
            next_col: int = current_col + move_dir[1]

            current_room: Room = room_dict[(current_row, current_col)]
            current_room.add_door(door=random_dir)

            if (next_row, next_col) not in room_dict:
                if (next_row, next_col) == (ex_row, ex_col):
                    exit_room.add_door(door=self.door_connections_dict[random_dir])

                    calculating = False
                    continue

                new_room: Room = Room(
                    surface=self.surface,
                    grid_constant=self.grid_constant,
                    row=next_row,
                    col=next_col,
                    room_type=RoomType.NORMAL,
                )
                new_room.add_door(door=self.door_connections_dict[random_dir])

                room_dict[(next_row, next_col)] = new_room

            else:
                next_room: Room = room_dict[(next_row, next_col)]
                next_room.add_door(door=self.door_connections_dict[random_dir])

            # move pointer
            current_row = next_row
            current_col = next_col

        room_dict[exit_room.get_loc()] = exit_room
        return room_dict


class Floor:
    def __init__(self, surface: pygame.Surface, path: dict[tuple[int, int], Room], grid_constant: int) -> None:
        self.surface: pygame.Surface = surface
        self.path: dict[tuple[int, int], Room] = path
        self.grid_constant: int = grid_constant

    def update(self, camera_offset: tuple[float, float]):
        for room in self.path.values():
            room.update(camera_offset=camera_offset)

    def draw(self):
        for room in self.path.values():
            room.draw(surface=self.surface)


class RoomType(Enum):
    ENTRANCE = auto()
    NORMAL = auto()
    ENEMY = auto()
    PUZZLE = auto()
    EXIT = auto()


class Direction(Enum):
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()


class Room:
    def __init__(
        self, surface: pygame.Surface, grid_constant: int, row: int, col: int, room_type: RoomType = RoomType.NORMAL
    ) -> None:
        self.surface: pygame.Surface = surface
        self.grid_constant: int = grid_constant
        self.row: int = row
        self.col: int = col
        self.room_type: RoomType = room_type

        self.tile_config: TileConfiguration = TileConfiguration(surface=self.surface, grid_constant=self.grid_constant)

        self.enabled: bool = True
        self.doors: set[Direction] = set()

        self.width: int = self.grid_constant * fl.ROOM_UNIT_SIZE
        self.height: int = self.grid_constant * fl.ROOM_UNIT_SIZE
        self.margin: int = self.grid_constant
        self.start_x: int = self.col * (self.margin + self.width)
        self.start_y: int = self.row * (self.margin + self.height)

        self.door_pos_dict: dict[Direction, tuple[int, int]] = {
            Direction.SOUTH: (1, 2),
            Direction.NORTH: (1, 0),
            Direction.WEST: (0, 1),
            Direction.EAST: (2, 1),
        }

        self.tile_map: list[Tile] = self.set_tiles()
        self.door_map: list[Tile] = []

    def add_door(self, door: Direction):
        self.doors.add(door)
        self.door_map = self.set_doors()

    def get_loc(self) -> tuple[int, int]:
        return self.row, self.col

    def set_tiles(self) -> list[Tile]:
        tiles: list[Tile] = []
        for row in range(fl.ROOM_UNIT_SIZE):
            for col in range(fl.ROOM_UNIT_SIZE):
                x: int = col * self.grid_constant + self.start_x
                y: int = row * self.grid_constant + self.start_y
                tiles.append(self.tile_config.create_tile(x=x, y=y, color=cp.DARK_GREEN))

        return tiles

    def set_doors(self) -> list[Tile]:
        base_x: int = self.width // 2
        base_y: int = self.height // 2

        doors: list[Tile] = []
        for door in self.doors:
            converted_x: int = self.start_x + base_x * self.door_pos_dict[door][0]
            converted_y: int = self.start_y + base_y * self.door_pos_dict[door][1]
            doors.append(self.tile_config.create_tile(x=converted_x, y=converted_y, color=cp.GRAY))

        return doors

    def update(self, camera_offset: tuple[float, float]):
        for tile in self.tile_map + self.door_map:
            tile.x_pos += camera_offset[0]
            tile.y_pos += camera_offset[1]

    def draw(self, surface: pygame.Surface):
        for tile in self.tile_map + self.door_map:
            tile.draw()
