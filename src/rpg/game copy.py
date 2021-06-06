from pathlib import Path
from random import randint
from time import sleep
from typing import Optional

import pygame


class Sprite(object):
    sheet: pygame.Surface

    def __init__(self, image_path: Path):
        self.sheet = pygame.image.load(image_path).convert_alpha()

    def get_frame(
        self,
        frame_id: tuple[int]=(0, 0),
        width: int=48,
        height: int=48,
        scale: int=1,
        color_key: Optional[tuple[int, int, int]]=(0, 0, 0)
    ) -> pygame.Surface:
        image = pygame.Surface((width, height)).convert_alpha()

        frame_x, frame_y = frame_id[0] * width, frame_id[1] * height
        image.blit(self.sheet,
                   (0, 0),
                   (frame_x, frame_y, width, height))

        scaled_width, scaled_height = width * scale, height * scale
        image = pygame.transform.scale(image,
                                       (scaled_width, scaled_height))
        image.set_colorkey(color_key)

        return image


class Player(pygame.sprite.Sprite):
    def __init__(self, image_path: Path):
        super().__init__(self, self.containers)

        sprite = Sprite(image_path)

        move_down = [sprite.get_frame(frame_id=(key, 0)) for key in range(2)]
        move_left = [sprite.get_frame(frame_id=(key, 1)) for key in range(2)]
        move_right = [sprite.get_frame(frame_id=(key, 2)) for key in range(2)]
        move_up = [sprite.get_frame(frame_id=(key, 3)) for key in range(2)]

        self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
        self.origtop = self.rect.top
        self.facing = -1

    def move(direction_x: int, direction_y: int):
        if direction:
            self.facing = direction
        self.rect.move_ip(direction * self.speed, 0)
        self.rect = self.rect.clamp(SCREENRECT)
        if direction < 0:
            self.image = self.images[0]
        elif direction > 0:
            self.image = self.images[1]
        self.rect.top = self.origtop - (self.rect.left // self.bounce % 2)


class Game(object):
    running: bool = True
    clock: pygame.time.Clock
    screen: pygame.surface.Surface
    player: pygame.surface.Surface

    def __init__(
        self,
        title: str="Game",
        width: int=640,
        height: int=480
    ):
        sprite_path = (Path(__file__).parent.parent.parent
                       / 'data'
                       / 'sprite'
                       / 'saddled_yak.png')
        self.SCREEN_RECT = pygame.Rect(0, 0, width, height)

        pygame.init()

        # Set display mode
        winstyle = 0
        best_depth = pygame.display.mode_ok(self.SCREEN_RECT.size, winstyle, 32)
        self.screen = pygame.display.set_mode(self.SCREEN_RECT.size, winstyle, best_depth)
        pygame.display.set_caption(title)

        # Load images
        self.player = Sprite(sprite_path)
        self.clock = pygame.time.Clock()

    def update(self) -> None:
        # frame = self.player.get_frame(frame_id=(randint(0, 2),
        #                                         randint(0, 3)))
        print(self.clock.get_rawtime())
        row = randint(0, 2)
        frames = [self.player.get_frame(frame_id=(row, i)) for i in range(4)]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

        self.screen.fill((20, 20, 20))
        for idx, frame in enumerate(frames):
            self.screen.blit(frame, (300, 250 + idx * 50))
        pygame.display.update()
        pygame.time.delay(1000)
        self.clock.tick(40)

def main():
    game = Game(title="Sprite Test")
    while game.running:
        game.update()


if __name__ == '__main__':
    main()