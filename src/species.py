"""Module with definitions of considered species"""
import random

class Creature:

    alive: bool = True

    def __init__(self, p_death: float, p_reproduce: float):
        self.p_death = p_death
        self.p_reproduce = p_reproduce

    def kill(self):
        """Kills (i.e. alive=False) the creature with probability p_death"""
        if random.random() < self.p_death:
            self.alive = False

    def reproduce(self):
        """Returns new instance of Creature with probability p_reproduce (otherwise None)"""

        if self.alive and (random.random() < self.p_reproduce):

            # 1. Consider changing p_death, p_reproduce to have instances different from the parent
            return self.__class__(p_death=self.p_death, p_reproduce=self.p_reproduce)

        return None

    # TODO: Implement it as descriptors
    @property
    def p_death(self):

        return self.__p_death

    @p_death.setter
    def p_death(self, value):

        # Makes sure that 0 <= value <= 1
        value = min(1.0, max(0.0, value))

        self.__p_death = value

    @property
    def p_reproduce(self):

        return self.__p_reproduce

    @p_reproduce.setter
    def p_reproduce(self, value):

        # Makes sure that 0 <= value <= 1
        value = min(1.0, max(0.0, value))

        self.__p_reproduce = value


class Prey(Creature):
    pass


class Predator(Creature):
    pass