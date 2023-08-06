from __future__ import annotations

import math
import random

from beartype import beartype
from beartype.typing import Callable


@beartype
class Scalar:
    """Scalar

    Args:
        data (float | None): defaults to `None`.
        leaf (bool):
        name:
        rate:
        _back:
        _grad:
        _prev:
    """

    def __init__(
        self,
        data: float | None = None,
        leaf: bool = False,
        name: str = "",
        rate: float = 1.0,
        _back: Callable[[], None] | None = None,
        _grad: float = 0.0,
        _prev: set[Scalar] | None = None,
    ) -> None:
        self._back: Callable[[], None] = _back or (lambda: None)
        self._data: float = data if data is not None else random.random()
        self._grad: float = _grad
        self._leaf: bool = leaf
        self._name: str = name
        self._prev: set[Scalar] = _prev or set()
        self._rate: float = rate

    def back(
        self,
        _root: bool = True,
    ) -> None:
        if _root:
            self._grad = 1.0

        self._back()

        for prev_i in self._prev:
            prev_i.back(_root=False)

    def step(
        self,
        rate: float = 1e-3,
    ) -> None:
        if self._leaf:
            return

        self._data += rate * self._rate * self._grad

        for prev_i in self._prev:
            prev_i.step(rate=rate)

    def zero(self) -> None:
        self._grad = 0.0

        for prev_i in self._prev:
            prev_i.zero()

    def __add__(
        self,
        other: Scalar | float,
    ) -> Scalar:
        other = Scalar(other) if isinstance(other, float) else other
        out = Scalar(
            self.data + other.data,
            name=f"({self.name}+{other.name})",
            _prev={self, other},
        )

        def _back() -> None:
            self._grad += out.grad * 1.0
            other._grad += out.grad * 1.0

        out._back = _back

        return out

    def __radd__(
        self,
        other: Scalar | float,
    ) -> Scalar:
        return self + other

    def __sub__(
        self,
        other: Scalar | float,
    ) -> Scalar:
        other = Scalar(other) if isinstance(other, float) else other
        out = Scalar(
            self.data - other.data,
            name=f"({self.name}-{other.name})",
            _prev={self, other},
        )

        def _back() -> None:
            self._grad += out.grad * 1.0
            other._grad += out.grad * (-1.0)

        out._back = _back

        return out

    def __rsub__(
        self,
        other: Scalar | float,
    ) -> Scalar:
        raise NotImplementedError

    def __mul__(
        self,
        other: Scalar | float,
    ) -> Scalar:
        other = Scalar(other) if isinstance(other, float) else other
        out = Scalar(
            self.data * other.data,
            name=f"({self.name}*{other.name})",
            _prev={self, other},
        )

        def _back() -> None:
            self._grad += out.grad * other.data
            other._grad += out.grad * self.data

        out._back = _back

        return out

    def __rmul__(
        self,
        other: Scalar | float,
    ) -> Scalar:
        return self * other

    def __truediv__(
        self,
        other: Scalar | float,
    ) -> Scalar:
        other = Scalar(other) if isinstance(other, float) else other
        out = Scalar(
            self.data / other.data,
            _prev={self, other},
        )

        def _back() -> None:
            self._grad += out.grad * (1.0 / other.data)
            other._grad += out.grad * (self.data * ((-1.0) * math.pow(other.data, -2.0)))

        out._back = _back

        return out

    def __rtruediv__(
        self,
        other: Scalar | float,
    ) -> Scalar:
        raise NotImplementedError

    def __pow__(
        self,
        other: Scalar | float,
    ) -> Scalar:
        other = Scalar(other) if isinstance(other, float) else other
        out = Scalar(
            self.data**other.data,
            _prev={self, other},
        )

        def _back() -> None:
            self._grad = out.grad * (other.data * (self.data ** (other.data - 1.0)))
            other._grad = out.grad * (out.data * math.log(self.data))

        out._back = _back

        return out

    def __rpow__(
        self,
        other: Scalar | float,
    ) -> Scalar:
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"Value(name={self._name}, data={self._data:.4f}, grad={self._grad:.4f})"

    @property
    def data(self) -> float:
        return self._data

    @property
    def grad(self) -> float:
        return self._grad

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(
        self,
        name: str,
    ) -> None:
        self._name = name

    @property
    def rate(self) -> float:
        return self._rate

    @rate.setter
    def rate(
        self,
        rate: float,
    ) -> None:
        self._rate = rate


def relu(inp: Scalar) -> Scalar:
    out = Scalar(
        max(inp.data, 0.0),
        name=f"ReLU({inp.name})",
        _prev={inp},
    )

    def _back() -> None:
        inp._grad += out.grad * (1.0 if out.data > 0.0 else 0.0)

    out._back = _back

    return out


@beartype
def sigmoid(inp: Scalar) -> Scalar:
    if (x := inp.data) > 0.0:
        z = math.exp(-x)
        a = 1.0 / (1.0 + z)
    else:
        z = math.exp(x)
        a = z / (1.0 + z)

    out = Scalar(
        a,
        name=f"sigmoid({inp.name})",
        _prev={inp},
    )

    def _back() -> None:
        inp._grad += out.grad * (out.data * (1.0 - out.data))

    out._back = _back

    return out


@beartype
def mse(
    y_pred: list[Scalar],
    y_true: list[Scalar],
) -> Scalar:
    out = Scalar(0.0)

    for p_i, t_i in zip(y_pred, y_true):
        out += (p_i - t_i) * (p_i - t_i)

    return out


@beartype
class Neuron:
    def __init__(
        self,
        n_inp: int,
    ) -> None:
        self.w: list[Scalar] = [Scalar() for _ in range(n_inp)]
        self.b = Scalar()

    def __call__(
        self,
        x: list[Scalar],
    ) -> Scalar:
        out = Scalar(0.0)

        for w_i, x_i in zip(self.w, x):
            out += w_i * x_i

        out += self.b

        return out


@beartype
class Linear:
    def __init__(
        self,
        n_inp: int,
        n_out: int,
    ) -> None:
        self.neurons: list[Neuron] = [Neuron(n_inp) for _ in range(n_out)]

    def __call__(
        self,
        x: list[Scalar],
    ) -> list[Scalar]:
        out = [neuron(x) for neuron in self.neurons]

        return out


@beartype
class MLP:
    def __init__(
        self,
        ns: list[int],
    ) -> None:
        self.linears = [Linear(a, b) for a, b in zip(ns[:-1], ns[1:])]

    def __call__(
        self,
        x: list[Scalar],
    ) -> list[Scalar]:
        for linear in self.linears[:-1]:
            x = linear(x)
            x = [relu(x_i) for x_i in x]

        x = self.linears[-1](x)

        return x


__all__ = [
    "Scalar",
    "Neuron",
    "Linear",
    "MLP",
]
