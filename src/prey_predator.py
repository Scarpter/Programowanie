from dataclasses import dataclass
import matplotlib.pyplot as plt

from species import Creature, Prey, Predator


@dataclass
class HistoryElement:
    prey: int
    predators: int

class Population:

    def __init__(self, population_data: dict):

        self._instances: set[Creature] = set()
        for cls, n in population_data.items():
            for _ in range(n):
                if cls is Prey:
                    self._instances.add(Prey())
                elif cls is Predator:
                    self._instances.add(Predator())
                else:
                    self._instances.add(cls())

        self.history: list[HistoryElement] = [self._count()]

    def _count(self) -> HistoryElement:
        prey = sum(1 for c in self._instances if isinstance(c, Prey))
        pred = sum(1 for c in self._instances if isinstance(c, Predator))
        return HistoryElement(prey=prey, predators=pred)

    @property
    def n(self) -> HistoryElement:
        return self._count()

    def hunting(self, other):
        predators = [c for c in self._instances
                     if isinstance(c, Predator) and c.alive]
        preys = [c for c in self._instances
                 if isinstance(c, Prey) and c.alive]
        for predator, prey in zip(predators, preys):
            predator.hunt(prey)


    def natural_selection(self):
        newborns = []

        for creature in list(self._instances):
            if creature.alive:
                child = creature.reproduce()
                if child is not None:
                    newborns.append(child)

        self.hunting()

        for creature in list(self._instances):
            if creature.alive:
                creature.kill()

        self._instances = {c for c in self._instances if c.alive}
        self._instances.update(newborns)
        self.history.append(self._count())

    def plot_history(self):
        plt.plot(self.history)
        plt.xlabel("Pokolenie")
        plt.ylabel("Liczebność populacji")
        plt.title("Historia populacji")
        plt.show()
