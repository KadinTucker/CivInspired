import pygame
import sys
import random

import game
import io_util
import camera
import macro_worldgen
import terrain_palettes
import world
import worldgen

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

SIMPLE_COLORS = {
    "J": (31, 74, 20),
    "d": (187, 160, 133),
    "S": (156, 133, 58),
    "g": (86, 119, 65),
    "p": (159, 151, 119),
    "F": (46, 82, 43),
    "T": (59, 75, 78),
    "u": (95, 95, 81),
    "I": (189, 194, 188),
    "~": (30, 48, 104),
    "-": (114, 144, 161),
    "=": (84, 93, 165),
}


def load_climate_map(filename):
    return io_util.load_matrix_from_csv(filename)


def get_draw_coordinate(x, y, map_corner, tile_size, map_dimensions):
    offset = 0
    if tile_size[0] * map_dimensions[0] < PANE_DIMENSIONS[0]:
        offset = (PANE_DIMENSIONS[0] - int(tile_size[0]) * map_dimensions[0]) // 2
    return (
    offset + (x + map_corner[0]) % map_dimensions[0] * int(tile_size[0]), (y + map_corner[1]) * int(tile_size[0]))


def draw_terrain(display, colormap, camera_obj):
    for x in range(len(colormap)):
        for y in range(len(colormap[x])):
            cx, cy = camera_obj.project_coordinate((x, y))
            pygame.draw.rect(display, colormap[x][y],
                             pygame.Rect(int(cx), int(cy), camera_obj.view_scale, camera_obj.view_scale))

def draw_map(display, colormap, camera_obj, game_obj):
    for x in range(int(display.get_width() / camera_obj.view_scale)):
        for y in range(int(display.get_height() / camera_obj.view_scale)):
            world_x, world_y = worldgen.wrap_coordinate(x + int(camera_obj.view_corner[0]),
                                                        y + int(camera_obj.view_corner[1]),
                                                        len(colormap), len(colormap[0]))
            rect = (x * camera_obj.view_scale, y * camera_obj.view_scale, camera_obj.view_scale, camera_obj.view_scale)
            pygame.draw.rect(display, colormap[world_x][world_y], rect)
            draw_player_control(display, game_obj.players[0], rect, world_x, world_y)

def get_control_boundaries(x, y, control_matrix):
    neighbors = worldgen.get_neighbors(x, y, len(control_matrix), len(control_matrix[x]))
    return [not control_matrix[n[0]][n[1]] for n in neighbors]


# For each border, a pair of vertices
# The coordinates in each vertex describe whether the width of the rect should be added
# In particular:
# (1, 0) is the top right corner
# (1, 1) is the bottom right
# (0, 0) is the top left
# (0, 1) is the bottom left
BORDER_VERTICES = [((1, 0), (1, 1)), ((0, 0), (0, 1)), ((0, 1), (1, 1)), ((0, 0), (1, 0))]


def draw_borders(display, x, y, control_matrix, color, rect):
    boundaries = get_control_boundaries(x, y, control_matrix)
    for b in range(len(boundaries)):
        if boundaries[b]:
            pygame.draw.line(display, color, (rect[0] + BORDER_VERTICES[b][0][0] * (rect[2] - 1),
                                              rect[1] + BORDER_VERTICES[b][0][1] * (rect[3] - 1)),
                             (rect[0] + BORDER_VERTICES[b][1][0] * (rect[2] - 1),
                              rect[1] + BORDER_VERTICES[b][1][1] * (rect[3] - 1)))

def draw_player_control_old(display, player_obj, camera_obj):
    for x in range(len(player_obj.territory.territory)):
        for y in range(len(player_obj.territory.territory[x])):
            cx, cy = camera_obj.project_coordinate((x, y))
            if player_obj.territory.cores[x][y]:
                pygame.draw.rect(display, player_obj.color,
                                 pygame.Rect(int(cx), int(cy), camera_obj.view_scale, camera_obj.view_scale))
                draw_borders(display, x, y, player_obj.territory.cores, (0, 0, 0),
                             (int(cx), int(cy), camera_obj.view_scale, camera_obj.view_scale))
            elif player_obj.territory.territory[x][y]:
                pygame.draw.rect(display, player_obj.color,
                                 pygame.Rect(int(cx), int(cy), camera_obj.view_scale, camera_obj.view_scale),
                                 int(camera_obj.view_scale / 4))
                draw_borders(display, x, y, player_obj.territory.territory, (0, 0, 0),
                             (int(cx), int(cy), camera_obj.view_scale, camera_obj.view_scale))

