from dataclasses import dataclass
import matplotlib.pyplot as plt

from species import Creature, Prey, Predator


@dataclass
class HistoryElement:
    """Struktura przechowująca stan populacji w jednym kroku symulacji."""
    prey: int
    predators: int

class Population:

    def __init__(self, population_data: dict):
        #population_data: {klasa: liczba}
        self._instances: list[Creature] = []
        #Przechowanie w liście bo inaczej seed nie działa
        for cls, n in population_data.items():
            for _ in range(n):
                self._instances.append(cls())
        self.history = [self._count()]

    def _count(self) -> HistoryElement:
        #Zlicza osobniki każdego gatunku i zwraca je jako HistoryElement
        prey = sum(1 for c in self._instances if isinstance(c, Prey))
        pred = sum(1 for c in self._instances if isinstance(c, Predator))
        return HistoryElement(prey=prey, predators=pred)

    @property
    def n(self) -> HistoryElement:
        return self._count()

    def hunting(self):
        #Polowanie poprzez stworzenie listy żywych drapieżników i ofiar, a następnie
        #parowanie ich 1:1
        predators = [c for c in self._instances
                     if isinstance(c, Predator) and c.alive]
        preys = [c for c in self._instances
                 if isinstance(c, Prey) and c.alive]
        for predator, prey in zip(predators, preys):
            predator.hunt(prey)


    def natural_selection(self):
        #Funkcja przeprowadza jeden krok stymulacji
        newborns = []
        #  Reprodukcja wszystkich żyjących organizmów
        for creature in list(self._instances):
            if creature.alive:
                child = creature.reproduce()
                if child is not None:
                    newborns.append(child)

        self.hunting()

        for creature in list(self._instances):
            if creature.alive:
                creature.kill()
        #Aktualizacja zbioru żyjących organizmów i reset głodu
        self._instances = [c for c in self._instances if c.alive]
        for c in self._instances:
            if isinstance(c, Predator):
                c.hungry = True
        self._instances.extend(newborns)
        self.history.append(self._count())

    def plot_history(self):
        #Tworzenie wykresu
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
        #Histogram wartości atrybutu (np. 'p_reproduce') dla aktualnej populacji.
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