import city
import unit
import player_territory

import random

class Player:
    """
    An object representing a player of the game
    Includes both computer and human players
    """
    def __init__(self, game_obj, p_id):
        """
        Initialise a new Player object
        Requires a p_id, or unique Player id, by which this player can be referenced
        The Player starts with no cities, units, or territory.
        """
        self.game = game_obj
        self.id = p_id
        self.cities = []
        self.territory = player_territory.PlayerTerritory(game_obj, self)
        self.units = []
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

    def add_city(self, c):
        """
        Add an existing City object to the Player object
        TODO: ensure that the PlayerTerritory object is appropriately modified
        """
        self.cities.append(c)

    def remove_city(self, c):
        """
        Remove an existing City object from the Player object
        under the precondition that this Player object has that city
        TODO: ensure that the PlayerTerritory object is appropriately modified
        """
        self.cities.remove(c)
