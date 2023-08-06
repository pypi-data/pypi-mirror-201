"""
This module aims to develop a set of custom builtins to improve iterators

Syntax Changes:
    From: filter(function, iterable)
    To: iterable.filter(function) 
"""

import builtins
from typing import Iterable, Callable, Union


class IteratorMethods:
    @staticmethod
    def filter(iterable: Iterable, func: Callable[[object], bool]) -> list:
        """
        Filter elements from an iterable based on a function.

        Args:
        iterable: An iterable object to filter elements from.
        func: A function that accepts one argument and returns a Boolean value.

        Returns:
        A list of elements from the iterable that satisfy the function.

        """
        return list(filter(func, iterable))

    @staticmethod
    def map(iterable: Iterable, func: Callable[[object], object]) -> list:
        """
        Apply a function to each element in an iterable.

        Args:
        iterable: An iterable object to apply the function to.
        func: A function that accepts one argument and returns a value.

        Returns:
        A list of values returned by the function for each element in the iterable.

        """
        return list(map(func, iterable))

    @staticmethod
    def reduce(iterable: Iterable, func: Callable[[object, object], object], initializer: Union[object, None] = None) -> Union[object, None]:
        """
        Apply a function to pairs of elements in an iterable to reduce the iterable to a single value.

        Args:
        iterable: An iterable object to reduce to a single value.
        func: A function that accepts two arguments and returns a value.
        initializer: An optional initial value for the reduction.

        Returns:
        The final value after reducing the iterable with the function.

        """
        iterator = iter(iterable)
        if initializer is None:
            try:
                initializer = next(iterator)
            except StopIteration:
                return None
        value = initializer
        for element in iterator:
            value = func(value, element)
        return value

    @staticmethod
    def any(iterable: Iterable, func: Callable[[object], bool] = lambda x: x) -> bool:
        """
        Check if at least one element in an iterable satisfies a function.

        Args:
        iterable: An iterable object to check for any satisfying elements.
        func: A function that accepts one argument and returns a Boolean value.

        Returns:
        True if at least one element satisfies the function, False otherwise.

        """
        for element in iterable:
            if func(element):
                return True
        return False

    @staticmethod
    def all(iterable: Iterable, func: Callable[[object], bool] = lambda x: x) -> bool:
        """
        Check if all elements in an iterable satisfy a function.

        Args:
        iterable: An iterable object to check for all satisfying elements.
        func: A function that accepts one argument and returns a Boolean value.

        Returns:
        True if all elements satisfy the function, False otherwise.

        """
        for element in iterable:
            if not func(element):
                return False
        return True


# APPLYING THE CHANGES TO THE BUILTINS ------------------------------

class list(builtins.list):
    def filter(self, func: Callable[[object], bool]) -> list:
        return IteratorMethods.filter(self, func)

    def map(self, func: Callable[[object], object]) -> list:
        return IteratorMethods.map(self, func)

    def reduce(self, func: Callable[[object, object], object]) -> object:
        return IteratorMethods.reduce(self, func)

    def any(self, func: Callable[[object], bool] = lambda x: x) -> bool:
        return IteratorMethods.any(self, func)
    
    def all(self, func: Callable[[object], bool] = lambda x: x) -> bool:
        return IteratorMethods.all(self, func)
    
class tuple(builtins.tuple):
    def filter(self, func: Callable[[object], bool]) -> list:
        return IteratorMethods.filter(self, func)

    def map(self, func: Callable[[object], object]) -> list:
        return IteratorMethods.map(self, func)

    def reduce(self, func: Callable[[object, object], object]) -> object:
        return IteratorMethods.reduce(self, func)

    def any(self, func: Callable[[object], bool] = lambda x: x) -> bool:
        return IteratorMethods.any(self, func)
    
    def all(self, func: Callable[[object], bool] = lambda x: x) -> bool:
        return IteratorMethods.all(self, func)
    
class set(builtins.set):
    def filter(self, func: Callable[[object], bool]) -> list:
        return IteratorMethods.filter(self, func)
    
    def map(self, func: Callable[[object], object]) -> list:
        return IteratorMethods.map(self, func)
    
    def reduce(self, func: Callable[[object, object], object]) -> object:
        return IteratorMethods.reduce(self, func)
    
    def any(self, func: Callable[[object], bool] = lambda x: x) -> bool:
        return IteratorMethods.any(self, func)
    
    def all(self, func: Callable[[object], bool] = lambda x: x) -> bool:
        return IteratorMethods.all(self, func)
    
class frozenset(builtins.frozenset):
    def filter(self, func: Callable[[object], bool]) -> list:
        return IteratorMethods.filter(self, func)
    
    def map(self, func: Callable[[object], object]) -> list:
        return IteratorMethods.map(self, func)
    
    def reduce(self, func: Callable[[object, object], object]) -> object:
        return IteratorMethods.reduce(self, func)
    
    def any(self, func: Callable[[object], bool] = lambda x: x) -> bool:
        return IteratorMethods.any(self, func)
    
    def all(self, func: Callable[[object], bool] = lambda x: x) -> bool:
        return IteratorMethods.all(self, func)
    
