import typing as t
import src.genetics.utils as utils


class Gene:
    @property
    def value(self) -> int:
        """Current value of the gene."""
        return self._value

    @property
    def value_range(self) -> t.Tuple[int, int]:
        """Value range for the range."""
        return self._value_range

    def __init__(
        self,
        value_range: t.Tuple[int, int],
        initial_value: t.Optional[int] = None,
    ) -> None:
        """Gene base class.

        Args:
            value_range (t.Tuple[int, int]): Value range in `[min, max)` order.
            initial_value (t.Optional[int], optional): Initial value. If None, then init with a random value. Defaults to None.
        """
        assert value_range[0] < value_range[1]
        self._value_range = value_range
        if initial_value:
            a, b = value_range
            assert a <= initial_value <= b
            self._value = initial_value
        else:
            self._value = self._rand_value()

    def __repr__(self) -> str:
        return str(self.value)

    def _rand_value(self) -> int:
        """Generate random value."""
        a, b = self._value_range
        return utils.random_state.choice(range(a, b))

    def randomize(self) -> None:
        """Randomize current value."""
        self._value = self._rand_value()
