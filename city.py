import random

TILE_ICONS = "I J F S T g p u d h M O o".split()
TILE_NAMES = "Ice Jungle Forest Scrubland Taiga Grassland Plains Tundra Desert Hill Mountain Coast Ocean".split()
TILE_YIELDS = [(0, 0, 0), (1, 1, 0), (1, 1, 0), (1, 1, 0), (1, 1, 0), (2, 0, 1), (1, 1, 1), (1, 0, 1), (0, 1, 1),
               (0, 2, 0), (0, 1, 0), (1, 0, 2), (0, 0, 2)]

RESOURCE_CATEGORY_NAMES = "Foodstuffs Livestock Lumber Mineral Strategic Luxury Simple".split()

FINAL_RESOURCE_NAMES = "Food Materials Wheat Maize Rice Potatoes Bananas Cattle Sheep Swine Llama Bison Game Fish Tropical_Wood Timber Stone Ore Horse Iron Niter Coal Rubber Oil Aluminium Uranium Cocoa Sugar Spices Dyes Furs Ivory Silks Wines Cotton Gold Gems Whales Pearls".split()
RESOURCE_CATEGORIES = [6, 6, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 2, 2, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5,
                       5, 5, 5, 5, 5, 5, 5]

FOOD_RESOURCE = 0
MATERIAL_RESOURCE = 1
RESOURCE_DECAY_RATE = 0.2
RESOURCE_NAMES = "Food Materials".split()
TEMP_CITY_NAMES = "London Paris Berlin Toledo Rome Moscow Athens Damascus Babylon Mecca Memphis Delhi Samarkand Beijing Shanghai Guangzhou Seoul Kyoto Bangkok Malacca Jakarta Sydney Manila Khartoum Axum Zanzibar Ulundi Kinshasa Kano Timbuktu Toronto Vancouver Philadelphia Chicago SanFrancisco Atlanta Tenochtitlan Palenque Cusco RiodeJaneiro BuenosAires".split()

DIRECTIONS = [(0, 0), (1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1)]
"""
7 3 8
4 0 1
6 2 5
"""

BORDER_EXPAND_CULTURE_COST = 10
PASSIVE_MIGRATION_COST = 100
PHILOSOPHY_COST = 4
MUSTER_COST = 10

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

"""
ORDER OF PROCESSES
 - PRODUCTION PHASE
1. All cities reset income (from last turn)
2. All cities generate resources
3. All cities consume resources
 - TRADE PHASE
4. The wider Economy runs
 - RESOLUTION PHASE
4. All cities resolve leftover and import yields
5. All cities experience migration
6. All cities resolve commerce
7. All cities resolve culture
8. All cities resolve science
"""


