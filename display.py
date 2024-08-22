import pygame
import sys
import random

import city
import worldgen

import terrain_palettes

EARTH_PLATE_TYPES = [1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0]

TERRAIN_COLORS = {
    "J": (0, 100, 30),
    "d": (200, 200, 150),
    "S": (150, 200, 50),
    "g": (15, 225, 15),
    "p": (200, 175, 30),
    "F": (25, 150, 50),
    "T": (0, 125, 100),
    "u": (0, 175, 150),
    "I": (225, 225, 255),
    "~": (0, 15, 200),
    "-": (125, 125, 250),
    "=": (105, 105, 220)
}
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

"""
D8:
1 2 3
4 0 5
6 7 8
"""
D8_RELATIVE_DESTINATIONS = [
    (0, 0),
    (-1, -1),
    (0, -1),
    (1, -1),
    (-1, 0),
    (1, 0),
    (-1, 1),
    (0, 1),
    (1, 1)
]
ELEVATION_COLORS = {
    ".": None,
    "+": (50, 75, 250),
    "v": (50, 150, 250),
    "f": None,
    "H": (150, 150, 150),
    "M": (100, 25, 0)
}


def regenerate_elev_map():
    return worldgen.build_elev_from_scratch()


def get_climate_map(elev_map):
    print("Simulating climate...")
    return worldgen.build_climateclass_map(worldgen.build_waterclass_map(elev_map), elev_map)


def get_d8(elev_map):
    return worldgen.build_d8_map(elev_map)


def get_topo(elev_map):
    return worldgen.build_topography_map(elev_map)


def draw_terrain(display, climatemap, xwidth, ywidth, xcorner, ycorner):
    for x in range(len(climatemap)):
        for y in range(len(climatemap[x])):
            c = get_draw_coordinate(x, y, xwidth, ywidth, xcorner, ycorner)
            pygame.draw.rect(display, random.choice(TERRAIN_PALETTES[climatemap[x][y]]),
                             pygame.Rect(c[0], c[1], xwidth, ywidth))
    pygame.display.update()

def draw_borders(display, xwidth, ywidth, xcorner, ycorner, active_city):
    for t in range(len(active_city.land)):
        coordinate = get_draw_coordinate(active_city.land[t][0], active_city.land[t][1],
                                         xwidth, ywidth, xcorner, ycorner)
        pygame.draw.rect(display, (255, 0, 255),
                         pygame.Rect(coordinate[0], coordinate[1], xwidth, ywidth), 1)


def draw_cities(display, xwidth, ywidth, xcorner, ycorner, cities, font):
    for c in cities:
        draw_borders(display, xwidth, ywidth, xcorner, ycorner, c)
        display.blit(font.render(c.name, True, (0, 0, 0)), get_draw_coordinate(c.x, c.y, xwidth, ywidth, xcorner, ycorner))
    pygame.display.update()


def draw_map(display, climate_map, xwidth, ywidth, xcorner, ycorner):
    draw_terrain(display, climate_map, xwidth, ywidth, xcorner, ycorner)


def find_mouse_position(xwidth, ywidth, xcorner, ycorner):
    mouse_pos = pygame.mouse.get_pos()
    return (int((mouse_pos[0] + xcorner) / xwidth), int((mouse_pos[1] + ycorner) / ywidth))


def get_draw_coordinate(xmap, ymap, xwidth, ywidth, xcorner, ycorner):
    return xmap * xwidth - xcorner, ymap * ywidth - ycorner


