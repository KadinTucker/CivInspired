import random

TILE_ICONS = "I J F S T g p u d h M O o".split()
TILE_NAMES = "Ice Jungle Forest Scrubland Taiga Grassland Plains Tundra Desert Hill Mountain Coast Ocean".split()
TILE_YIELDS = [(0, 0, 0), (1, 1, 0), (1, 2, 0), (1, 2, 0), (1, 2, 0), (2, 0, 1), (1, 1, 1), (1, 0, 1), (0, 1, 0), (1, 1, 0), (0, 2, 0), (1, 0, 2), (0, 0, 2)]

RESOURCE_CATEGORY_NAMES = "Foodstuffs Livestock Lumber Mineral Strategic Luxury Simple".split()

FINAL_RESOURCE_NAMES = "Food Materials Wheat Maize Rice Potatoes Bananas Cattle Sheep Swine Llama Bison Game Fish Tropical_Wood Timber Stone Ore Horse Iron Niter Coal Rubber Oil Aluminium Uranium Cocoa Sugar Spices Dyes Furs Ivory Silks Wines Cotton Gold Gems Whales Pearls".split()
RESOURCE_CATEGORIES = [6, 6, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 2, 2, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]

FOOD_RESOURCE = 0
MATERIAL_RESOURCE = 1
RESOURCE_DECAY_RATE = 0.2
REPRODUCTION_COST = 20
RESOURCE_NAMES = "Food Materials".split()
TEMP_CITY_NAMES = "Rome Moscow Babylon Zimbabwe Tokyo Berlin Paris Thebes Tenochtitlan Washington Beijing Athens London Delhi Karakorum".split()

"""
THE TRADING PROCESS
For each resource:
A city puts on the market an export to each other city, referenced by id. 
 - The export is in proportion to the difference in supplies in each city, as well as the relative "favorability" of the export, 
   decided by the commercial strength of the buyer, the "trade distance" between the cities, and any governmental policies that affect it.
After each city has put its exports on the market, each city decides how much of each export it can buy with its available commerce. 
This is done by each city looking at all that the other cities have to offer, and seeing how much it costs at the default price of 2 per individual resource.
The city then buys a fraction of the resources from each exporter relative to how much it can pay, rounded down (it's inefficient.)
"""

