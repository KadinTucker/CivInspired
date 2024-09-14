import city
import unit

class Player:
    """
    An object representing a player of the game
    Includes both computer and human players
    """
    def __init__(self, p_id):
        """
        Initialise a new Player object
        Requires a p_id, or unique Player id, by which this player can be referenced
        The Player starts with no cities, units, or territory.
        """
        self.id = p_id
        self.cities = []
        self.territory = []
        self.units = []

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
