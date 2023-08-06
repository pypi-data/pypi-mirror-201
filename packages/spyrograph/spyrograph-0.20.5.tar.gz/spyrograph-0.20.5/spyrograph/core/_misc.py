"""Miscellaneous helper functions"""

import itertools
import collections
from typing import Tuple, List, Union
from numbers import Number
import turtle
import time

def _get_products_of_inputs(*args) -> Tuple[Number]:
    """Return a list of tuples that contains all of the input arguments"""
    list_of_lists = [_set_int_to_list(el) for el in args]
    product = list(itertools.product(*list_of_lists))
    return product

def _validate_only_one_iterable(*args) -> bool:
    """Return validation check that only one argument passed to create_range is an iterable"""
    inputs = collections.Counter([isinstance(el, collections.abc.Iterable) for el in args])
    if inputs[True] > 1:
        raise ValueError((
            "More than one input variable was varied."
            "Please only pass one list of varying inputs and try again."
        ))

def _set_int_to_list(input_val: Union[Number, List[Number]]) -> List[Number]:
    """Return list of numbers from given input parameter"""
    if isinstance(input_val, Number):
        input_val = [input_val]
    return input_val

def _draw_animation(
        shapes_arr, screen_size: Tuple[Number, Number] = (1000, 1000),
        screen_color: str = "white", exit_on_click: bool = False,
        color: str = "black", width: Number = 1,
        frame_pause: Number = 0.1, screen: "turtle.Screen" = None
    ) -> None:
    for shape in shapes_arr:
        if screen is not None:
            screen.clear()
            screen.setup(*screen_size)
            screen.bgcolor(screen_color)
        screen = shape.trace(
            screen = screen, screen_size = screen_size,
            screen_color = screen_color,
            color = color, width=width
        )
        time.sleep(frame_pause)
    if exit_on_click:
        turtle.Screen().exitonclick()
