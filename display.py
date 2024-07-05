import pygame
import sys
import random

import city
import worldgen

TERRAIN_COLORS = {
    "J" : (0, 100, 30),
    "d" : (200, 200, 150),
    "S" : (150, 200, 50),
    "g" : (15, 225, 15),
    "p" : (200, 175, 30),
    "F" : (25, 150, 50),
    "T" : (0, 125, 100),
    "u" : (0, 175, 150),
    "I" : (225, 225, 255),
    "~" : (0, 15, 200),
    "-" : (125, 125, 250),
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
    "." : None,
    "+" : (50, 75, 250),
    "v" : (50, 150, 250),
    "f" : None,
    "H" : (150, 150, 150),
    "M" : (100, 25, 0)
}

def regenerate_elev_map():
    return worldgen.build_elev_from_scratch()

def get_climate_map(elev_map):
    return worldgen.build_climateclass_map(worldgen.build_waterclass_map(elev_map), elev_map)

def get_d8(elev_map):
    return worldgen.build_d8_map(elev_map)

def get_topo(elev_map):
    return worldgen.build_topography_map(elev_map)

def draw_terrain(display, climatemap):
    xwidth = int(800 / len(climatemap))
    ywidth = int(400 / len(climatemap[0]))
    for x in range(len(climatemap)):
        for y in range(len(climatemap[x])):
            pygame.draw.rect(display, TERRAIN_COLORS[climatemap[x][y]], pygame.Rect(x * xwidth, y * ywidth, xwidth, ywidth))
    pygame.display.update()

def draw_watersheds(display, d8):
    xwidth = int(800 / len(d8))
    ywidth = int(400 / len(d8[0]))
    for x in range(len(d8)):
        for y in range(len(d8[x])):
            if d8[x][y] != 0:
                pygame.draw.line(display, (0, 15, 125), (int((x + 0.5) * xwidth), int((y + 0.5) * ywidth)), (int((x + 0.5 + D8_RELATIVE_DESTINATIONS[d8[x][y]][0]) * xwidth), int((y + 0.5 + D8_RELATIVE_DESTINATIONS[d8[x][y]][1]) * ywidth)))
    pygame.display.update()

def draw_topography(display, topomap):
    xwidth = int(800 / len(topomap))
    ywidth = int(400 / len(topomap[0]))
    for x in range(len(topomap)):
        for y in range(len(topomap[x])):
            if ELEVATION_COLORS[topomap[x][y]] != None:
                pygame.draw.rect(display, ELEVATION_COLORS[topomap[x][y]], pygame.Rect(x * xwidth, y * ywidth, xwidth, ywidth))
    pygame.display.update()

def draw_cities(display, xwidth, ywidth, cities, font):
    for c in cities:
        pygame.draw.rect(display, (255, 0, 255), pygame.Rect(c.x * xwidth, c.y * ywidth, xwidth, ywidth), 1)
        display.blit(font.render(c.name, True, (0, 0, 0)), (c.x * xwidth, c.y * ywidth))
    pygame.display.update()

def draw_map(display, climate_map):
    #topo_map = get_topo(elev_map)
    #d8 = get_d8(elev_map)
    draw_terrain(display, climate_map)
    #draw_watersheds(display, d8)
    #draw_topography(display, topo_map)

def find_mouse_position(xwidth, ywidth):
    mouse_pos = pygame.mouse.get_pos()
    return (int(mouse_pos[0] / xwidth), int(mouse_pos[1] / ywidth))

def main():
    pygame.init()
    font = pygame.font.Font(None, 18)
    display = pygame.display.set_mode((800, 400))
    elev_map = regenerate_elev_map()
    climate_map = get_climate_map(elev_map)
    xwidth = int(800 / len(climate_map))
    ywidth = int(400 / len(climate_map[0]))
    cities = []
    economy = city.Economy()
    draw_map(display, climate_map)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                m = find_mouse_position(xwidth, ywidth)
                new_city = city.City(m[0], m[1], len(cities), random.choice(city.TEMP_CITY_NAMES))
                cities.append(new_city)
                economy.add_city(new_city)
                draw_cities(display, xwidth, ywidth, cities, font)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print(" = RUNNING TURN = ")
                    for c in cities:
                        c.work_temp()
                    economy.run_economy()
                    for c in cities:
                        c.resolve_turn()
                elif event.key == pygame.K_TAB:
                    for c in cities:
                        c.print_report()
                        print("\n")

if __name__ == "__main__":
    main()