class Economy:
    """
    The Economy class comprises all of the cities in the world
    It serves to facilitate imports and exports between all of the cities
    """

    def __init__(self):
        self.cities = []
        self.distance_matrix = []  # A square (for easy access) matrix of distances between cities
        self.export_strength = []  # A list of square matrices, with first index origin and second index destination
        self.total_strength = []  # A list of the sums of each row of export_strength; that is, the total export strength for each origin (exporter).
        self.export_gradient = [[] for i in range(len(RESOURCE_NAMES))]  # Indexed by resource; a list of square matrices
        self.live_export_offer = [[] for i in range(len(RESOURCE_NAMES))]  # Indexed by resource; a list of square matrices

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
        return max(self.cities[origin_id].resource_stock[resource_id] / self.cities[origin_id].population -
                   self.cities[destination_id].resource_stock[resource_id] / self.cities[destination_id].population, 0)

    def get_export_strength(self, origin_id, destination_id):
        """
        The relative favourability of exports from this city to a destination city
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
        return (self.export_strength[origin_id][destination_id] / self.total_strength[origin_id]
                * self.export_gradient[resource_id][origin_id][destination_id]
                * self.cities[destination_id].population / max(2, self.distance_matrix[origin_id][destination_id]))

    def transfer_resource(self, amount, origin_id, destination_id, resource_id):
        """
        Transfers an amount of a resource from one city to another,
        and exchanges commerce.
        It costs 2 commerce per resource to import resources, and the exporter gets 1 commerce per resource.
        This function should only be used once all trade parameters have been determined this turn
        """
        self.cities[destination_id].import_resource(resource_id, amount)
        self.cities[origin_id].export_resource(resource_id, amount)
        if amount > 0:
            print("%s bought %s %s, spending %s commerce, from %s."
                  % (self.cities[destination_id].name, amount,
                     RESOURCE_NAMES[resource_id], amount * 2, self.cities[origin_id].name))

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


class City:

    def __init__(self, x, y, c_id, name):
        self.x = x
        self.y = y
        self.id = c_id
        self.name = name

        # For now, only the 3x3 region centered on the city is usable as territory
        self.territory = [True, False, False, False, False, False, False, False, False]  # see the const DIRECTIONS
        self.territory_size = 1  # a stored value of the number of 'True' in the above

        self.population = 1
        self.starving = 0  # starving citizens should not continue to starve, or they will die.

        self.passive_migration_progress = 0

        self.production_pool = 0

        self.philosophy_pool = 0
        self.muster_pool = 0

        self.resource_stock = [0 for _ in range(len(RESOURCE_NAMES))]

        self.resource_made = [0 for _ in range(len(RESOURCE_NAMES))]
        self.resource_consumed = [0 for _ in range(len(RESOURCE_NAMES))]
        self.resource_imported = [0 for _ in range(len(RESOURCE_NAMES))]
        self.resource_exported = [0 for _ in range(len(RESOURCE_NAMES))]

        self.commerce = 0
        self.commerce_income = 0

        self.income = [random.randint(1, 2), random.randint(0, 2), random.randint(0, 2)]

        self.science_income = 0
        self.culture_income = 0

        self.border_culture = 0

    def make_resource(self, resource, quantity):
        """
        Adds a resource to the stock, and notes that it is made by the city itself.
        """
        self.resource_stock[resource] += quantity
        self.resource_made[resource] += quantity

    def consume_resource(self, resource, quantity):
        self.resource_stock[resource] -= quantity
        self.resource_consumed[resource] += quantity

    def export_resource(self, resource, quantity):
        self.resource_stock[resource] -= quantity
        self.commerce_income += quantity
        self.resource_exported[resource] += quantity

    def import_resource(self, resource, quantity):
        """
        Prepares a resource to be imported
        The resource is first "held", in preparation for yield losses
        Then the resource is added to the stock
        """
        self.commerce -= 2 * quantity
        self.resource_imported[resource] += quantity

    def work_temp(self):
        self.make_resource(FOOD_RESOURCE, self.income[0] * self.population)
        self.make_resource(MATERIAL_RESOURCE, self.income[1] * self.population)
        self.commerce += self.income[2] * self.population

    def work_tile(self, tile_id):
        self.make_resource(FOOD_RESOURCE, TILE_YIELDS[tile_id][0])
        self.make_resource(MATERIAL_RESOURCE, TILE_YIELDS[tile_id][1])
        self.commerce += TILE_YIELDS[tile_id][2]

    def get_border_growth_cost(self):
        return BORDER_EXPAND_CULTURE_COST * (1 + self.population)

    def get_muster_pool_limit(self):
        return self.population * MUSTER_COST

    def get_distance_to(self, destination):
        """
        Gets the distance to another city
        For now, just uses manhattan distance
        For the future, distance can take into account whether the two are connected, 
            the shortest valid land route, the shortest valid sea route, etc... 
        """
        return abs(self.x - destination.x) + abs(self.y - destination.y)

    def get_gross_income(self, resource):
        """
        Returns the "gross income" from the last turn of a resource,
        being total local production plus total imports
        """
        return self.resource_made[resource] + self.resource_imported[resource]

    def get_net_income(self, resource):
        """
        Returns the "net income" from the last turn of a resource,
        being total local production plus total imports, minus exports, minus consumption
        """
        return (self.resource_made[resource] + self.resource_imported[resource]
                - self.resource_exported[resource] - self.resource_consumed[resource])

    def get_appeal(self):
        """
        Calculates the appeal of the city
        Appeal is an aggregate of the amount of excess food and materials the city produces/imports per population,
        as well as the number of unique luxury and bonus resources, and culture.
        Excess means how much more of the food and materials are there than citizens that would consume them.
        For now, only excess food and materials income.
        It can be zero if the city is very short on resources.
        """
        if self.population == 0:
            return 0
        return (self.get_gross_income(FOOD_RESOURCE) + self.get_gross_income(MATERIAL_RESOURCE)) / self.population - 2

    def print_report(self):
        print(self.name)
        print("Population: %s" % self.population)
        print("Production: %s (+%s)" % (self.production_pool, self.get_expected_production()))
        print("Culture: +%s" % self.culture_income)
        print("Science: +%s" % self.science_income)
        print("\t\t\tLocal\tConsumption\tImport\tExport")
        print("Commerce: \t\t+%s\t\t-%s\t\t-%s\t\t+%s" % (self.income[2] * self.population, "--",
                                                          sum(self.resource_imported) * 2, sum(self.resource_exported)))
        for i in range(len(self.resource_stock)):
            print("%s:\t\t+%s\t\t-%s\t+%s\t\t-%s" % (RESOURCE_NAMES[i], self.resource_made[i],
                                                     self.resource_consumed[i], self.resource_imported[i],
                                                     self.resource_exported[i]))
        print("Muster Pool: %s/%s" % (self.muster_pool, self.get_muster_pool_limit()))
        print("Border Expansion: %s/%s" % (self.border_culture, self.get_border_growth_cost()))
        print("Territory: %s" % self.territory_size)
        print("Growth Progress: %s/%s" % (self.passive_migration_progress, PASSIVE_MIGRATION_COST))

    def get_expected_production(self):
        return min(self.resource_stock[MATERIAL_RESOURCE] + self.resource_made[MATERIAL_RESOURCE], self.population)

    def resolve_passive_migration(self):
        """
        Resolves migrants moving and assimilating to the city and/or passive city growth
        Works through the product of appeal and the amount of territory more than the population size
        Once the progress exceeds a threshold, the city gains a population and the counter is reset
        A city cannot grow more than once per turn this way,
        and the amount of migration progress per turn cannot exceed the cost of migrating.
        """
        self.passive_migration_progress += int(min(max(0, self.territory_size - self.population) * self.get_appeal(),
                                                   PASSIVE_MIGRATION_COST))
        if self.passive_migration_progress >= PASSIVE_MIGRATION_COST:
            self.population += 1
            print("%s has grown to size %s" % (self.name, self.population))
            self.passive_migration_progress -= PASSIVE_MIGRATION_COST

    def resolve_food(self):
        """
        After all trading is done, food is resolved:
         - Incoming food is added to the amount of food present
         - The population each eat two food units, including starving citizens
         - If the amount of food left over is less than 0, that many starving citizens are created.
         - If the number of starving citizens is greater than half the population, then a citizen dies instead. 
         - With some advancements (government, tech), this can be lessened to only killing a citizen when the number is greater than all. 
        """
        self.resource_stock[FOOD_RESOURCE] -= self.population
        if self.resource_stock[FOOD_RESOURCE] < 0:
            self.starving -= self.resource_stock[FOOD_RESOURCE]
            self.resource_stock[FOOD_RESOURCE] = 0
        else:
            self.starving = 0

    def resolve_materials(self):
        """
        Each citizen wants to use materials to work on things.
        Both materials and the citizen using them are needed to produce production. 
        [In extreme cases, citizens can produce materials through sheer labor]
        """
        if self.resource_stock[MATERIAL_RESOURCE] >= self.population:
            self.resource_stock[MATERIAL_RESOURCE] -= self.population
            self.production_pool += self.population
        else:
            self.production_pool += self.resource_stock[MATERIAL_RESOURCE]
            self.resource_stock[MATERIAL_RESOURCE] = 0

    def resolve_commerce(self):
        """
        Before researching Currency, say, commerce produced locally can't be stored long term. 
        [idea] After Currency, it can be kept. After Banking, it even produces interest.
        Only commerce from trade can be stored. 
        Thus, commerce left over after trading is lost.
        Returns the amount of commerce lost this way.
        """
        commerce_lost = self.commerce
        self.commerce = self.commerce_income
        self.commerce_income = 0
        return commerce_lost

    def expand_border_randomly(self):
        indices = [i for i in range(9)]
        random.shuffle(indices)
        for i in indices:
            if not self.territory[i]:
                self.territory[i] = True
                self.territory_size += 1
                print("The borders of %s have grown." % self.name)
                break

    def resolve_leftovers(self):
        """
        After trade, leftover resources are either allocated to storage, or lost
        When resources are lost, they are converted to "philosophy" points or "muster" points
        Leftover commerce is worth double
        [idea] Initially, muster points are the priority, and philosophy points are accumulated
        only when the muster box is full.
        Later technology might allow for different allocation
        [idea] Instead, make it happen in two steps: excess resources are turned into commerce,
        and then that commerce is turned into philosophy if not otherwise used.
        """
        total_excess = 2 * self.resolve_commerce()
        for r in range(len(RESOURCE_NAMES)):
            total_excess += self.resource_stock[r]
            self.resource_stock[r] = self.resource_imported[r]
        self.muster_pool += total_excess
        if self.muster_pool > MUSTER_COST:
            self.philosophy_pool += self.muster_pool - MUSTER_COST
            self.muster_pool = MUSTER_COST
        self.resolve_philosophy()

    def resolve_philosophy(self):
        """
        Resolves the philosophy pool in the city
        From all lost excess resources, people "think" and philosophise,
        which causes culture and science to be accumulated
        """
        total_philosophy = self.philosophy_pool // PHILOSOPHY_COST
        self.culture_income += total_philosophy
        self.science_income += total_philosophy
        actual_philosophy = total_philosophy * PHILOSOPHY_COST
        self.philosophy_pool -= actual_philosophy

    def resolve_culture(self):
        """
        Turns culture production into actual culture
        For now, only adds culture to the border growth counter.
        In future, it will also add this to a moving average of culture
        Also grows the borders.
        For now, the borders grow randomly if culture exceeds a threshold
        In future, the player will choose how the border should grow
        and the cost will increase a lot with distance.
        [idea] The effect of culture is reduced with the population.
        The effective culture is actually culture / population
        """
        self.border_culture += self.culture_income
        if self.border_culture >= self.get_border_growth_cost():
            self.border_culture -= self.get_border_growth_cost()
            self.expand_border_randomly()

    def reset_income(self):
        """
        Resets all records of the amount made and imported of resources to zero
        """
        self.culture_income = 0
        self.science_income = 0
        for r in range(len(RESOURCE_NAMES)):
            self.resource_made[r] = 0
            self.resource_imported[r] = 0
            self.resource_exported[r] = 0

    def run_production_phase(self):
        """
        The city starts its turn by resetting its past income, making resources locally, and consuming resources
        """
        self.reset_income()
        self.work_temp()
        self.resolve_food()
        self.resolve_materials()

    def run_resolution_phase(self):
        """
        After trade has been resolved, the city resolves its leftover resources and commerce.
        Then, migration, culture, and science are resolved.
        """
        self.resolve_leftovers()
        self.resolve_passive_migration()
        self.resolve_culture()
