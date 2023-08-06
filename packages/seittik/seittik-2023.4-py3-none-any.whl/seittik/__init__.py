"""
A functional programming library that aims to supplant Python's existing
functional interfaces, offering a more comprehensive and expressive
alternative.
"""
from .pipes import Pipe
from .shears import X, Y, Z


__version__ = '2023.04'


P = Pipe
"""
An alias to {py:class}`seittik.pipes.Pipe`
"""


__all__ = ('Pipe', 'P', 'X', 'Y', 'Z')