def draw_player_control(display, player_obj, rect, x, y):
    if player_obj.territory.cores[x][y]:
        pygame.draw.rect(display, player_obj.color, rect)
        draw_borders(display, x, y, player_obj.territory.cores, (0, 0, 0), rect)
    elif player_obj.territory.territory[x][y]:
        pygame.draw.rect(display, player_obj.color, rect, int(rect[3] / 4))
        draw_borders(display, x, y, player_obj.territory.territory, (0, 0, 0), rect)

def draw_blackmap(display, player, camera_obj):
    for x in range(len(player.territory.explored)):
        for y in range(len(player.territory.explored[x])):
            cx, cy = camera_obj.project_coordinate((x, y))
            if not player.territory.explored[x][y]:
                pygame.draw.rect(display, (10, 10, 10),
                                 pygame.Rect(int(cx), int(cy), camera_obj.view_scale, camera_obj.view_scale))


def generate_color_map(climatemap):
    colormap = [[(0, 0, 0) for _ in range(len(climatemap[x]))] for x in range(len(climatemap))]
    for x in range(len(climatemap)):
        for y in range(len(climatemap[x])):
            # colormap[x][y] = random.choice(TERRAIN_PALETTES[climatemap[x][y]])
            colormap[x][y] = SIMPLE_COLORS[climatemap[x][y]]
    return colormap


PANE_DIMENSIONS = (800, 400)

TC_COLORS = {".": (30, 48, 104), "-": (20, 36, 80), "I": (44, 71, 48), "l": (149, 141, 118),
             "V": (101, 48, 41), "M": (71, 71, 41)}
ELEV_BREAKS = [macro_worldgen.CONTINENT_LEVEL, macro_worldgen.SEA_LEVEL,
               macro_worldgen.SEA_LEVEL + macro_worldgen.VOLCANO_SHARING,
               macro_worldgen.SEA_LEVEL + macro_worldgen.MOUNTAIN_SHARING,
               macro_worldgen.SEA_LEVEL + macro_worldgen.VOLCANO_ELEV,
               macro_worldgen.SEA_LEVEL + macro_worldgen.MOUNTAIN_ELEV]
ELEV_COLORS = [(30, 48, 104), (94, 113, 175), (44, 71, 48), (86, 110, 80),
               (149, 141, 118), (141, 110, 41), (71, 71, 41)]


def classify_elev_color(elevation):
    index = 0
    while index < len(ELEV_BREAKS) and elevation > ELEV_BREAKS[index]:
        index += 1
    return ELEV_COLORS[index]


