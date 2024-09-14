import player

class PlayerTerritory:
    """
    A class to describe the territory of a player from the Player's perspective
    """
    def __init__(self, game, player_obj):
        self.game = game
        self.player = player_obj
        # The matrix of tiles giving whether the Player has explored them
        self.explored = [[False for _ in range(len(game.world.terrain[x]))] for x in range(len(game.world.terrain))]
        # The matrix of tiles giving whether the Player claims them
        self.claims = [[False for _ in range(len(game.world.terrain[x]))] for x in range(len(game.world.terrain))]
        # The matrix of tiles giving whether the Player tangibly controls them
        self.territory = [[False for _ in range(len(game.world.terrain[x]))] for x in range(len(game.world.terrain))]
        # The matrix of tiles giving whether the Player controls a city that works them
        self.cores = [[False for _ in range(len(game.world.terrain[x]))] for x in range(len(game.world.terrain))]
