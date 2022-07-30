from random import choice

import pygame as pg

import bindu.engine as bindu


def main() -> None:
    game = bindu.Game()

    # grass = bindu.Tile(game.data_path / "grass.png", position=pg.Vector2(0, 0))
    # dirt = bindu.Tile(game.data_path / "dirt.png", position=pg.Vector2(32, 64))
    # water = bindu.Tile(game.data_path / "water.png", position=pg.Vector2(96, 64))

    tile_map = {
        "0": pg.image.load(game.data_path / "grass.png"),
        "1": pg.image.load(game.data_path / "dirt.png"),
        "2": pg.image.load(game.data_path / "water.png"),
    }

    map1 = [''.join([choice("012") for _ in range(game.screen_height // 16)]) for _ in range(game.screen_width // 16)]

    my_map = bindu.Map(tile_map=tile_map, values=map1, size=(game.screen_width*2, game.screen_height*2))

    game.add_entity(my_map)

    game.run()


if __name__ == "__main__":
    main()
