#!/usr/bin/env python
"""This is the stub for the figure-type in matplot-lib."""
from typing import Optional, Tuple, Iterable

from .pyplot import Axes


class Canvas:
    """Canvas, which contains the figure."""

    def draw(self) -> None: ...

    def fush_events(self) -> None: ...


class Figure:

    axes: Iterable[Axes]

    canvas: Canvas

    def __init__(
        self, figsize: Optional[Tuple[float, float]] = None) -> None: ...

    def gca(self) -> Axes: ...

    def set_size_inches(self, x: float, y: float) -> None: ...

    def subplots_adjust(self, bottom: Optional[float] = None,
                        right: Optional[float] = None) -> None: ...

    def add_subplot(self, position: int = 111,
                    projection: str = "2d") -> Axes: ...
