from pathlib import Path
from random import randint
from time import sleep
from typing import Optional, NamedTuple

import pygame as pg


class FilledRect(NamedTuple):
    rect: pg.Rect
    color: pg.Color

    def draw(self, surface: pg.Surface):
        pg.draw.rect(surface=surface, color=self.color, rect=self.rect)


def player_move(surface: FilledRect, sprite: FilledRect, move: pg.Vector2) -> FilledRect:
    new_pos = sprite.rect.move(move.x, move.y)
    if not surface.rect.contains(new_pos):
        if new_pos.left < surface.rect.left:
            new_pos.left = surface.rect.left
        if new_pos.right > surface.rect.right:
            new_pos.right = surface.rect.right
        if new_pos.top < surface.rect.top:
            new_pos.top = surface.rect.top
        if new_pos.bottom > surface.rect.bottom:
            new_pos.bottom = surface.rect.bottom
    return FilledRect(rect=new_pos, color=sprite.color)


class Game(object):
    running: bool = True
    clock: pg.time.Clock
    display: pg.Surface
    screen: FilledRect
    canvas: FilledRect
    bg_map: list[FilledRect]
    player: FilledRect

    def __init__(
        self,
        title: str="Game",
        width: int=640,
        height: int=480
    ):
        self.screen = FilledRect(pg.Rect(0, 0, width, height), pg.Color(0, 0, 0))
        self.canvas = FilledRect(pg.Rect(20, 20, 600, 440), pg.Color(125, 225, 125))

        self.bg_map = [FilledRect(pg.Rect(120, 80, 240, 380), pg.Color(225, 225, 125)),
                       FilledRect(pg.Rect(20, 140, 320, 320), pg.Color(125, 225, 225))]

        pg.init()
        pg.display.set_caption(title)
        pg.key.set_repeat(200)

        # Set display mode
        best_depth = pg.display.mode_ok(self.screen.rect.size, 0, 32)
        self.display = pg.display.set_mode(self.screen.rect.size, 0, best_depth)

        # Load images
        self.player = FilledRect(pg.Rect(300, 200, 20, 40), pg.Color(120, 120, 255))

        # Set Clock
        self.clock = pg.time.Clock()

    def update(self) -> None:
        MOVE_SIZE = 20
        self.screen.draw(self.display)
        self.canvas.draw(self.display)

        for bg in self.bg_map:
            bg.draw(self.display)

        move = pg.Vector2(x=0, y=0)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                if event.key == pg.K_LEFT:
                    move.x -= MOVE_SIZE
                if event.key == pg.K_RIGHT:
                    move.x += MOVE_SIZE
                if event.key == pg.K_UP:
                    move.y -= MOVE_SIZE
                if event.key == pg.K_DOWN:
                    move.y += MOVE_SIZE

            # if event.type == pg.KEYUP:
            #     if event.key == pg.K_LEFT:
            #         move.x = 0
            #     if event.key == pg.K_RIGHT:
            #         move.x = 0
            #     if event.key == pg.K_UP:
            #         move.y = 0
            #     if event.key == pg.K_DOWN:
            #         move.y = 0

        # print(">> ", move)
        self.player = player_move(self.canvas, self.player, move)

        self.player.draw(self.display)
        pg.display.update()
        # pg.time.delay(1000)
        self.clock.tick(60)


def main():
    game = Game(title="Sprite Test")
    while game.running:
        game.update()


if __name__ == '__main__':
    main()