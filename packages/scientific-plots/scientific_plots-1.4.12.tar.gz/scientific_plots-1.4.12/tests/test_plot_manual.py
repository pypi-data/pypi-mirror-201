#!/usr/bin/env python3
"""
Test the design of the created plots by eye and by hand. For this, the plots
are placed in a persistent directory.
"""
from pathlib import Path

from pytest import mark
from numpy import linspace
from scientific_plots.default_plots import two_plots, three_axis_plots, plot
from scientific_plots.types_ import Vector


LOCATION = Path("tests/plots/test_plot.pdf")
LOCATION2 = Path("tests/plots/test_plot2.pdf")
LOCATION3 = Path("tests/plots/test_plot3.pdf")


@mark.use_style
def test_two_plots() -> None:
    """Test the creation of a twin-plot."""
    x_test: Vector = linspace(1., 100., 100)
    y_test1: Vector = x_test**2
    y_test2: Vector = x_test**.5
    filename = LOCATION
    filename.parent.mkdir(exist_ok=True)
    two_plots(x_test, y_test1, "plot1",
              x_test, y_test2, "plot2",
              "x", "y",
              filename)
    assert filename.exists()


@mark.use_style
def test_three_plots() -> None:
    """Test the creation of a plot with three y axis."""
    x_test: Vector = linspace(1., 100., 100)
    y_test1: Vector = x_test**2
    y_test2: Vector = x_test**.5
    y_test3: Vector = x_test**3 + 1
    filename = LOCATION2
    filename.parent.mkdir(exist_ok=True)
    three_axis_plots(
        x_test, y_test1, "1.",
        x_test, y_test2, "2.",
        x_test, y_test3, "3.",
        "x", "y1", "y2", "y3",
        filename, color=(3, 4, 5))
    assert filename.exists()


@mark.use_style
def test_skip_color() -> None:
    """Test the skipping of a color in the cycle."""
    x_test: Vector = linspace(1., 2., 100)
    y_test1: Vector = x_test**2
    filename = LOCATION3
    filename.parent.mkdir(exist_ok=True)
    plot(x_test, y_test1, "x", "y", filename, cycler=1)
    assert filename.exists()
