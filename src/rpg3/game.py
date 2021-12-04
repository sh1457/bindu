from pathlib import Path
import sys

import pygame as pg


class Player(pg.sprite.Sprite):
    direction: int = 0
    frame: int = 0
    area: pg.Rect

    old_move = pg.Vector2()
    moving: bool = False

    def __init__(self):
        super().__init__()
        path = Path(__file__).parent.parent.parent / "data/sprite/saddled_yak.png"
        if not path.exists():
            raise ValueError("Missing data")
        self.image = pg.image.load(path).convert_alpha()
        sheet_size = self.image.get_rect()
        self.image = pg.transform.scale(pg.image.load(path).convert_alpha(), (sheet_size.width * 2 // 3, sheet_size.height * 2 // 3))
        self.rect = self.image.get_rect()
        self.update_area()

    def update_area(self):
        sheet_size = self.image.get_rect()
        sprite_size = sheet_size.width // 4
        self.area = pg.Rect(sheet_size.left + (sprite_size * self.frame),
                            sheet_size.top + (sprite_size * self.direction),
                            sprite_size,
                            sprite_size)

    def update(self, move: pg.Vector2):
        """DLRT"""
        direction = -1
        if move.y > 0:
            direction = 0
            print("Down")

        if move.y < 0:
            direction = 3
            print("Top")

        if move.x < 0:
            direction = 1
            print("Left")

        if move.x > 0:
            direction = 2
            print("Right")

        if self.moving:
            print(self.frame)
            if self.frame < 3:
                self.frame += 1
                self.rect.move_ip(self.old_move.x // 4, self.old_move.y // 4)
            else:
                self.rect.move_ip(self.old_move.x // 4, self.old_move.y // 4)
                self.frame = 0
                self.moving = False

            if direction >= 0 and direction != self.direction and self.moving:
                print("Changed directions midway")
                self.rect.move_ip(self.old_move.x // 4 * (3-self.frame), self.old_move.y // 4 * (3-self.frame))
                self.frame = 0
                self.moving = False
                self.old_move = move

        if direction >= 0:
            self.direction = direction
            self.moving = True
            self.old_move = move

        self.update_area()



class Game(object):
    running: bool = True
    clock: pg.time.Clock

    def __init__(
        self,
        title: str="Game",
        width: int=640,
        height: int=480
    ):
        pg.init()
        pg.display.set_caption(title)
        pg.key.set_repeat(200)

        # Set display mode
        best_depth = pg.display.mode_ok((width, height), 0, 32)
        self.display_surface = pg.display.set_mode((width, height), 0, best_depth)

        # Make player
        self.player = Player()

        # Set Clock
        self.clock = pg.time.Clock()

    def event_handler(self) -> pg.Vector2:
        move = pg.Vector2()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                if event.key == pg.K_LEFT:
                    move.x -= 32
                if event.key == pg.K_RIGHT:
                    move.x += 32
                if event.key == pg.K_UP:
                    move.y -= 32
                if event.key == pg.K_DOWN:
                    move.y += 32
        return move

    def update(self):
        move = self.event_handler()
        self.player.update(move)

    def render(self):
        pg.draw.rect(self.display_surface, (255,255,255), self.display_surface.get_rect())
        for x in range(0, 640, 32):
            for y in range(0, 480, 32):
                pg.draw.line(self.display_surface, (0,0,0), (x,y), (x,480-y))
                pg.draw.line(self.display_surface, (0,0,0), (x,y), (640-x,y))
        self.display_surface.blit(self.player.image, self.player.rect, area=self.player.area)
        sprite_area = pg.Rect(self.player.rect.x,
                              self.player.rect.y,
                              self.player.area.width,
                              self.player.area.height)
        pg.draw.rect(self.display_surface, (255,25,25,22), sprite_area, width=1)
        pg.display.update()


def main():
    game = Game(title="Sprite Test")
    while game.running:
        game.render()
        game.update()
        game.clock.tick(3)


if __name__ == '__main__':
    main()