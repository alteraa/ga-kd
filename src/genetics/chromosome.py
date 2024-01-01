import typing as t
import src.genetics.utils as utils
from .gene import Gene


class Chromosome:
    @property
    def fitness(self) -> float:
        """Current fitness value for the chromosome."""
        return self._fitness

    @property
    def genes(self) -> t.List[Gene]:
        """List of current genes."""
        return self._genes

    @property
    def length(self) -> int:
        """Number of genes."""
        return self._length

    def __init__(
        self,
        length: int,
        initial_genes: t.Optional[t.List[Gene]] = None,
        **kwargs,
    ) -> None:
        """Chromosome base class.

        Args:
            length (int): Number of genes (ie. chromosome length).
            initial_genes (t.Optional[t.List[Gene]], optional): Initial genes. If None, then initialize with random genes. Defaults to None.
        """
        assert length > 0
        self._length = length
        if not initial_genes:
            assert "value_range" in kwargs
            self._value_range = kwargs["value_range"]
            self._genes = self._rand_genes()
        else:
            self._genes = initial_genes
        self._fitness = 0

    def __repr__(self) -> str:
        return str(self._genes)

    def _rand_genes(self) -> t.List[Gene]:
        """Generate random genes."""
        return [Gene(self._value_range) for _ in range(self._length)]

    def to_list(self) -> t.List[int]:
        """Convert gene values to list."""
        return [g.value for g in self._genes]

    def apply_fitness_fn(self, fn: t.Callable[["Chromosome"], float]) -> None:
        """Apply fitness function. After applying, updates its current fitness value.

        Args:
            fn (t.Callable[[&quot;Chromosome&quot;], float]): Fitness function.
        """
        self._fitness = fn(self)

    def mutate(self, rate: float) -> None:
        """Mutation operator.

        Args:
            rate (float): Mutation rate in `[0, 1]`.
        """
        for gene in self._genes:
            if utils.random_state.random() < rate:
                gene.randomize()

    def crossover(self, other: "Chromosome") -> "Chromosome":
        """Crossover operator.

        Args:
            other (Chromosome): Other chromosome to crossover.

        Returns:
            Chromosome: New (child) chromosome.
        """
        child_genes = []
        mid_point = utils.random_state.randint(0, self._length)
        for i in range(self._length):
            if i < mid_point:
                child_genes.append(self._genes[i])
            else:
                child_genes.append(other.genes[i])
        return Chromosome(self._length, child_genes)