def main():
    pygame.init()
    font = pygame.font.Font(None, 18)
    display = pygame.display.set_mode(PANE_DIMENSIONS)
    climatemap = load_climate_map("climate_map.csv")
    hill_map = load_climate_map("valley_map.csv")
    cl_colormap = generate_color_map(climatemap)
    elev_map = load_climate_map("elev_map.csv")
    tc_map = load_climate_map("tileclass_map.csv")
    fa_map = load_climate_map("accumulation_map.csv")
    tc_colormap = [[(0, 0, 0) for _ in range(len(tc_map[x]))] for x in range(len(tc_map))]
    ev_colormap = [[(0, 0, 0) for _ in range(len(elev_map[x]))] for x in range(len(elev_map))]
    fa_colormap = [[(0, 0, 0) for _ in range(len(elev_map[x]))] for x in range(len(elev_map))]
    for x in range(len(tc_map)):
        for y in range(len(tc_map[x])):
            tc_colormap[x][y] = TC_COLORS[tc_map[x][y]]
            if hill_map[x][y] == "True":
                tc_colormap[x][y] = (0, 0, 0)
            ev_colormap[x][y] = classify_elev_color(float(elev_map[x][y]))
            fa_value = min(255, 10 * float(fa_map[x][y]))
            fa_colormap[x][y] = (fa_value, fa_value, fa_value)
    world_obj = world.World(None, climatemap, climatemap)
    game_obj = game.Game(1, world_obj)

    colormaps = [cl_colormap, ev_colormap, tc_colormap, fa_colormap]
    colormap_index = 0

    valid_start = False
    while not valid_start:
        player_start = (random.randint(2, len(climatemap) - 3), random.randint(2, len(climatemap[0]) - 3))
        valid_start = climatemap[player_start[0]][player_start[1]] not in ["-", "~", "I"]
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

    camera_obj = camera.Camera((len(climatemap), len(climatemap[0])),
                               (display.get_width(), display.get_height()))
    camera_obj.view_corner = (player_start[0] - 12, player_start[1] - 5)
    camera_obj.view_scale = 32

    while True:
        display.fill((50, 50, 50))
        #draw_terrain(display, colormaps[colormap_index], camera_obj)
        #draw_player_control(display, game_obj.players[0], camera_obj)
        draw_map(display, colormaps[colormap_index], camera_obj, game_obj)
        #draw_blackmap(display, game_obj.players[0], camera_obj)
        #cx, cy = camera_obj.project_coordinate(player_start)
        #pygame.draw.rect(display, game_obj.players[0].color,
        #                 pygame.Rect(int(cx), int(cy), camera_obj.view_scale, camera_obj.view_scale))
        #pygame.draw.rect(display, (0, 0, 0),
        #                 pygame.Rect(int(cx), int(cy), camera_obj.view_scale, camera_obj.view_scale), 1)
        ox, oy = camera_obj.deproject_coordinate(pygame.mouse.get_pos())
        cx, cy = camera_obj.project_coordinate((ox, oy))
        pygame.draw.rect(display, (255, 255, 255),
                         pygame.Rect(int(cx), int(cy), camera_obj.view_scale, camera_obj.view_scale))
        for n in worldgen.get_neighbors(ox, oy, len(climatemap), len(climatemap[0])):
            cx, cy = camera_obj.project_coordinate((n[0], n[1]))
            pygame.draw.rect(display, (155, 155, 155),
                             pygame.Rect(int(cx), int(cy), camera_obj.view_scale, camera_obj.view_scale))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    camera_obj.shift_view((75, 0))
                elif event.key == pygame.K_LEFT:
                    camera_obj.shift_view((-75, 0))
                if event.key == pygame.K_UP:
                    camera_obj.shift_view((0, -75))
                elif event.key == pygame.K_DOWN:
                    camera_obj.shift_view((0, 75))
                elif event.key == pygame.K_PLUS:
                    camera_obj.set_scale(round(1.6 * camera_obj.view_scale), pygame.mouse.get_pos())
                elif event.key == pygame.K_MINUS:
                    camera_obj.set_scale(max(1, round(camera_obj.view_scale / 1.6)), pygame.mouse.get_pos())
                elif event.key == pygame.K_TAB:
                    colormap_index += 1
                    colormap_index %= len(colormaps)
            elif event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    mouse_coordinate = camera_obj.deproject_coordinate(pygame.mouse.get_pos())
                    if 0 <= mouse_coordinate[0] < len(game_obj.players[0].territory.explored) \
                            and 0 <= mouse_coordinate[1] < len(game_obj.players[0].territory.explored[0]):
                        game_obj.players[0].territory \
                            .explored[int(mouse_coordinate[0])][int(mouse_coordinate[1])] = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_RIGHT:
                    x, y = camera_obj.deproject_coordinate(pygame.mouse.get_pos())
                    world_coordinate = worldgen.wrap_coordinate(x, y, len(climatemap), len(climatemap[0]))
                    if game_obj.players[0].territory.territory[int(world_coordinate[0])][int(world_coordinate[1])]:
                        game_obj.players[0].territory \
                            .cores[int(world_coordinate[0])][int(world_coordinate[1])] = True
                    game_obj.players[0].territory \
                        .territory[int(world_coordinate[0])][int(world_coordinate[1])] = True

        pygame.display.update()


if __name__ == "__main__":
    main()
