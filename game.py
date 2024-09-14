import player
import world

class Game:
    """
    An object storing and collecting all of the relevant information for a single game
    Includes the Player objects in the game as well as the World used in the game.
    """
    def __init__(self, players, world_obj):
        """
        Initialise a new Game object
        Takes in a list of Player objects, already generated, and a World object
        """
        self.players = players
        self.world = world_obj
