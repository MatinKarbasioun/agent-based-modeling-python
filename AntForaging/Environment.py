import random

from AntForaging.Ant import Ant


class Location:
    """The grid recording the food and pheromone."""

    def __init__(self):
        self.food = 0
        self.pheromone = 0

    def place_food(self, p):
        """Place food with probability p into this Location."""
        if random.random() < p:
            self.food = 1

    def has_food(self):
        """Returns True if this Location has at least 1 food in it,
        False otherwise.
        """
        return self.food > 0

    def remove_food(self):
        """Remove one food from this Location. Crashes if there is
        no food in this Location.
        """
        assert self.has_food
        self.food -= 1

    def add_pheromone(self, amount=1):
        """Add pheromone to this Location."""
        self.pheromone += amount

    def set_pheromone(self, amount):
        """Set the pheromone in this Location to amount."""
        self.pheromone = amount

    def get_pheromone(self):
        """Returns the amount of pheromone in this Location."""
        return self.pheromone

    def evaporate_pheromone(self):
        """Evaporates 1/30 of the pheromone in this Location."""
        self.pheromone -= self.pheromone * (1.0 / 30)


class Model:
    """Class that represents the room the robot ants live in	"""

    MAX_ANTS = 200

    def __init__(self):
        self.ants = {}
        self.locations = {}
        self.p_food = 0

    def place_food(self, p):
        """Place food in all Locations with probability p."""
        self.p_food = p
        for point in self.locations:
            point.place_food(p)

    def remove_food(self, pos):
        """Remove one unit of food from the Location at pos."""
        self.locations[pos].remove_food()

    def has_food(self, pos):
        """Returns true if the Location at pos has at least one unit
        of food, false otherwise.
        """
        return self.get_location(pos).has_food()

    def add_ants(self, n):
        """Add n ants to the nest. Each ant starts at (0,0)"""
        for i in range(n):
            ant = Ant(self)
            pos = (ant.x, ant.y)
            if pos in self.ants:
                self.ants[pos].append(ant)
            else:
                self.ants[pos] = [ant]

    def __repr__(self):
        """Return a string representation of this room."""
        return str(self.ants)

    def move_ants(self):
        """Iterate through and move all the Ants in the room."""
        ants = []
        for pos, antlist in self.ants.items():
            for ant in antlist:
                ant.move()
                ants.append(ant)
        self.evaporate_pheromone()
        d = {}
        for ant in ants:
            pos = (ant.x, ant.y)
            if pos in d:
                d[pos].append(ant)
            else:
                d[pos] = [ant]
        self.ants = d

    def get_location(self, pos):
        """Returns the Location at pos, creating it if it doesn't
        already exist.
        """
        if pos not in self.locations:
            loc = Location()
            self.locations[pos] = loc
            if self.p_food > 0:
                loc.place_food(self.p_food)
        else:
            loc = self.locations[pos]
        return loc

    def add_pheromone(self, pos, amount=1):
        """Adds amount pheromone to the Location at pos."""
        self.get_location(pos).add_pheromone(amount)

    def get_pheromone(self, pos):
        """Returns the amount of pheromone in the Location at pos."""
        return self.get_location(pos).get_pheromone()

    def set_pheromone(self, pos, amount):
        """Sets the amount of pheromone in the Location at pos to
        amount.
        """
        self.get_location(pos).set_pheromone(amount)

    def evaporate_pheromone(self):
        """Evaporates pheromone from all existing Locations."""
        for pos, loc in self.locations.items():
            loc.evaporate_pheromone()

    def num_ants(self, pos):
        """Returns the number of Ants at pos."""
        if pos in self.ants:
            return len(self.ants[pos])
        else:
            return 0

    def at_capacity(self, pos):
        """Returns True if the Location at pos is full of Ants,
        False otherwise.
        """
        return self.num_ants(pos) >= Model.MAX_ANTS

