import random
import time
import math
import matplotlib.pyplot as plt


class Ant:
    """A single Ant"""

    def __init__(self, model):
        self.model = model
        self.x = 0
        self.y = 0
        self.has_food = 0

    def next_left(self):
        """The (x, y) position of the Location the Ant
        would move to if it moved forward left.
        """
        if not self.has_food:
            return self.x, self.y + 1
        else:
            return self.x, self.y - 1

    def next_right(self):
        """The (x, y) position of the Location the Ant
        would move to if it moved forward right.
        """
        if not self.has_food:
            return self.x + 1, self.y
        else:
            return self.x - 1, self.y

    def left_pheromone(self):
        """The amount of pheromone in the Location that
        the Ant	would move into if it moved forward left.
        """
        return self.model.get_pheromone(self.next_left())

    def right_pheromone(self):
        """The amount of pheromone in the Location that
        the Ant	would move into if it moved forward right.
        """
        return self.model.get_pheromone(self.next_right())

    def will_move(self):
        """Whether or not this Ant will move this turn."""
        if self.model.at_capacity(self.next_left()) and \
                self.model.at_capacity(self.next_right()):
            return False
        p_l = self.left_pheromone()
        p_r = self.right_pheromone()
        prob_move = 0.5 + 0.5 * math.tanh((p_l + p_r) / 100.0 - 1)
        return random.random() < prob_move

    def will_go_right(self):
        """Whether or not this Ant will move forward right
        this turn.
        """
        p_l = self.left_pheromone()
        p_r = self.right_pheromone()

        if self.model.at_capacity(self.next_right()):
            return False

        if self.model.at_capacity(self.next_left()):
            return True

        prob_right = (1 - (5 + p_l) ** 2 /
                      float((5 + p_l) ** 2 + (5 + p_r) ** 2))

        return random.random() < prob_right

    def move(self):
        """Moves this Ant."""
        if not self.will_move():
            return
        if self.will_go_right():
            (self.x, self.y) = self.next_right()
        else:
            (self.x, self.y) = self.next_left()
        self.lay_pheromone()
        pos = (self.x, self.y)
        if pos == (0, 0):
            self.has_food = False
        else:
            if self.model.has_food(pos) and not self.has_food:
                self.model.remove_food(pos)
                self.has_food = True

    def lay_pheromone(self):
        """This Ant lays pheromone in its current Location."""
        pos = (self.x, self.y)
        current = self.model.get_pheromone(pos)
        if not self.has_food:
            limit = 1000
            amount = 1
        else:
            limit = 300
            amount = 10
        if current >= limit:
            return
        new_amount = min(current + amount, limit)
        self.model.set_pheromone(pos, new_amount)