"""Module with definitions of considered species."""
import random


class Creature:
    """Abstrakcyjny organizm z rozrodem i śmiertelnością."""

    p_death = 0.1
    p_reproduce = 0.2

    # Zbiór nazw atrybutów, które mają być walidowane do [0, 1]
    _probability_attrs = {"p_death", "p_reproduce", "p_hunt"}

    def __init__(self, p_death=None, p_reproduce=None):
        if p_death is not None:
            self.p_death = p_death
        if p_reproduce is not None:
            self.p_reproduce = p_reproduce
        self.alive = True

    def __setattr__(self, name, value):
        """Ścina prawdopodobieństwa do [0, 1] – walidator §2B."""
        if name in self._probability_attrs:
            value = min(1.0, max(0.0, float(value)))
        super().__setattr__(name, value)

    def kill(self):
        """Zabija organizm z prawdopodobieństwem p_death."""
        if random.random() < self.p_death:
            self.alive = False

    def reproduce(self):
        """Z prawdopodobieństwem p_reproduce zwraca nowego osobnika."""
        if self.alive and random.random() < self.p_reproduce:
            return self.__class__(
                p_death=self.p_death,
                p_reproduce=self.p_reproduce,
            )
        return None


class Prey(Creature):
    """Ofiara – dodatkowe p_hunt (szansa przeżycia polowania)."""

    def __init__(self, p_death=None, p_reproduce=None, p_hunt=0.3):
        super().__init__(p_death, p_reproduce)
        self.p_hunt = p_hunt

    def reproduce(self):
        if self.alive and random.random() < self.p_reproduce:
            return Prey(
                p_death=self.p_death,
                p_reproduce=self.p_reproduce,
                p_hunt=self.p_hunt,
            )
        return None


class Predator(Creature):
    """Drapieżca – stan 'hungry' i metoda hunt(prey)."""

    p_death_hungry = 0.6

    def __init__(self, p_death=None, p_reproduce=None):
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
            return Predator(
                p_death=self.p_death,
                p_reproduce=self.p_reproduce,
            )
        return None