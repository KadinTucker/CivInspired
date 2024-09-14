import game

class World:
    """
    A World class, containing several matrices describing the physical world
    Each matrix has the same dimensions, and each describes a different layer of the world
    The layers of the world consist of:
     - The terrain layer, giving the physical terrain type
     - The resource layer, giving any resources that are in the world
     - The improvement layer, giving any improvements that are on each tile
     - The city layer, giving any cities that might be found on each tile
     - The control layer, describing any players and cities that might control
     - The unit layer, giving any units that are on each tile
    """
    def __init__(self, game_obj, terrain, resource):
        """
        Initialise a new World
        With the exception of the Game, each field is a matrix, and all should have the same dimensions
        Takes in `terrain` and `resource` arguments, to have been generated separately
        The `resource` and `terrain` layers must have the same dimensions
        Default behaviour is for improvements, control, and units to start empty
        """
        # Which Game object this world belongs to
        self.game = game_obj
        # The terrain layer's entries are unsigned integers, giving the index of their terrain type
        self.terrain = terrain
        # The resource layer's entries are unsigned integers, giving the index of their resource type
        self.resource = resource
        # The improvement layer's entries are lists containing as many improvements as may exist on each tile
        self.improvement = [[[] for _ in range(len(terrain[x]))] for x in range(len(terrain))]
        # The city layer's entries are City objects, or None if no City is located there
        self.city = [[None for _ in range(len(terrain[x]))] for x in range(len(terrain))]
        # The control layer's entries are tuples of length three with:
        # (a list of claimant Player objects, a controlling Player object if any, a controlling City object if any
        self.control = [[([], None, None) for _ in range(len(terrain[x]))] for x in range(len(terrain))]
        # The unit layer's entries are lists of any and all units on each tile
        self.unit = [[[] for _ in range(len(terrain[x]))] for x in range(len(terrain))]