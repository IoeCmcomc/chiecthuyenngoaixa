# -*- coding: utf-8 -*-

from __future__ import annotations

import unicodedata
from abc import ABC, abstractmethod
from functools import lru_cache

from .constants import TONES, TONE_NAMES
from .misc import normalize, separate_tone

class TonePlacer(ABC):
    """Controls tone mark placements."""

    @staticmethod
    @lru_cache(maxsize=160)
    def place_to_char(char, tone) -> str:
        name = unicodedata.name(char)
    
        if (tone != '') and (tone in TONES):
            if 'WITH' in name:
                name += ' AND '
            else:
                name += ' WITH '
            name += TONE_NAMES[TONES.index(tone)]
    
        return unicodedata.lookup(name)
    
    @classmethod
    def place(cls, syllable: Syllable) -> str:
        nucleus = syllable.nucleus
        i = cls.placement_index(syllable)
        return nucleus[:i] + cls.place_to_char(nucleus[i], syllable.tone) + nucleus[i+1:]
    
    @classmethod
    @abstractmethod
    def placement_index(cls, syllable: Syllable) -> int:
        pass

class NewStyleTonePlacer(TonePlacer):
    @classmethod
    def placement_index(cls, syllable: Syllable):
        nucleus = syllable.nucleus
        nucleus_len = len(nucleus)
        if nucleus_len == 1:
            return 0
        elif nucleus_len == 2:
            if nucleus in {'uy', 'uơ'}:
                return 1
            elif nucleus in Syllable.CLOSED_DIPHTHONGS:
                return 0
            else:
                return 1
        elif nucleus_len == 3:
            if nucleus in Syllable.CLOSED_TRIPHTHONGS:
                return 1
            else:
                return 2

class OldStyleTonePlacer(NewStyleTonePlacer):
    @classmethod
    def placement_index(cls, syllable: Syllable):
        if (syllable.nucleus in {'oa', 'oe', 'uy'}) and (syllable.coda == ''):
            return 0
        else:
            return super().placement_index(syllable)

