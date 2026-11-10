from dataclasses import dataclass
import matplotlib.pyplot as plt

from .species import Creature


@dataclass
class HistoryElement:
    prey: int
    predators: int

class Population:

    _instances: set[Creature]  # Tu będą dwa zbiory (Prey & Predator)
    history: list[int]  # list[HistoryElement]

    def __init__(self, n: int, **kwargs):

        self._instances = set(
            [Creature(**kwargs) for _ in range(n)]
        )

        self.history = [self.n]

    def natural_selection(self):

        for creature in self._instances:
            creature.kill()

        self._instances = set([creature for creature in self._instances if creature.alive])

        self.history.append(self.n)

    def plot_history(self):
        plt.plot(self.history)
        plt.xlabel("Pokolenie")
        plt.ylabel("Liczebność populacji")
        plt.title("Historia populacji")
        plt.show()

    @property
    def n(self):
        return len(self._instances)