import city

class Player:

    def __init__(self, p_id):
        self.id = p_id
        self.cities = []
        self.territory = []

    def add_city(self, c):
        self.cities.append(c)
        for t in c.land:
            self.territory.append(t)

    def remove_city(self, c):
        self.cities.remove(c)
        for t in c.land:
            self.territory.remove(t)