def draw_degree_labels(display, climate_map, font, xwidth, ywidth, xcorner, ycorner):
    display.blit(font.render("67.5°N", True, (255, 255, 255)),
                 get_draw_coordinate(0, len(climate_map[0]) // 8, xwidth, ywidth, 0, ycorner))
    display.blit(font.render("45°N", True, (255, 255, 255)),
                 get_draw_coordinate(0, 2 * len(climate_map[0]) // 8, xwidth, ywidth, 0, ycorner))
    display.blit(font.render("22.5°N", True, (255, 255, 255)),
                 get_draw_coordinate(0, 3 * len(climate_map[0]) // 8, xwidth, ywidth, 0, ycorner))
    display.blit(font.render("0°", True, (255, 255, 255)),
                 get_draw_coordinate(0, 4 * len(climate_map[0]) // 8, xwidth, ywidth, 0, ycorner))
    display.blit(font.render("22.5°S", True, (255, 255, 255)),
                 get_draw_coordinate(0, 5 * len(climate_map[0]) // 8, xwidth, ywidth, 0, ycorner))
    display.blit(font.render("45°S", True, (255, 255, 255)),
                 get_draw_coordinate(0, 6 * len(climate_map[0]) // 8, xwidth, ywidth, 0, ycorner))
    display.blit(font.render("67.5°S", True, (255, 255, 255)),
                 get_draw_coordinate(0, 7 * len(climate_map[0]) // 8, xwidth, ywidth, 0, ycorner))

def redraw(display, climate_map, cities, font, xwidth, ywidth, xcorner, ycorner):
    display.fill((0, 0, 0))
    draw_map(display, climate_map, xwidth, ywidth, xcorner, ycorner)
    draw_degree_labels(display, climate_map, font, xwidth, ywidth, xcorner, ycorner)
    draw_cities(display, xwidth, ywidth, xcorner, ycorner, cities, font)
    pygame.display.update()

def main():
    pygame.init()
    font = pygame.font.Font(None, 18)
    display = pygame.display.set_mode((800, 400))
    elev_map = regenerate_elev_map()
    # elev_map = worldgen.build_elev_from_csv_plates("Earth/plates_remapped.csv", EARTH_PLATE_TYPES, None)
    climate_map = get_climate_map(elev_map)
    xcorner = 0
    ycorner = 0
    xwidth = int(800 / len(climate_map))
    ywidth = int(400 / len(climate_map[0]))
    cities = []
    economy = city.Economy()
    redraw(display, climate_map, cities, font, xwidth, ywidth, xcorner, ycorner)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                m = find_mouse_position(xwidth, ywidth, xcorner, ycorner)
                new_city = city.City(m[0], m[1], len(cities), random.choice(city.TEMP_CITY_NAMES))
                cities.append(new_city)
                economy.add_city(new_city)
                redraw(display, climate_map, cities, font, xwidth, ywidth, xcorner, ycorner)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print(" = RUNNING TURN = ")
                    for c in cities:
                        c.run_production_phase()
                    economy.run_economy()
                    for c in cities:
                        c.run_resolution_phase()
                elif event.key == pygame.K_TAB:
                    for c in cities:
                        c.print_report()
                        print("\n")
                elif event.key == pygame.K_PLUS:
                    xwidth += 1
                    ywidth += 1
                    redraw(display, climate_map, cities, font, xwidth, ywidth, xcorner, ycorner)
                elif event.key == pygame.K_MINUS:
                    xwidth -= 1
                    ywidth -= 1
                    redraw(display, climate_map, cities, font, xwidth, ywidth, xcorner, ycorner)
                elif event.key == pygame.K_RIGHT:
                    xcorner += 5 * xwidth
                    redraw(display, climate_map, cities, font, xwidth, ywidth, xcorner, ycorner)
                elif event.key == pygame.K_LEFT:
                    xcorner -= 5 * xwidth
                    redraw(display, climate_map, cities, font, xwidth, ywidth, xcorner, ycorner)
                elif event.key == pygame.K_DOWN:
                    ycorner += 5 * ywidth
                    redraw(display, climate_map, cities, font, xwidth, ywidth, xcorner, ycorner)
                elif event.key == pygame.K_UP:
                    ycorner -= 5 * ywidth
                    redraw(display, climate_map, cities, font, xwidth, ywidth, xcorner, ycorner)



if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    main()
