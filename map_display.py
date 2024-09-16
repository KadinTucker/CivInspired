import pygame
import sys
import random

import game
import io_util
import terrain_palettes
import world

TERRAIN_PALETTES = {
    "J": terrain_palettes.JUNGLE_E,
    "d": terrain_palettes.DESERT_E,
    "S": terrain_palettes.SCRUB_E,
    "g": terrain_palettes.GRASSLAND_E,
    "p": terrain_palettes.PLAINS_E,
    "F": terrain_palettes.FOREST_E,
    "T": terrain_palettes.TAIGA_E,
    "u": terrain_palettes.TUNDRA_E,
    "I": terrain_palettes.ICE_E,
    "~": terrain_palettes.OCEAN_E,
    "-": terrain_palettes.COAST_E,
    "=": terrain_palettes.COAST_E,
}

def load_climate_map(filename):
    return io_util.load_matrix_from_csv(filename)

def get_draw_coordinate(x, y, map_corner, tile_size, map_dimensions):
    offset = 0
    if tile_size[0] * map_dimensions[0] < PANE_DIMENSIONS[0]:
        offset = (PANE_DIMENSIONS[0] - int(tile_size[0]) * map_dimensions[0]) // 2
    return (offset + (x + map_corner[0]) % map_dimensions[0] * int(tile_size[0]), (y + map_corner[1]) * int(tile_size[0]))

def draw_terrain(display, colormap, map_corner, tile_size):
    for x in range(len(colormap)):
        for y in range(len(colormap[x])):
            c = get_draw_coordinate(x, y, map_corner, tile_size, (len(colormap), len(colormap[x])))
            pygame.draw.rect(display, colormap[x][y],
                             pygame.Rect(c[0], c[1], int(tile_size[0]), int(tile_size[1])))

def draw_blackmap(display, player, map_corner, tile_size):
    for x in range(len(player.territory.explored)):
        for y in range(len(player.territory.explored[x])):
            c = get_draw_coordinate(x, y, map_corner, tile_size,
                                    (len(player.territory.explored), len(player.territory.explored[x])))
            if not player.territory.explored[x][y]:
                pygame.draw.rect(display, (10, 10, 10),
                                 pygame.Rect(c[0], c[1], int(tile_size[0]), int(tile_size[1])))

def generate_color_map(climatemap):
    colormap = [[(0, 0, 0) for _ in range(len(climatemap[x]))] for x in range(len(climatemap))]
    for x in range(len(climatemap)):
        for y in range(len(climatemap[x])):
            colormap[x][y] = random.choice(TERRAIN_PALETTES[climatemap[x][y]])
    return colormap


PANE_DIMENSIONS = (800, 400)

def main():
    pygame.init()
    font = pygame.font.Font(None, 18)
    display = pygame.display.set_mode(PANE_DIMENSIONS)
    climatemap = load_climate_map("climate_map.csv")
    colormap = generate_color_map(climatemap)

    world_obj = world.World(None, climatemap, climatemap)
    game_obj = game.Game(1, world_obj)

    player_start = (random.randint(2, len(climatemap) - 3), random.randint(2, len(climatemap[0]) - 3))
    game_obj.players[0].territory.explored[player_start[0]][player_start[1]] = True
    game_obj.players[0].territory.explored[player_start[0] + 1][player_start[1]] = True
    game_obj.players[0].territory.explored[player_start[0] - 1][player_start[1]] = True
    game_obj.players[0].territory.explored[player_start[0]][player_start[1] + 1] = True
    game_obj.players[0].territory.explored[player_start[0]][player_start[1] - 1] = True
    game_obj.players[0].territory.explored[player_start[0] + 1][player_start[1] + 1] = True
    game_obj.players[0].territory.explored[player_start[0] - 1][player_start[1] - 1] = True
    game_obj.players[0].territory.explored[player_start[0] - 1][player_start[1] + 1] = True
    game_obj.players[0].territory.explored[player_start[0] + 1][player_start[1] - 1] = True
    game_obj.players[0].territory.explored[player_start[0] + 2][player_start[1] - 1] = True
    game_obj.players[0].territory.explored[player_start[0] + 2][player_start[1] + 1] = True
    game_obj.players[0].territory.explored[player_start[0] + 2][player_start[1]] = True
    game_obj.players[0].territory.explored[player_start[0] - 2][player_start[1] - 1] = True
    game_obj.players[0].territory.explored[player_start[0] - 2][player_start[1] + 1] = True
    game_obj.players[0].territory.explored[player_start[0] - 2][player_start[1]] = True
    game_obj.players[0].territory.explored[player_start[0] - 1][player_start[1] + 2] = True
    game_obj.players[0].territory.explored[player_start[0] + 1][player_start[1] + 2] = True
    game_obj.players[0].territory.explored[player_start[0]][player_start[1] + 2] = True
    game_obj.players[0].territory.explored[player_start[0] - 1][player_start[1] - 2] = True
    game_obj.players[0].territory.explored[player_start[0] + 1][player_start[1] - 2] = True
    game_obj.players[0].territory.explored[player_start[0]][player_start[1] - 2] = True

    map_corner = (-player_start[0] + 12, -player_start[1] + 5)
    tile_size = (32, 32)
    while True:
        display.fill((0, 0, 0))
        draw_terrain(display, colormap, map_corner, tile_size)
        #draw_blackmap(display, game_obj.players[0], map_corner, tile_size)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    map_corner = (map_corner[0] - 5, map_corner[1])
                elif event.key == pygame.K_LEFT:
                    map_corner = (map_corner[0] + 5, map_corner[1])
                if event.key == pygame.K_UP:
                    map_corner = (map_corner[0], map_corner[1] + 5)
                elif event.key == pygame.K_DOWN:
                    map_corner = (map_corner[0], map_corner[1] - 5)
                elif event.key == pygame.K_PLUS:
                    prev_tiles = (PANE_DIMENSIONS[0] / tile_size[0], PANE_DIMENSIONS[1] / tile_size[1])
                    tile_size = (tile_size[0] * 1.5, tile_size[1] * 1.5)
                    new_tiles = (PANE_DIMENSIONS[0] / tile_size[0], PANE_DIMENSIONS[1] / tile_size[1])
                    map_corner = (map_corner[0] - int(prev_tiles[0] - new_tiles[0]) // 2,
                                  map_corner[1] - int(prev_tiles[1] - new_tiles[1]) // 2)
                elif event.key == pygame.K_MINUS:
                    prev_tiles = (PANE_DIMENSIONS[0] / tile_size[0], PANE_DIMENSIONS[1] / tile_size[1])
                    tile_size = (tile_size[0] / 1.5, tile_size[1] / 1.5)
                    new_tiles = (PANE_DIMENSIONS[0] / tile_size[0], PANE_DIMENSIONS[1] / tile_size[1])
                    map_corner = (map_corner[0] - int(prev_tiles[0] - new_tiles[0]) // 2,
                                  map_corner[1] - int(prev_tiles[1] - new_tiles[1]) // 2)
        pygame.display.update()

if __name__ == "__main__":
    main()