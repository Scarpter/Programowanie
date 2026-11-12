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

        if self.alive and random.random() < self.p_reproduce:

            # 1. Consider changing p_death, p_reproduce to have instances different from the parent
            return self.__class__(p_death=self.p_death, p_reproduce=self.p_reproduce)

        return None



class Prey(Creature):

    p_hunt = 0.2
    def __init__(self, p_death , p_reproduce,
                 p_hunt: float = 0.2):
        super().__init__(p_death, p_reproduce)
        self.p_hunt = p_hunt

    def reproduce(self):
        if self.alive and random.random() < self.p_reproduce:
            return Prey(p_death=self.p_death,
                        p_reproduce=self.p_reproduce,
                        p_hunt=self.p_hunt)
        return None




class Predator(Creature):

    p_death_hungry = 0.9

    def __init__(self, p_death , p_reproduce):
        super().__init__(p_death, p_reproduce)
        self.hungry = True

    def kill(self):

        p = self.p_death_hungry if self.hungry else self.p_death
        if random.random() < p:
            self.alive = False

    def hunt(self, prey: Prey):

        if not self.alive or not prey.alive:
            return
        if random.random() < prey.p_hunt:
            prey.alive = False
            self.hungry = False

    def reproduce(self):
        if self.alive and random.random() < self.p_reproduce:
            return Predator(p_death=self.p_death,
                            p_reproduce=self.p_reproduce)
        return None