class Economy():
    """
    The Economy class comprises all of the cities in the world
    It serves to facilitate imports and exports between all of the cities
    """

    def __init__(self):
        self.cities = []
        self.distance_matrix = [] # A square (for easy access) matrix of distances between cities
        self.export_strength = [] # A list of square matrices, with first index origin and second index destination
        self.total_strength = [] # A list of the sums of each row of export_strength; that is, the total export strength for each origin (exporter). 
        self.export_gradient = [[] for i in range(len(RESOURCE_NAMES))] # Indexed by resource; a list of square matrices
        self.live_export_offer = [[] for i in range(len(RESOURCE_NAMES))] # Indexed by resource; a list of square matrices

    def add_city(self, city):
        self.cities.append(city)
        self.set_distance_matrix()

    def run_economy(self):
        """
        Handles the exports and imports of all cities
        Starts with setting the exports, which is done by setting the export strengths to each destination, and the gradients for each resource
        For each resource, from the export strength and the export gradient for the resource, a certain amount is put on offer. 
        Lastly, for each city, the total amount being exported to that city is determined, and it is reduced by how much money the city can pay. 
        """
        self.set_export_strength()
        for r in range(len(RESOURCE_NAMES)):
            self.set_export_gradient(r)
            self.set_export_offer(r)
        print(self.export_gradient)
        for i in range(len(self.cities)):
            self.import_all_for_city(i)

    def set_distance_matrix(self):
        matrix = []
        for i in range(len(self.cities)):
            matrix.append([])
            
            for j in range(len(self.cities)):
                matrix[i].append(self.cities[i].get_distance_to(self.cities[j]))
        self.distance_matrix = matrix

    def set_export_strength(self):
        """
        TODO: clean up, make affect an existing matrix. 
        """
        strengths = []
        totals = []
        for i in range(len(self.cities)):
            strengths.append([])
            total = 0
            for j in range(len(self.cities)):
                strength = self.get_export_strength(i, j)
                strengths[i].append(strength)
                total += strength
            totals.append(total)
        self.export_strength = strengths
        self.total_strength = totals

    def set_export_gradient(self, resource_id):
        """
        TODO: clean up, make affect an existing matrix.
        """
        gradients = []
        for i in range(len(self.cities)):
            gradients.append([])
            for j in range(len(self.cities)):
                gradients[i].append(self.get_resource_gradient(i, j, resource_id))
        self.export_gradient[resource_id] = gradients

    def set_export_offer(self, resource_id):
        offers = []
        for i in range(len(self.cities)):
            offers.append([])
            for j in range(len(self.cities)):
                offers[i].append(self.get_offer(i, j, resource_id))
        self.live_export_offer[resource_id] = offers

    def get_resource_gradient(self, origin_id, destination_id, resource_id):
        if self.cities[origin_id].population == 0 or self.cities[destination_id].population == 0:
            return 0
        return max(self.cities[origin_id].resource_stock[resource_id] / self.cities[origin_id].population - self.cities[destination_id].resource_stock[resource_id] / self.cities[destination_id].population, 0)

    def get_export_strength(self, origin_id, destination_id):
        """
        The relative favorability of exports from this city to a destination city
        The export strength is an aggregate of:
         - The distance between cities (more = less movement)
         - The commercial ability of the buyer (destination)
        """
        if origin_id == destination_id:
            return 0
        conductance = max(self.cities[destination_id].commerce // 2, 0)
        resistance = self.distance_matrix[origin_id][destination_id]
        return conductance / resistance
    
    def get_offer(self, origin_id, destination_id, resource_id):
        """
        The amount of actual resource that flows along a density gradient is given by:
         - P2 G, where P2 is the destination population and G is the size of the gradient
         - It is divided by the distance between the cities, to represent the difficulty created by distances
           - It should be divided by at least 2, to ensure that there is no underdamped oscillation in the flow
         - And is then in turn modified by the relative export strength, being the fraction of export strength 
           from the origin to the destination of the total from that origin. 
        """
        if self.total_strength[origin_id] == 0:
            return 0
        return self.export_strength[origin_id][destination_id] / self.total_strength[origin_id] * self.export_gradient[resource_id][origin_id][destination_id] * self.cities[destination_id].population / max(2, self.distance_matrix[origin_id][destination_id]) 

    def transfer_resource(self, amount, origin_id, destination_id, resource_id):
        """
        Transfers an amount of a resource from one city to another,
        and exchanges commerce.
        It costs 2 commerce per resource to import resources, and the exporter gets 1 commerce per resource.
        This function should only be used once all trade parameters have been determined this turn
        """
        self.cities[destination_id].resource_stock[resource_id] += amount 
        self.cities[origin_id].resource_stock[resource_id] -= amount 
        self.cities[destination_id].commerce -= 2 * amount # commerce used to buy comes from actual store
        self.cities[origin_id].commerce_income += amount # commerce gained from sales is incoming and does not decay before the next turn
        if amount > 0:
            print("%s bought %s %s, spending %s commerce, from %s." % (self.cities[destination_id].name, amount, RESOURCE_NAMES[resource_id], amount * 2, self.cities[origin_id].name))

    def import_all_for_city(self, city_id):
        """
        Determines what the city imports from the available export offers
        If the city has enough money, it imports everything
        Otherwise, if the city doesn't have enough money, it imports as much as it can, 
        in proportion to all that is offered by each city on each resource
        This function should only be used once all trade parameters have been determined this turn
        """
        total_imports = 0
        for i in range(len(self.cities)):
            for r in range(len(RESOURCE_NAMES)):
                total_imports += self.live_export_offer[r][i][city_id]
        if total_imports == 0:
            fraction_bought = 0
        else:
            fraction_bought = max(min(1.0, self.cities[city_id].commerce / total_imports / 2), 0)

        for i in range(len(self.cities)):
            for r in range(len(RESOURCE_NAMES)):
                self.transfer_resource(int(fraction_bought * self.live_export_offer[r][i][city_id]), i, city_id, r)


class City():

    def __init__(self, x, y, id, name):
        self.x = x
        self.y = y
        self.id = id
        self.name = name

        self.population = 1
        self.starving = 0 # starving citizens should not continue to starve, or they will die. They also do not reproduce. 
        self.reproduction_progress = 0 # reproduction happens exponentially: each non-starving population adds one to the box, while each starving citizen takes away two from the box. If and when the box fills, the population increases. 

        self.production = 0

        self.resource_stock = [0 for _ in range(len(RESOURCE_NAMES))]
        self.commerce = 0 # idea: commerce goes away at the end of a turn resolution, but banking, currency give benefits that help to keep it. 
        self.commerce_income = 0

        self.income = [random.randint(0, 5), random.randint(0, 5), random.randint(0, 5)]

    def work_temp(self):
        self.resource_stock[FOOD_RESOURCE] += self.income[0] * self.population
        self.resource_stock[MATERIAL_RESOURCE] += self.income[1] * self.population
        self.commerce += self.income[2] * self.population

    def work_tile(self, tile_id):
        self.resource_stock[FOOD_RESOURCE] += TILE_YIELDS[tile_id][0]
        self.resource_stock[MATERIAL_RESOURCE] += TILE_YIELDS[tile_id][1]
        self.commerce += TILE_YIELDS[tile_id][2]

    def get_distance_to(self, destination):
        """
        Gets the distance to another city
        For now, just uses manhattan distance
        For the future, distance can take into account whether the two are connected, 
            the shortest valid land route, the shortest valid sea route, etc... 
        """
        return abs(self.x - destination.x) + abs(self.y - destination.y)

    def get_export_strength(self, destination):
        """
        The relative favorability of exports from this city to a destination city
        The export strength is an aggregate of:
         - The distance between cities (more = less movement)
         - The commercial ability of the buyer (destination)
        """
        if self == destination:
            return 0
        conductance = max(destination.commerce // 2, 0)
        resistance = self.get_distance_to(destination)
        return conductance / resistance
    
    def set_exports(self, all_cities):
        """
        The city exports its stuff to all other cities. 
        The amount exported to each city is due to:
         - The relative export strength to the destination compared to the total export strength to all cities
         - The gradient in resource density by population
        The amount of actual resource that flows along a density gradient is given by:
         - P2 G, where P2 is the destination population and G is the size of the gradient
         - This should be divided by 2, to ensure that there is no underdamped oscillation in the flow
         - It is furthermore divided by the distance between the cities, to account for difficulty of travelling so far
         - And is then in turn modified by the relative export strength. 
        TODO: make exports happen with more than just food gorf
        """
        export_gradients = []
        export_strengths = []
        total_export_strength = 0
        for i in range(len(all_cities)):
            gradient = max(self.food_stock / self.population - all_cities[i].food_stock / all_cities[i].population, 0)
            export_gradients.append(gradient)
            strength = self.get_export_strength(all_cities[i])
            export_strengths.append(strength)
            total_export_strength += strength
        for j in range(len(all_cities)):
            export_amount = export_strengths[j] / total_export_strength * export_gradients[j] * all_cities[j].population // 2
            self.food_exports[j] = export_amount

    def print_report(self):
        print(self.name)
        print("Population: %s" % self.population)
        for i in range(len(self.resource_stock)):
            print("%s: %s (+%s)" % (RESOURCE_NAMES[i], self.resource_stock[i], self.income[i] * self.population))
        print("Commerce: %s (+%s)" % (self.commerce, self.income[2] * self.population))

    def resolve_food(self):
        """
        After all trading is done, food is resolved:
         - Incoming food is added to the amount of food present
         - The population each eat two food units, including starving citizens
         - If the amount of food left over is less than 0, that many starving citizens are created.
         - If the number of starving citizens is greater than half the population, then a citizen dies instead. 
         - With some advancements (government, tech), this can be lessened to only killing a citizen when the number is greater than all. 
        """
        self.resource_stock[FOOD_RESOURCE] -= 2 * self.population
        if self.resource_stock[FOOD_RESOURCE] < 0:
            self.starving -= self.resource_stock[FOOD_RESOURCE]
            # Death by starving: maybe it doesn't happen unless, Civ style, the reproduction box is less than empty
            # if self.starving_citizens > self.population // 2:
            #     self.starving_citizens -= (self.starving_citizens - self.population // 2)
            #     self.population -= (self.starving_citizens - self.population // 2)
            self.resource_stock[FOOD_RESOURCE] = 0
        else:
            self.starving = 0

    def resolve_materials(self):
        """
        Each citizen wants to use materials to work on things.
        Both materials and the citizen using them are needed to produce production. 
        [In extreme cases, citzens can produce materials through sheer labor]
        """
        if self.resource_stock[MATERIAL_RESOURCE] >= self.population:
            self.resource_stock[MATERIAL_RESOURCE] -= self.population
            self.production += self.population
        else:
            self.production += self.resource_stock[MATERIAL_RESOURCE]
            self.resource_stock[MATERIAL_RESOURCE] = 0

    def resolve_commerce(self):
        """
        Before researching Currency, say, commerce produced locally can't be stored long term. 
        [idea] After Currency, it can be kept. After Banking, it even produces interest.
        Only commerce from trade can be stored. 
        Thus, commerce left over after trading is lost forever. 
        Hopefully the city actually uses it before then 
        For now, this is the default behaviour. 
        """
        self.commerce = self.commerce_income
        self.commerce_income = 0

    def reproduce(self):
        """
        The city's population reproduces, and maybe grows in population
        """
        self.reproduction_progress += self.population
        self.reproduction_progress -= 3 * self.starving
        if self.reproduction_progress > REPRODUCTION_COST:
            print("%s Grew from size %s to size %s." % (self.name, self.population, self.population + 1))
            self.population += 1
            self.reproduction_progress = 0 # Doesn't wrap over, just to slow it down a bit
        elif self.reproduction_progress < 0: # Starvation! 
            self.population -= 1
            self.reproduction_progress = 0
        # TODO: if the city goes below 0 population, it is destroyed. 
    
    def decay_resources(self):
        """
        All the resources the city has decay a bit
        If the city has more resources than it can use, this might just happen
        """
        for r in range(len(RESOURCE_NAMES)):
            self.resource_stock[r] -= int(RESOURCE_DECAY_RATE * self.resource_stock[r])

    def resolve_turn(self):
        """
        After trade has been resolved, the city resolves its own stuff
        """
        self.resolve_food()
        self.resolve_materials()
        self.resolve_commerce()
        self.decay_resources()
        self.reproduce()