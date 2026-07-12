# -*- coding: utf-8 -*-

from __future__ import annotations

from typing import Union, Iterable, Set, overload
from abc import ABC, abstractmethod
from functools import lru_cache

from .constants import TONES, ALL_RIMES
from .misc import nfc_normalize, place_tone_to_char, separate_tone, is_even_tone


def find_startswith(text: str, candidates: Iterable):
    try:
        return next(filter(text.startswith, candidates))
    except StopIteration:
        return None


class TonePlacer(ABC):
    """Controls tone mark placements."""

    @staticmethod
    def place_to_vowels_at(vowels, tone, position):
        return vowels[:position] + place_tone_to_char(vowels[position], tone) + vowels[position+1:]

    @classmethod
    def place(cls, syllable: Syllable, nucleus) -> str:
        i = cls.placement_index(syllable)
        return cls.place_to_vowels_at(nucleus, syllable.tone, i)

    @classmethod
    @abstractmethod
    def placement_index(cls, syllable: Syllable) -> int:
        pass


class NewStyleTonePlacer(TonePlacer):
    @classmethod
    def placement_index(cls, syllable: Syllable) -> int:
        nucleus = syllable.nucleus
        nucleus_len = len(nucleus)
        assert nucleus_len > 0
        if nucleus_len == 1:
            return 0
        elif nucleus_len == 2:
            if (nucleus in {'uy', 'uơ'}) or (syllable.onset == 'q'):
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
        else:
            return 2


class OldStyleTonePlacer(NewStyleTonePlacer):
    @classmethod
    def placement_index(cls, syllable: Syllable) -> int:
        if (syllable.nucleus in {'oo', 'ôô'}) or ((syllable.rime in {'oa', 'oe', 'uy'}) and (syllable.onset != 'q')):
            return 0
        else:
            return super().placement_index(syllable)


