"""A utility library for processing Vietnamese texts.

This pure-Python library provides functions and classes for various tasks
in processing Vietnamese texts, such as removing diacritics, converting
numbers to words, sorting strings, validations and more."""

__version__ = '0.2.1'

from .sort import vi_sort_key
from .number import num_to_words
from .misc import normalize_text, remove_diacritics, remove_tones
