import player
import world

class Game:
    """
    An object storing and collecting all of the relevant information for a single game
    Includes the Player objects in the game as well as the World used in the game.
    """
    def __init__(self, num_players, world_obj):
        """
        Initialise a new Game object
        Takes in a number of Players to be generated, as well as a world
        Note that the world takes in a Game object, which is set to this once the game is constructed
        TODO: make the world be generated as part of the Game construction
        """
        self.world = world_obj
        self.world.game = self
        self.players = []
        for i in range(num_players):
            self.players.append(player.Player(self, i))