class Syllable:
    """Represent a syllable in Vietnamese language."""

    ONSETS = ('b', 'ch', 'c', 'd', 'đ', 'gh', 'gi', 'g', 'h', 'kh', 'k', 'l', 'm', 'ngh', 'ng', 'nh', 'ng',
              'n', 'ph', 'p', 'q', 'r', 's', 'th', 'tr', 't', 'v', 'x', '')
    MONOPHTHONGS = ('a', 'ă', 'â', 'e', 'ê', 'i', 'o', 'ô', 'ơ', 'u', 'ư', 'y')
    # 'oo' and 'ôô' are not diphthongs but they're denoted using two characters
    OPEN_DIPHTHONGS = ('iê', 'oo', 'ôô', 'uâ', 'uô', 'ươ', 'yê')
    CLOSEABLE_DIPHTHONGS = ('oa', 'oă', 'oe', 'uê', 'uy')
    CLOSED_DIPHTHONGS = ('ai', 'ao', 'au', 'ay', 'âu', 'ây', 'eo', 'êu', 'ia', 'iu', 'oi',
                         'ôi', 'ơi', 'ua', 'ui', 'uơ', 'ưa', 'ưi', 'ưu', 'yu')
    # Also includes combinations of an onglide semivowel and a vowel
    DIPHTHONGS = OPEN_DIPHTHONGS + CLOSEABLE_DIPHTHONGS + CLOSED_DIPHTHONGS
    # 'uêu' is the lip-rounded form of 'êu'
    # 'uơi' is the lip-rounded form of 'ơi'
    # 'uyêu' is the lip-rounded form of 'iêu'/'yêu'
    CLOSED_TRIPHTHONGS = ('iêu', 'oai', 'oao', 'oau', 'oay', 'oeo',
                          'uay', 'uây', 'uêu', 'uôi', 'uya', 'uyu', 'uơi', 'ươi', 'ươu', 'yêu')
    OPEN_TRIPHTHONGS = ('uyê',)
    # These "triphthongs" are actually diphthongs + semivowel (oversimplified)
    TRIPHTHONGS = CLOSED_TRIPHTHONGS + OPEN_TRIPHTHONGS
    OTHER_CLOSED_NUCLEI = ('uyêu',)
    OTHER_NUCLEI = OTHER_CLOSED_NUCLEI
    OPEN_NUCLEI = OPEN_TRIPHTHONGS + OPEN_DIPHTHONGS
    CLOSED_NUCLEI = OTHER_CLOSED_NUCLEI + CLOSED_TRIPHTHONGS + CLOSED_DIPHTHONGS
    NUCLEI = OTHER_NUCLEI + TRIPHTHONGS + DIPHTHONGS + MONOPHTHONGS
    NON_LIP_ROUNDABLE_NUCLEI_SET = {'o', 'oi', 'oo', 'u', 'ua', 'ui', 'uô', 'uôi'}
    QU_NUCLEUS_PREFIX_REPLACEMENTS = {'ua': 'oa', 'uă' : 'oă', 'ue': 'oe'}
    CODAS = ('ch', 'c', 'm', 'ng', 'nh', 'n', 'p', 't', '')


    def __init__(self, onset: str, nucleus: str, coda: str, tone='',
                 auto_correct: bool = True, tone_placer = NewStyleTonePlacer):
        self.auto_correct: bool = auto_correct
        self.tone_placer: type[TonePlacer] = tone_placer

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

    @overload
    def __eq__(self, other: str) -> bool:
        ...
    
    @overload
    def __eq__(self, other: Syllable) -> bool:
        ...
    
    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            other = Syllable.from_string(other)
        if isinstance(other, Syllable):
            return self.onset == other.onset and self.i_normalized_nucleus == other.i_normalized_nucleus and self.coda == self.coda and self.tone == other.tone
        return False

    @classmethod
    def _parse_rime(cls, string: str, has_q_onset: bool) -> tuple:
        if has_q_onset:
            prefix = string[:2]
            if prefix in cls.QU_NUCLEUS_PREFIX_REPLACEMENTS:
                string = cls.QU_NUCLEUS_PREFIX_REPLACEMENTS[prefix] + string[2:]

        nucleus = find_startswith(string, cls.NUCLEI)

        if nucleus:
            string = string[len(nucleus):]
        # Nucleus may be empty when parsing the 'gìn' syllable.

        coda = find_startswith(string, cls.CODAS)
        assert coda is not None
        string = string[len(coda):]

        return (nucleus, coda, string)

    @classmethod
    @lru_cache
    def _from_string(cls, string: str, auto_correct=True, tone_placer=NewStyleTonePlacer) -> Syllable:
        """Create a Syllable object from string."""

        string = nfc_normalize(string).lower()
        if ' ' in string:
            raise Exception(f"The input string must not have whitespaces")
        original = string
        onset = nucleus = coda = tone = ''

        if string in {'gịa', 'gỵa'}:
            return cls('gi', 'ia', '', '.',
                            auto_correct=auto_correct,
                            tone_placer=tone_placer)

        string, tone = separate_tone(string)

        onset = find_startswith(string, cls.ONSETS)
        assert onset is not None
        string = string[len(onset):]

        if onset == 'gi':
            if (len(string) > 1) and (string[0] == 'ê'):
                string = 'i' + string

        nucleus, coda, rest = cls._parse_rime(string, onset == 'q')

        if not nucleus:
            if onset == 'gi':
                nucleus = 'i'
            else:
                raise Exception(f"Invaild syllable: {original}")

        if rest != '':
            raise Exception(
                f"Unexpected characters '{rest}' after a syllable (in '{original}'')")

        return cls(onset, nucleus, coda, tone, auto_correct=auto_correct,
                   tone_placer=tone_placer)
    
    @classmethod
    @lru_cache
    def from_string(cls, string: str, auto_correct=True, tone_placer=NewStyleTonePlacer) -> Syllable:
        """Create a Syllable object from string.
This method is cached by default; use `_from_string` for the uncached method instead."""

        return cls._from_string(string, auto_correct, tone_placer)

    def to_string(self) -> str:
        """Return the written form of the syllable."""
        onset = self.onset
        nucleus = self.nucleus
        coda = self.coda

        if (onset == 'gi') and ((nucleus == 'i') or (nucleus[:2] in {'iê', 'ia'})):
            onset = 'g'

        if onset == 'q' and nucleus[0] == 'o':
            nucleus = 'u' + nucleus[1:]

        return ''.join((onset, self.tone_placer.place(self, nucleus), coda))

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
        
        if nucleus == 'uô' and coda == 'c':
            if onset == 'k':
                onset = 'c'
        elif self._nucleus_has_onglide_semivowel(nucleus):
            if onset in {'c', 'k'}:
                onset = 'q'
        elif onset == 'q':
            onset = 'c'

        if onset in {'c', 'k'}:
            onset = 'k' if nucleus[0] in {'e', 'ê', 'i', 'y'} else 'c'
        if onset in {'ng', 'ngh'}:
            onset = 'ngh' if (nucleus[0] in {'e', 'ê', 'i'}) else 'ng'

        if onset == '':
            if nucleus == 'iêu':
                nucleus = 'yêu'
            elif nucleus == 'iê':
                nucleus = 'yê'
        else:
            if nucleus == 'yêu':
                nucleus = 'iêu'
            elif nucleus == 'yê':
                nucleus = 'iê'

        if coda == '':
            if nucleus in self.OPEN_NUCLEI:
                raise ValueError(
                    f"Open syllable (nucleus: {nucleus}) must have a coda")
            elif nucleus in self.CLOSED_NUCLEI:
                coda = ''

        if (coda in {'c', 'p', 't'}) and not (tone in {'/', '.'}):
            if tone in {'\\', '?'}:
                tone = '.'
            if tone in {'', '~'}:
                tone = '/'

        rime = self._i_normalize_nucleus(nucleus) + coda
        if rime not in ALL_RIMES:
            if not self.auto_correct:
                raise ValueError(f"Invalid rime: {orig_nuclues + orig_coda}")
            if rime in {'iênh', 'yênh'}:
                coda = 'ng' # iêng/yêng
            elif rime in {'iêch', 'yêch'}:
                coda = 'ng' # iêc/yêc

            rime = self._i_normalize_nucleus(nucleus) + coda
            if rime not in ALL_RIMES:
                raise ValueError(f"Invalid rime: {orig_nuclues + orig_coda} (after auto-fix: {rime})")

        if not self.auto_correct:
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
        """The vowel part of the syllable as stored in this object, including semivowels."""

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

    @staticmethod
    def _i_normalize_nucleus(nucleus):
        if nucleus == 'yêu':
            return 'iêu'
        elif nucleus == 'yê':
            return 'iê'
        elif nucleus == 'y':
            return 'i'
        else:
            return nucleus

    @property
    def i_normalized_nucleus(self) -> str:
        """The vowel part of the syllable, with i/y-normalized value."""
        return self._i_normalize_nucleus(self.nucleus)

    @property
    def normalized_nucleus(self) -> str:
        nucleus = self.i_normalized_nucleus
        if self.coda == '':
            if nucleus == 'iê':
                nucleus = 'ia'
            elif nucleus == 'uô':
                nucleus = 'ua'
            elif nucleus == 'ươ':
                nucleus = 'ưa'

        return nucleus

    @property
    def rime(self) -> str:
        """The rime of the syllable, which is the combination of the nucleus and the coda."""

        return self.nucleus + self.coda

    @rime.setter
    def rime(self, rime: str):
        nucleus, coda, rest = self._parse_rime(rime, self.onset == 'q')
        if not nucleus:
            raise Exception('Invalid rime: rime')
        if rest != '':
            raise Exception(
                f"Unexpected characters '{rest}' after a rime (in '{rime}'')")

        self.update(onset=self.onset, nucleus=nucleus,
                    coda=coda, tone=self.tone)
    
    @property
    def normalized_rime(self) -> str:
        """The rime of the syllable, with i/y-normalized value."""

        return self.i_normalized_nucleus + self.coda

    @staticmethod
    def _nucleus_has_onglide_semivowel(nucleus: str) -> bool:
        return (nucleus[0] in {'o', 'u'}) and (nucleus not in Syllable.NON_LIP_ROUNDABLE_NUCLEI_SET)

    @property
    def has_onglide_semivowel(self) -> bool:
        """Check whether the syllable has a on-glide semivowel, as presented in 'qua' and 'xoa', or not."""
        return self._nucleus_has_onglide_semivowel(self.nucleus)

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

        self_rime = self.normalized_rime
        other_rime = other.normalized_rime
        if self_rime == other_rime:
            return True

        if self._check_rime_groups_exact(self_rime, other_rime, (
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
                self._check_rime_groups_exact(self_rime, other_rime, (
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
    def can_apply_onglide_semivowel(self):
        return self.i_normalized_nucleus[0] in {'a', 'ă', 'â', 'e', 'ê', 'i', 'ơ', 'y'}

    @staticmethod
    def _apply_onglide_semivowel_to_nucleus(nucleus):
        if nucleus[0] in {'i', 'y'}:
            nucleus = 'uy' + nucleus[1:]
        elif nucleus[0] in {'a', 'ă', 'e'}:
            nucleus = 'o' + nucleus
        else:  # â, ê, ơ
            nucleus = 'u' + nucleus
        return nucleus

    def apply_onglide_semivowel(self) -> bool:
        if not self.can_apply_onglide_semivowel:
            return False

        if self.onset in {'c', 'k'}:
            self.onset = 'q'
        self.nucleus = self._apply_onglide_semivowel_to_nucleus(self.nucleus)

        return True