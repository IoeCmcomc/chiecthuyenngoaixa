# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import List, Iterable

from .constants import ALPHABET, DEFAULT_TONE_ORDER, VOWEL_TONE_TO_CHAR

class ViCollator:
    """Vietnamese-aware class for generating a sorting key for use with the `key` parameter
    in :py:func:`sorted` and :py:meth:`list.sort` functions.

    To get the default collator key, use :py:data:`ctnx.vi_sort_key`

    :param tone_order: A sequence of tone marks defining the sort order for vowels.
                       Defaults to ``('', '/', '\\', '?', '~', '.')``.
    :type tone_order: Iterable
    """
    
    def __init__(self, tone_order: Iterable = DEFAULT_TONE_ORDER) -> None:
        self.tone_order = tone_order

        index = 0
        mapping = {}

        def add_char(ch: str, is_upper: bool):
            nonlocal index, mapping
            if is_upper:
                ch = ch.upper()
            mapping[ch] = index
            index += 1

        def make_case_group(start_letter, is_upper):
            nonlocal index
            index = ord(start_letter)
            for letter in ALPHABET:
                if letter in VOWEL_TONE_TO_CHAR:
                    for tone in tone_order:
                        add_char(VOWEL_TONE_TO_CHAR[letter][tone], is_upper)
                else:
                    add_char(letter, is_upper)

        for i in range(ord('A')):
            add_char(chr(i), False)
        make_case_group('A', True)
        for ch in "[\\]^_`":
            add_char(ch, False)
        make_case_group('a', False)
        self.mapping = mapping
        self.last_map_index = index - 1

    def key(self, text: str) -> List[int]:
        key = []
        _append = key.append
        mapping = self.mapping 
        offset = self.last_map_index
        
        for ch in text:
            try:
                _append(mapping[ch])
            except KeyError:
                _append(ord(ch) + offset)
                
        return key

vi_collator = ViCollator()
vi_sort_key = vi_collator.key
