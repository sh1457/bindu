import sys
from pathlib import Path
from typing import Protocol

import pygame as pg


class Entity(Protocol):
    def render(self) -> None:
        ...


# class Actor(pg.Sprite):

class Tile(pg.sprite.Sprite):
    image: pg.Surface
    rect: pg.Rect
    position: pg.Vector2

    def __init__(self, path: Path, position: pg.Vector2):
        super().__init__()
        self.image = pg.image.load(path)
        self.rect = self.image.get_rect()
        self.position = position

    def render(self, surface: pg.Surface) -> None:
        surface.blit(self.image, (self.position.x, self.position.y))


class Map(pg.Surface):
    tile_map: dict[str, pg.Surface] = {}
    values: list[str] = []
    offset: pg.Vector2 = pg.Vector2(0, 0)

    def __init__(self, tile_map, values, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tile_map = tile_map
        self.values = values
        self.prerender()

    def prerender(self) -> None:
        width, height = self.get_size()
        for x, row in zip(range(0, width, 32), self.values):
            for y, col in zip(range(0, height, 32), row):
                tile = self.tile_map.get(col)
                if tile is None:
                    print(row, col, x, y)
                    raise ValueError("Bad tile")
                self.blit(tile, (x, y))

    def render(self, surface: pg.Surface) -> None:
        surface.blit(self, (self.offset.x, self.offset.y))

    def update(self, delta: pg.Vector2, game_size: pg.Vector2) -> None:
        width, height = self.get_size()
        max_x = width - game_size.x
        max_y = height - game_size.y
        new_x = self.offset.x + delta.x
        new_y = self.offset.y + delta.y

        if delta.x != 0 or delta.y != 0:
            print(delta, (max_x, max_y), (new_x, new_y))

        if 0 <= -new_x <= max_x:
            self.offset.x = new_x
        if 0 <= -new_y <= max_y:
            self.offset.y = new_y


class Game:
    screen_width: int = 800
    screen_height: int = 600
    entities: list[Entity] = []
    data_path: Path = Path.home() / "bin" / "pygame" / "data"

    def add_entity(self, entity: Entity) -> None:
        self.entities.append(entity)

    def render(self) -> None:
        for e in self.entities:
            e.render(surface=self.screen)

    def update(self, *args, **kwargs) -> None:
        for e in self.entities:
            e.update(*args, **kwargs, game_size=pg.Vector2(self.screen_width, self.screen_height))

    def run(self) -> None:
        pg.init()
        self.screen = pg.display.set_mode((self.screen_width, self.screen_height))
        pg.display.set_caption("Game")
        self.clock = pg.time.Clock()

        while True:
            delta = pg.Vector2(0, 0)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                if event.type == pg.MOUSEBUTTONDOWN:
                    pass

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_DOWN:
                        delta.y -= 32
                    if event.key == pg.K_UP:
                        delta.y += 32
                    if event.key == pg.K_RIGHT:
                        delta.x -= 32
                    if event.key == pg.K_LEFT:
                        delta.x += 32

            self.screen.fill("black")

            self.update(delta=delta)
            self.render()

            pg.display.update()
            self.clock.tick(60)
