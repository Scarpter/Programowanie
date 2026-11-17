from dataclasses import dataclass
import matplotlib.pyplot as plt

from species import Creature, Prey, Predator


@dataclass
class HistoryElement:
    prey: int
    predators: int

class Population:

    def __init__(self, population_data: dict, **species_params):
        """population_data: {klasa: liczba}
           species_params: {klasa: {nazwa_parametru: wartość}} – opcjonalne nadpisania."""
        self._instances: set[Creature] = set()
        for cls, n in population_data.items():
            params = species_params.get(cls, {})
            for _ in range(n):
                self._instances.add(cls(**params))
        self.history = [self._count()]

    def _count(self) -> HistoryElement:
        prey = sum(1 for c in self._instances if isinstance(c, Prey))
        pred = sum(1 for c in self._instances if isinstance(c, Predator))
        return HistoryElement(prey=prey, predators=pred)

    @property
    def n(self) -> HistoryElement:
        return self._count()

    def hunting(self):
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
        steps = range(len(self.history))
        prey = [h.prey for h in self.history]
        pred = [h.predators for h in self.history]

        plt.plot(steps, prey, label="Prey")
        plt.plot(steps, pred, label="Predator")
        plt.xlabel("Krok symulacji")
        plt.ylabel("Liczebność")
        plt.title("Historia populacji")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()

    def plot_histogram(self, attr: str):
        """Histogram wartości atrybutu (np. 'p_reproduce') dla aktualnej populacji."""
        values = [getattr(c, attr) for c in self._instances
                  if hasattr(c, attr)]
        if not values:
            print(f"Brak osobników z atrybutem '{attr}'.")
            return
        plt.hist(values, bins=10, edgecolor="black")
        plt.xlabel(attr)
        plt.ylabel("Liczba osobników")
        plt.title(f"Histogram atrybutu '{attr}'")
        plt.grid(True, alpha=0.3)
        plt.show()