class Syllable:
    """Represent a syllable in Vietnamese language."""

    ONSETS = ('b', 'ch', 'c', 'd', 'đ', 'gh', 'gi', 'g', 'h', 'kh', 'k', 'l', 'm', 'ngh', 'ng', 'nh', 'ng',
    'n', 'ph', 'p', 'qu', 'r', 's', 'th', 'tr', 't', 'v', 'x', '')
    MONOPHTHONGS = ('a', 'ă', 'â', 'e', 'ê', 'i', 'o', 'ô', 'ơ', 'u', 'ư', 'y')
    # 'oo' and 'ôô' are not a diphthong but it's denoted using two characters
    OPEN_DIPHTHONGS = ('iê', 'oă', 'oo', 'ôô', 'uâ', 'uô', 'ươ', 'yê')
    ROUNDED_DIPHTHONGS = ('oa', 'oe', 'uê')
    CLOSED_DIPHTHONGS = ('ai', 'ao', 'au', 'ay', 'âu', 'ây', 'eo', 'êu', 'ia', 'iu', 'oi',
    'ôi', 'ơi', 'ua', 'ui', 'uơ', 'uy', 'ưa', 'ưi', 'ưu', 'yu')
    DIPHTHONGS = OPEN_DIPHTHONGS + ROUNDED_DIPHTHONGS + CLOSED_DIPHTHONGS
    CLOSED_TRIPHTHONGS = ('iêu', 'oai', 'oao', 'oay', 'oeo', 'uay', 'uây', 'uôi', 'uya', 'uyu', 'ươi', 'ươu', 'yêu')
    OPEN_TRIPHTHONGS = ('uyê',)
    TRIPHTHONGS = CLOSED_TRIPHTHONGS + OPEN_TRIPHTHONGS
    OPEN_NUCLEI = OPEN_TRIPHTHONGS + OPEN_DIPHTHONGS
    CLOSED_NUCLEI = CLOSED_TRIPHTHONGS + CLOSED_DIPHTHONGS
    NUCLEI = TRIPHTHONGS + DIPHTHONGS + MONOPHTHONGS
    CODAS = ('ch', 'c', 'm', 'ng', 'nh', 'n', 'p', 't', '')
    
    AUTO_CORRECT: bool = True
    
    tone_placer = NewStyleTonePlacer
    
    def __init__(self, onset: str, nucleus: str, coda: str, tone=''):
        self.onset = onset
        self.nucleus = nucleus
        self.coda = coda
        self.tone = tone
   		
    def __repr__(self):
        if self.tone:
            return f"Syllable({self.onset}, {self.nucleus}, {self.coda}, {self.tone})"
        else:
            return f"Syllable({self.onset}, {self.nucleus}, {self.coda})"
   
    def __str__(self):
       return self.to_string()
       
    def __bool__(self):
        return True
    
    def __eq__(self, other: Syllable):
        return self.onset == other.onset and self.nucleus == other.nucleus and self.coda == self.coda and self.tone == other.tone
    
    @classmethod
    @lru_cache
    def from_string(cls, string: str) -> Syllable:
        """Create a Syllable object from string."""

        string = normalize(string).lower()
        if ' ' in string:
            raise Exception(f"The input string must not have whitespaces")
        original = string
        onset = nucleus = coda = tone = ''
        
        string, tone = separate_tone(string)
        
        onset = next(filter(string.startswith, cls.ONSETS))
        string = string[len(onset):]
        
        if onset == 'gi':
            if (len(string) > 1) and (string[0] == 'ê'):
                string = 'i' + string
        try:
            nucleus = next(filter(string.startswith, cls.NUCLEI))
            string = string[len(nucleus):]
        except StopIteration:
            if onset == 'gi':
                nucleus = 'i'
            else:
                raise Exception(f"Invaild syllable: {original}")
        
        coda = next(filter(string.startswith, cls.CODAS))
        string = string[len(coda):]
                
        if string != '':
            raise Exception(f"Unexpected characters '{string}' after a syllable (in '{original}'')")
                
        return Syllable(onset, nucleus, coda, tone)
       
    def to_string(self) -> str:
        """Return the written form of the syllable."""
        onset = self.onset
        nucleus = self.nucleus
        coda = self.coda
        
        if (onset == 'gi') and ((nucleus == 'i') or (nucleus[:2] == 'iê')):
            onset = 'g'
        
        return ''.join((onset, self.tone_placer.place(self), coda))

    @property
    def onset(self) -> str:
        """The initial consonant part of the syllable."""

        return self._onset

    @onset.setter
    def onset(self, value: str):
        value = value.lower()
        original = value
        if hasattr(self, "_onset"):
            if value == self.onset: return
        if value in self.ONSETS:
            if hasattr(self, "_nucleus"):
                if value in {'ng', 'ngh'}:
                    value = 'ngh' if (self.nucleus[0] in {'e', 'ê', 'i'}) else 'ng'
                elif value in {'c', 'k'}:
                    value = 'k' if (self.nucleus[0] in {'e', 'ê', 'i', 'y'}) else 'c'
                elif value == 'q':
                    nucleusChars = list(self.nucleus)
                    print(nucleusChars)
                    if nucleusChars[0] != 'u':
                        nucleusChars[0] = 'u'
                        self.nucleus = ''.join(nucleusChars)
            if not self.AUTO_CORRECT and (value != original):
                raise ValueError(f"Invaild onset consonant: {original}")
            else:
                self._onset = value
        else:
            raise ValueError(f"Invaild onset: {value}")
    
    @property
    def nucleus(self) -> str:
        """The vowel part of the syllable as stored in this object, not necessarily including the semivowel."""
        
        return self._nucleus
        
    @nucleus.setter
    def nucleus(self, value: str):
        value = value.lower()
        original = value
        original_onset = self.onset
        if value in self.NUCLEI:
            if hasattr(self, "_onset"):
                if self.onset in {'ng', 'ngh'}:
                    self.onset = 'ngh' if (value[0] in {'e', 'ê', 'i'}) else 'ng'
                elif self.onset in {'c', 'k', 'q'}:
                    if value[0] in {'e', 'ê', 'i', 'y'}:
                         self.onset = 'k'
                    elif value[0] != 'u':
                         self.onset = 'c'
            if not self.AUTO_CORRECT and (self.onset != original_onset):
                raise ValueError(f"Invaild nucleus: {original}")
            else:
                self._nucleus = value
        else:
            raise ValueError(f"Invaild nucleus: {value}")

    @property
    def coda(self) -> str:
        """The final consonant part of the syllable."""

        return self._coda
        
    @coda.setter
    def coda(self, value: str):
        value = value.lower()
        original = value
        original_nucleus = self.nucleus
        if value in self.CODAS:
            if value == '':
                if self.nucleus in self.OPEN_NUCLEI:
                    raise ValueError(f"Open syllable (nucleus: {self.nucleus}) must have a coda")
            elif (self.nucleus == 'uy' or (self.nucleus == 'y' and self.onset == 'qu')) and value not in {'c', 'ng', ''}:
                pass
            elif self.nucleus in self.CLOSED_NUCLEI:
                value = ''
            else:
                if self.nucleus == 'y':
                    if value == 'ng':
                        value = 'nh'
                    self.nucleus = 'i'
            if not self.AUTO_CORRECT and ((value != original) or (self.nucleus != original_nucleus)):
                raise ValueError(f"Invaild coda: {original}")
            else:
                self._coda = value
        else:
            raise ValueError(f"Invaild coda: {value}")

    @property
    def tone(self) -> str:
        """The tone of the syllable.
        
        The returned tone is denoted as the following:
        '': unmarked (ngang)
        '/': acute accent (sắc)
        '\\': grave accent (huyền)
        '?': hook above (hỏi)
        '~': tilde (ngã)
        '.': dot below (nặng)
        """

        return self._tone
        
    @tone.setter
    def tone(self, value: str):
        if value in TONES:
            if hasattr(self, "_coda"):
                if (self.coda in {'c', 'p', 't'}) and not (value in {'/', '.'}):
                    if not self.AUTO_CORRECT:
                        raise ValueError(f"Invaild tone: {value}")
                    elif value in {'', '\\', '?'}:
                        value = '.'
                    elif value == '~':
                        value = '/'
            self._tone = value
        else:
            raise ValueError(f"Invaild tone: {value}")
    
    @property
    def vowel(self) -> str:
        """The vowel part of the syllable, including the semivowel if any."""

        if self.onset == 'qu':
            return 'u' + self.nucleus
        else:
            return self.nucleus
        
    @property
    def rime(self) -> str:
        """The rime of the syllable, which is the combination of the vowel and the coda."""

        return self.vowel + self.coda
