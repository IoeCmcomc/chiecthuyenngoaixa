"""A utility library for processing Vietnamese texts.

This pure-Python library provides functions and classes for various tasks
in processing Vietnamese texts, such as removing diacritics, converting
numbers to words, sorting strings, validations and more."""

__version__ = '0.1.2'

from .sort import ViSortKey
from .number import num_to_words
from .misc import normalize, remove_diacritics, remove_tones
