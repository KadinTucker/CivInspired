import city
import player

class Tile:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.player_owner = None
        self.city_owner = None

