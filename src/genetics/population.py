import math
import typing as t
import src.genetics.utils as utils
from copy import deepcopy
from .chromosome import Chromosome


class Population:
    @property
    def size(self) -> int:
        """Population size."""
        return self._size

    @property
    def global_best(self) -> Chromosome:
        """Global best chromosome."""
        return self._global_best

    @property
    def local_best(self) -> Chromosome:
        """Local best chromosome (for last evaluation)."""
        return self._local_best

    @property
    def best_chromosomes(self) -> t.List[Chromosome]:
        """Best of local bests."""
        return self._best_chromosomes

    def __init__(
        self,
        size: int,
        mutation_rate: float,
        initial_chromosomes: t.Optional[t.List[Chromosome]] = None,
        keep_best_chromosomes: bool = True,
        **kwargs,
    ) -> None:
        """Population base class.

        Args:
            size (int): Population size.
            mutation_rate (float): Mutation rate in `[0, 1]` range.
            initial_chromosomes (t.Optional[t.List[Chromosome]], optional): Initial chromosomes. If None, then init with random chromosomes. Defaults to None.
            keep_best_chromosomes (bool): Keep local bests on each evaluation. Defaults to True.
        """
        self._size = size
        self._mutation_rate = mutation_rate
        if not initial_chromosomes:
            assert "value_range" in kwargs
            assert "length" in kwargs
            self._value_range = kwargs["value_range"]
            self._length = kwargs["length"]
            self.chromosomes = self._rand_chromosomes()
        else:
            self.chromosomes = initial_chromosomes
        self._global_best = deepcopy(self.chromosomes[0])
        self.keep_best_chromosomes = keep_best_chromosomes
        self._best_chromosomes = []

    def _rand_chromosomes(self) -> t.List[Chromosome]:
        """Generate random chromosomes."""
        return [
            Chromosome(self._length, value_range=self._value_range)
            for _ in range(self._size)
        ]

    def eval(self, fitness_fn: t.Callable[[t.List[int]], float]) -> None:
        """Evaluate all chromosomes with given function.

        Args:
            fitness_fn (t.Callable[[t.List[int], float]]): Fitness function to evaluate.
        """
        # ? apply fitnes function to all
        self._local_best = self.chromosomes[0]
        for c in self.chromosomes:
            c.apply_fitness_fn(lambda c: fitness_fn(c.to_list()))
            if c.fitness > self._local_best.fitness:
                self._local_best = c
        if self._local_best.fitness > self.global_best.fitness:
            self._global_best = deepcopy(self._local_best)
        if self.keep_best_chromosomes:
            self._best_chromosomes.append(deepcopy(self._local_best))

    def update(self) -> None:
        """Update all chromosomes for its' current states."""
        # apply natural selection
        mating_pool: t.List[Chromosome] = []
        for c in self.chromosomes:
            n = math.floor((c.fitness / self._local_best.fitness) * 100)
            mating_pool.extend([c for _ in range(n)])
        # create next generation
        pool_size = len(mating_pool) - 1
        for i in range(self._size):
            c1 = mating_pool[utils.random_state.randint(0, pool_size)]
            c2 = mating_pool[utils.random_state.randint(0, pool_size)]
            child = c1.crossover(c2)
            child.mutate(self._mutation_rate)
            self.chromosomes[i] = child
