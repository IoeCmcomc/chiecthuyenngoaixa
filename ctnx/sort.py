# -*- coding: utf-8 -*-

from __future__ import annotations

from .constants import CHAR_ORDER_DICT


class ViSortKey:
    """Vietnamese-aware sorting key class for use with the `key` parameter
    in `sorted()` and `str.sort()` functions."""

    def __init__(self, string=''):
        self.string = string

    def __repr__(self):
        return f"<ViSortKey '{self.string}'>"

    def __lt__(self, other: ViSortKey):
        d = CHAR_ORDER_DICT
        self_str = self.string
        other_str = other.string
        while True:
            if (self_str == '') or (other_str == ''):
                return len(self_str) < len(other_str)
            
            self_first = self_str[0]
            other_first = other_str[0]

            if self_first != other_first:
                if (self_first in d) and (other_first in d):
                    return d[self_first] < d[other_first]
                else:
                    return self_first < other_first
            
            self_str = self_str[1:]
            other_str = other_str[1:]