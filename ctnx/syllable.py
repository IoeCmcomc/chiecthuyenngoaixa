# -*- coding: utf-8 -*-

from __future__ import annotations

from typing import Union, Iterable, Set
import unicodedata
from abc import ABC, abstractmethod
from functools import lru_cache

from .constants import TONES, TONE_NAMES
from .misc import normalize, separate_tone, is_even_tone

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
        if (syllable.nucleus in {'oo', 'ôô'}) or (syllable.rime in {'oa', 'oe', 'uy'}):
            return 0
        else:
            return super().placement_index(syllable)


class Syllable:
    """Represent a syllable in Vietnamese language."""

    ONSETS = ('b', 'ch', 'c', 'd', 'đ', 'gh', 'gi', 'g', 'h', 'kh', 'k', 'l', 'm', 'ngh', 'ng', 'nh', 'ng',
              'n', 'ph', 'p', 'qu', 'r', 's', 'th', 'tr', 't', 'v', 'x', '')
    MONOPHTHONGS = ('a', 'ă', 'â', 'e', 'ê', 'i', 'o', 'ô', 'ơ', 'u', 'ư', 'y')
    # 'oo' and 'ôô' are not diphthongs but they're denoted using two characters
    OPEN_DIPHTHONGS = ('iê', 'oo', 'ôô', 'uâ', 'uô', 'ươ', 'yê')
    CLOSEABLE_DIPHTHONGS = ('oa', 'oă', 'oe', 'uê', 'uy')
    CLOSED_DIPHTHONGS = ('ai', 'ao', 'au', 'ay', 'âu', 'ây', 'eo', 'êu', 'ia', 'iu', 'oi',
                         'ôi', 'ơi', 'ua', 'ui', 'uơ', 'ưa', 'ưi', 'ưu', 'yu')
    ROUNDED_DIPHTHONGS = ('oa', 'oă', 'uâ', 'oe', 'uê', 'uơ', 'uy')
    DIPHTHONGS = OPEN_DIPHTHONGS + CLOSEABLE_DIPHTHONGS + CLOSED_DIPHTHONGS
    CLOSED_TRIPHTHONGS = ('iêu', 'oai', 'oao', 'oay', 'oeo',
                          'uay', 'uây', 'uôi', 'uya', 'uyu', 'ươi', 'ươu', 'yêu')
    OPEN_TRIPHTHONGS = ('uyê',)
    ROUNDED_TRIPHTHONGS = ('oai', 'oao', 'oay', 'oeo', 'uay', 'uây', 'uya', 'uyu')
    TRIPHTHONGS = CLOSED_TRIPHTHONGS + OPEN_TRIPHTHONGS
    OPEN_NUCLEI = OPEN_TRIPHTHONGS + OPEN_DIPHTHONGS
    CLOSED_NUCLEI = CLOSED_TRIPHTHONGS + CLOSED_DIPHTHONGS
    NUCLEI = TRIPHTHONGS + DIPHTHONGS + MONOPHTHONGS
    ROUNDED_NUCLEI = set(ROUNDED_TRIPHTHONGS + ROUNDED_DIPHTHONGS)
    CODAS = ('ch', 'c', 'm', 'ng', 'nh', 'n', 'p', 't', '')

    AUTO_CORRECT: bool = True

    tone_placer = NewStyleTonePlacer

    def __init__(self, onset: str, nucleus: str, coda: str, tone=''):
        self._onset = onset
        self._nucleus = nucleus
        self._coda = coda
        self._tone = tone
        self.update(onset, nucleus, coda, tone)

    def __repr__(self):
        if self.tone:
            return f"Syllable({self.onset}, {self.nucleus}, {self.coda}, {self.tone})"
        else:
            return f"Syllable({self.onset}, {self.nucleus}, {self.coda})"

    def __str__(self):
        return self.to_string()

    def __bool__(self):
        return True

    def __eq__(self, other: Union[str, Syllable]):
        if isinstance(other, str):
            other = Syllable.from_string(other)
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
            raise Exception(
                f"Unexpected characters '{string}' after a syllable (in '{original}'')")

        return Syllable(onset, nucleus, coda, tone)

    def to_string(self) -> str:
        """Return the written form of the syllable."""
        onset = self.onset
        nucleus = self.nucleus
        coda = self.coda

        if (onset == 'gi') and ((nucleus == 'i') or (nucleus[:2] == 'iê')):
            onset = 'g'

        return ''.join((onset, self.tone_placer.place(self), coda))
    
    def update(self, onset: str, nucleus: str, coda: str, tone: str):
        onset, nucleus, coda = onset.lower(), nucleus.lower(), coda.lower()
        orig_onset, orig_nuclues, orig_coda, orig_tone = onset, nucleus, coda, tone
        if nucleus not in self.NUCLEI:
            ValueError(f"Invaild nucleus: {nucleus}")
        elif onset not in self.ONSETS:
            ValueError(f"Invaild onset: {onset}")
        elif coda not in self.CODAS:
            ValueError(f"Invaild coda: {coda}")
        elif tone not in TONES:
            ValueError(f"Invaild tone: '{tone}'")

        if onset in {'ng', 'ngh'}:
            onset = 'ngh' if (nucleus[0] in {'e', 'ê', 'i'}) else 'ng'
        
        if nucleus in self.ROUNDED_NUCLEI:
            if onset == 'qu':
                nucleus = nucleus[1:]
            elif self.onset == 'qu': # from 'qu' to another
                nucleus = self._apply_w_semivowel_for_non_qu(nucleus)
        elif (self.onset == 'qu') and (onset != 'qu'):
            if nucleus not in self.ROUNDED_NUCLEI:
                nucleus = self._apply_w_semivowel_for_non_qu(nucleus)
        elif (onset == 'qu') and (self.onset != 'qu'):
            onset = 'c'

        if onset in {'c', 'k'}:
            onset = 'k' if nucleus[0] in {'e', 'ê', 'i', 'y'} else 'c'

        if coda == '':
            if nucleus in self.OPEN_NUCLEI:
                raise ValueError(f"Open syllable (nucleus: {nucleus}) must have a coda")
            elif nucleus in self.CLOSED_NUCLEI:
                coda = ''
            elif onset != 'qu':
                if nucleus == 'y':
                    if coda == 'ng':
                        coda = 'nh'
                    nucleus = 'i'

        if (coda in {'c', 'p', 't'}) and not (tone in {'/', '.'}):
                if tone in {'\\', '?'}:
                    tone = '.'
                if tone in {'', '~'}:
                    tone = '/'
        
        if not self.AUTO_CORRECT:
            if onset != orig_onset:
                raise ValueError(f"Invaild onset consonant: {orig_onset}")
            elif nucleus != orig_nuclues:
                raise ValueError(f"Invaild nucleus: {orig_nuclues}")
            elif coda != orig_coda:
                raise ValueError(f"Invaild coda: {orig_coda}")
            elif tone != orig_tone:
                raise ValueError(f"Invaild tone: {orig_tone}")
        
        self._onset = onset
        self._nucleus = nucleus
        self._coda = coda
        self._tone = tone

    @property
    def onset(self) -> str:
        """The initial consonant part of the syllable."""

        return self._onset

    @onset.setter
    def onset(self, value: str):
        self.update(value, self.nucleus, self.coda, self.tone)

    @property
    def nucleus(self) -> str:
        """The vowel part of the syllable as stored in this object, not necessarily including the semivowel."""

        return self._nucleus

    @nucleus.setter
    def nucleus(self, value: str):
        self.update(self.onset, value, self.coda, self.tone)

    @property
    def coda(self) -> str:
        """The final consonant part of the syllable."""

        return self._coda

    @coda.setter
    def coda(self, value: str):
        self.update(self.onset, self.nucleus, value, self.tone)

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
        self.update(self.onset, self.nucleus, self.coda, value)

    @property
    def vowel(self) -> str:
        """The vowel part of the syllable, including the semivowel if any."""
        nucleus = self.nucleus

        if nucleus == 'yêu':
            return 'iêu'
        elif nucleus == 'yê':
            return 'iê'

        if self.onset == 'qu':
            if nucleus[0] in {'a', 'ă', 'e'}:
                return 'o' + self.nucleus
            else:
                return 'u' + self.nucleus
        elif nucleus == 'y':
            return 'i'
        else:
            return self.nucleus

    @property
    def rime(self) -> str:
        """The rime of the syllable, which is the combination of the vowel and the coda."""

        return self.vowel + self.coda

    @property
    def has_w_semivowel(self) -> bool:
        """Check whether the syllable has a on-glide semivowel or not."""
        return (self.onset == 'qu') or (self.nucleus in self.ROUNDED_NUCLEI)

    @property
    def has_even_tone(self) -> bool:
        """Check whether the syllable's tone is even (not oblique) or not."""
        return is_even_tone(self.tone)

    @property
    def has_oblique_tone(self) -> bool:
        """Check whether the syllable's tone is oblique (uneven) or not."""
        return not self.has_even_tone

    @staticmethod
    def _check_rime_groups_exact(rime1: str, rime2: str, rime_groups: Iterable[Set[str]]) -> bool:
        for rimes in rime_groups:
            if (rime1 in rimes) and (rime2 in rimes):
                return True
        return False

    def is_rhyme_with(self, other: Union[Syllable, str]) -> bool:
        """Check whether a syllable rhymes with another syllable or not. Beside exact rime matching,
        this method uses pre-defined rules for detecting similar rimes.

        Similar-rime rules are based on https://bentinhyeu.forumvi.com/t10-topic and https://hoaanhdao0603082010.violet.vn/entry/van-trong-tho-12076153.html ."""
        if isinstance(other, str):
            other = Syllable.from_string(other)

        self_rime = self.rime
        other_rime = other.rime
        if self_rime == other_rime:
            return True

        if Syllable._check_rime_groups_exact(self_rime, other_rime, (
            {'a', 'ơ'},
            {'ư', 'ơ'},
            {'e', 'ê', 'i'},
            {'o', 'ô', 'u'},
            {'ai', 'ay', 'ây'},
            {'ai', 'oi', 'ôi', 'ơi', 'ươi', 'ui'},
            {'ao', 'au'},
            {'âu', 'au'},
            {'ao', 'eo', 'êu', 'iêu', 'iu', 'ưu'},
            {'am', 'ơm'},
            {'ăm', 'âm'},
            {'em', 'êm', 'im'},
            {'an', 'ơn'},
            {'on', 'un'},
            {'ăn', 'ân', 'uân'},
            {'en', 'in', 'iên', 'uyên'},
            {'on', 'ôn', 'uôn', },
            {'ang', 'ương', },
            {'uông', 'ương', },
            {'ăng', 'âng', 'ưng'},
            {'ong', 'ông', 'ung'},
            {'anh', 'ênh', 'inh', 'oanh', 'uynh'},
        )):
            return True
        elif self.has_oblique_tone and other.has_oblique_tone and \
                Syllable._check_rime_groups_exact(self_rime, other_rime, (
                    {'o', 'ua'},
                    {'ia', 'uê'},
                    {'ac', 'ươc'},
                    {'âc', 'ưc'},
                    {'at', 'ưt'},
                    {'ât', 'ăt'},
                    {'it', 'uyêt'},
                    {'ut', 'uôt'},
                )):
            return True
        else:
            return False

    @property
    def can_apply_w_semivowel(self):
        return (self.onset != 'qu') and (self.vowel[0] in {'a', 'ă', 'â', 'e', 'ê', 'i', 'ơ', 'y'})
    
    @staticmethod
    def _apply_w_semivowel_for_non_qu(nucleus):
        if nucleus[0] in {'i', 'y'}:
            nucleus = 'uy' + nucleus[1:]
        elif nucleus[0] in {'a', 'ă', 'e'}:
            nucleus = 'o' + nucleus
        else: # â, ê, ơ
            nucleus = 'u' + nucleus
        return nucleus

    def apply_w_semivowel(self) -> bool:
        if not self.can_apply_w_semivowel:
            return False
        
        if self.onset in {'c', 'k'}:
            self.onset = 'qu'
        else:
            self.nucleus = self._apply_w_semivowel_for_non_qu(self.nucleus)
        
        return True