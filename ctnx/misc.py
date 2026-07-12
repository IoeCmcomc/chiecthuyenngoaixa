# -*- coding: utf-8 -*-
from __future__ import annotations

from unicodedata import name as unicode_name, lookup as unicode_lookup, normalize as unicode_normalize
from functools import lru_cache
from re import compile as re_compile, escape as re_escape, sub as re_sub, IGNORECASE as re_IGNORECASE, \
    Match as re_Match
from typing import Literal, Optional, Iterable, Dict
from itertools import product

from .constants import TONES, TONE_NAMES, NO_TONE_CHAR_TRANS, \
    BASE_TONE_PLACEMENT_REPLACE_PAIRS, NON_WORD_CHARS_REGEX, \
    VOWEL_TONE_TO_CHAR, CHAR_TO_TONE_AND_VOWEL


def nfc_normalize(text: str) -> str:
    """Converts combining Unicode characters to theirs equivalent precomposed characters."""
    return unicode_normalize('NFC', text)


def normalize_confusables(text: str) -> str:
    """Converts a confusable text to a potentially normal text.

    Replace similar-looking characters and homoglyphs with theirs equivalent
    Vietnamese characters. Small cap letters will be converted to lowercase.
    """
    from .constants.confusables import CONFUSABLE_CHAR_TRANS
    return nfc_normalize(text.translate(CONFUSABLE_CHAR_TRANS))


def remove_tones(text: str) -> str:
    """Remove tone marks from text.

    Replace characters with tone marks with theirs equivalent non-toned
    characters. Other diacritics will be kept.
    """
    return text.translate(NO_TONE_CHAR_TRANS)


def remove_diacritics(text: str) -> str:
    """Remove all diacritics from text.

    Replace characters with diacritics with theirs equivalent ASCII
    characters.
    """

    SPECIAL_TRANS = str.maketrans('đĐ', 'dD')
    return unicode_normalize('NFKD', text.translate(SPECIAL_TRANS)).encode('ascii', 'ignore').decode()


def sep_tone_from_char(char: str):
    """Extract the tone mark from a character.

    The returned tone is denoted as the following:
    '': unmarked (ngang)
    '/': acute accent (sắc)
    '\\': grave accent (huyền)
    '?': hook above (hỏi)
    '~': tilde (ngã)
    '.': dot below (nặng)

    Parameters
    ----------
    char : str
        The character from which the tone will be extracted

    Returns
    -------
    tuple
        a tuple of the same character without tone mark and its tone
    """

    try:
        return CHAR_TO_TONE_AND_VOWEL[char]
    except KeyError:
        return _sep_tone_from_char_unicode(char)


@lru_cache(maxsize=160)
def _sep_tone_from_char_unicode(char: str):
    try:
        name = unicode_name(char)
        # print(name)
    except ValueError:
        return ('', char)
    nname = ''
    tone = ''

    for ti, tname in enumerate(TONE_NAMES):
        if tname in name:
            tone = TONES[ti]
            nname = name.replace(tname, '')
            break
    else:
        return ('', char)

    if nname.endswith('WITH '):
        nname = nname[:-5]
    elif nname.endswith('AND '):
        nname = nname[:-4]
    nname = nname.strip()

    try:
        new_char = unicode_lookup(nname)
        return (tone, new_char)
    except KeyError:
        raise


def place_tone_to_char(char, tone) -> str:
    try:
        return VOWEL_TONE_TO_CHAR[char][tone]
    except KeyError:
        return _place_tone_to_char_unicode(char, tone)


@lru_cache(maxsize=160)
def _place_tone_to_char_unicode(char, tone):
    name = unicode_name(char)

    if (tone != '') and (tone in TONES):
        if 'WITH' in name:
            name += ' AND '
        else:
            name += ' WITH '
        name += TONE_NAMES[TONES.index(tone)]

    return unicode_lookup(name)


def separate_tone(text: str, all=False):
    """Extract the tone mark from text.

    The returned tone is denoted as the following:
    '': unmarked (ngang)
    '/': acute accent (sắc)
    '\\': grave accent (huyền)
    '?': hook above (hỏi)
    '~': tilde (ngã)
    '.': dot below (nặng)

    Parameters
    ----------
    char : str
        The text from which the tone will be extracted
    all : bool, default : False
        If set to True, the last tone will be returned instead of the
        first one

    Returns
    -------
    tuple
        a tuple of the text without tone marks and its tone
    """

    text = nfc_normalize(text)
    tone = ''

    for i, lett in enumerate(text):
        tone, new_char = sep_tone_from_char(lett)

        if tone == '':
            continue
        else:
            text = text[:i] + new_char + text[i+1:]
        if not all:
            break

    return (text, tone)


def is_even_tone(tone: str) -> bool:
    return tone in {'', '\\'}


class DictBasedOnePassStrReplacer:
    def __init__(self, dictionary: dict, use_atomic_group=False, case_sensitive=True, word_boundary='') -> None:
        self.use_atomic_group = use_atomic_group
        self.case_sensitive = case_sensitive
        self.dictionary = dictionary
        regex_string = self._build_trie_regex_str(dictionary)
        regex_string = self._wrap_word_boundaries(regex_string, word_boundary)

        if case_sensitive:
            self.regex = re_compile(regex_string)
        else:
            self.regex = re_compile(regex_string, re_IGNORECASE)

    def _build_trie_regex_str(self, dictionary: dict):
        return self._trie_to_regex_str(self._make_trie(list(dictionary.keys())))
    
    def _wrap_word_boundaries(self, regex_string: str, word_boundary: str):
        if word_boundary == r'\b':
            regex_string = word_boundary + regex_string + word_boundary
        elif word_boundary:
            regex_string = rf"(?<!{word_boundary})" + \
                regex_string + rf"(?!{word_boundary})"
        return regex_string

    @classmethod
    def _make_trie(cls, strings: list) -> dict:
        full_trie = {}
        for string in strings:
            trie = full_trie
            for ch in string:
                if not (ch in trie):
                    trie[ch] = {}
                trie = trie[ch]
            trie['\0'] = None
        return full_trie

    @classmethod
    def _escape(cls, s: str) -> str:
        return re_escape(s.replace('/', r"\/")).replace(r'\ ', ' ')

    def _trie_to_regex_str(self, trie: dict, depth: int = 0) -> str:
        output = ""
        if not trie:
            return output
        if len(trie) == 2 and '\0' in trie:
            return "(?:" + next(self._escape(ch) + self._trie_to_regex_str(trie[ch], depth+1) for ch in trie if ch != '\0') + ")?"
        if len(trie) > 1:
            output += "(?>" if self.use_atomic_group else "(?:"
        first = True
        for ch, sub_trie in sorted(trie.items(), reverse=True):
            if first:
                first = False
            else:
                output += "|"
            if ch != '\0':
                output += self._escape(ch) + \
                    self._trie_to_regex_str(sub_trie, depth+1)
        if len(trie) > 1:
            output += ")"
        return output

    def _get_replacement(self, match: str):
        if self.case_sensitive:
            return self.dictionary[match]

        replacement: str = self.dictionary[match.lower()]
        if match == match.capitalize():
            if (match == match.title()) and any(c.isupper() for c in replacement):
                return replacement.title()
            else:
                return replacement[0].upper() + replacement[1:]
        elif match == match.upper():
            return replacement.upper()
        else:
            return replacement

    def replace(self, text: str) -> str:
        return self.regex.sub(lambda match: self._get_replacement(match.group()), text)

    def __call__(self, text: str) -> str:
        return self.replace(text)


def make_regex_str_from_tokens(tokens: list, use_atomic_group=False,
                               case_sensitive=True, word_boundary=''):
    replacer = DictBasedOnePassStrReplacer({}, use_atomic_group=use_atomic_group,
                                           case_sensitive=case_sensitive,
                                           word_boundary=word_boundary)
    regex_str = replacer._trie_to_regex_str(replacer._make_trie(tokens))
    return replacer._wrap_word_boundaries(regex_str, word_boundary)


def generate_tone_placement_replace_mapping(old_to_new=True, includes_rare_casing=False) -> dict:
    def reverse_sent_case(text):
        return text[0].lower() + text[1:].upper()

    mapping = {}
    for from_chars, to_chars in BASE_TONE_PLACEMENT_REPLACE_PAIRS:
        if not old_to_new:
            from_chars, to_chars = to_chars, from_chars

        mapping[from_chars] = to_chars
        mapping[from_chars.upper()] = to_chars.upper()
        mapping[from_chars.capitalize()] = to_chars.capitalize()
        if includes_rare_casing:
            mapping[reverse_sent_case(
                from_chars)] = reverse_sent_case(to_chars)

    return mapping


normalize_tone_placement_new_style = DictBasedOnePassStrReplacer(
    generate_tone_placement_replace_mapping())
normalize_tone_placement_old_style = DictBasedOnePassStrReplacer(
    generate_tone_placement_replace_mapping(old_to_new=False))


class IYNormalizer(DictBasedOnePassStrReplacer):
    ONSETS = ['qu', 'h', 'k', 'l', 'm', 's', 't', 'v',]

    LOWER_I_VARIANTS = 'iìíỉĩị'
    LOWER_Y_VARIANTS = 'yỳýỷỹỵ'
    I_VARIANTS = LOWER_I_VARIANTS + LOWER_I_VARIANTS.upper()
    Y_VARIANTS = LOWER_Y_VARIANTS + LOWER_Y_VARIANTS.upper()
    I_TO_Y_TRANS = str.maketrans(I_VARIANTS, Y_VARIANTS)
    Y_TO_I_TRANS = str.maketrans(Y_VARIANTS, I_VARIANTS)

    TRANS_TABLE_ROUTER = {
        'i': Y_TO_I_TRANS,
        'y': I_TO_Y_TRANS,
    }

    SYLLABLE_PATTERN = f"([{''.join(ONSETS[1:])}]|{ONSETS[0]})?[{LOWER_I_VARIANTS}{LOWER_Y_VARIANTS}]"

    POSSIBLE_PRESET_STYLES = (
        "i", "unified_i",
        "sinoviet_hklmqstv_y", "hklmqstv_y",
        "sinoviet_hklmqst_y", "hklmqst_y",
        "sinoviet_hklmqt_y", "hklmqt_y"
    )

    DEFAULT_I_OVERRIDE_LIST = [
        "hi hi", "hì hì", "hí hí", "hị hị", "hì hục", "hì hụi", "hỉ hả",
        "hỉ mũi", "hí hoáy", "hí húi", "hí hửng", "hí hởn", "hủ hỉ", "hậu hĩ",
        "ki bo", "ki cóp", "ki-lô-gam", "ki-ốt", "kì cạch", "kì cọ", "kì kèo",
        "kì cùng", "kì đà", "kì giông", "kí ninh", "kĩ tính", "kĩ càng",
        "cũ kĩ", "cụ kị", "ô li", "li bì", "li ti", "li-ti", "chi li",
        "cu li", "mi li", "lâm li", "va li", "phẳng lì", "nhẵn lì", "lì loà",
        "lì lợm", "lì xì", "lí nhí", "lũ lĩ", "kiết lị", "mi-ca", "mi-crô",
        "mi mắt", "cù mì", "lúa mì", "khoai mì", "bột mì", "mì sợi", "mì chính",
        "rễ mí", "tỉ mỉ", "mụ mị", "cây si", "nốt si", "si-lic", "đen sì",
        "hôi sì", "hàn sì", "sì sụp", "mua sỉ", "ti hí", "ti gôn", "ti-tan",
        "ti toe", "đinh ti", "ti trôn", "ti ti", "ti tỉ", "ti tiện", "tì tì",
        "tì vết", "tì tay", "tù tì", "tí toáy", "tí tách", "tí teo", "tí hon",
        "tỉ tê", "bạc tỉ", "tị nạnh", "tí ti", "ki ốt", "si đa",
        # Sino-Vietnamese words
        "ti tiện", "tự ti", "tị nạn", "ghen tị", "hồi tị", "tị nạnh",
    ]

    def __init__(self, use_atomic_group=False,
                 ignore_likely_proper_nouns=True,
                 h: Literal['i', 'y'] = 'y',
                 k='y',
                 l='y',
                 m='y',
                 qu='y',
                 s='i',
                 t='y',
                 v='i',
                 i='y',
                 use_sinoviet_heuristic=True,
                 i_override_list: Optional[Iterable[str]] = None,
                 max_repl_cache_size: Optional[int] = 0,
                 ) -> None:

        i_override_list = i_override_list
        actual_i_override_list = self.DEFAULT_I_OVERRIDE_LIST
        if i_override_list is not None:
            actual_i_override_list = i_override_list

        self.case_sensitive = False
        self.use_atomic_group = use_atomic_group
        self.ignore_likely_proper_nouns = ignore_likely_proper_nouns
        self.i_override_set = set(actual_i_override_list)
        self.use_sinoviet_heuristic = use_sinoviet_heuristic
        self.max_repl_cache_size = max_repl_cache_size

        self.dictionary = self._generate_exception_phrases_mapping(
            actual_i_override_list)

        regex_string = self._build_trie_regex_str(
            self.dictionary) + '|' + self.SYLLABLE_PATTERN
        regex_string = f"(?:{regex_string})"  # prevents lời from becoming lờy
        regex_string = self._wrap_word_boundaries(regex_string, r'\b')

        self.regex = re_compile(regex_string, re_IGNORECASE)

        trans_tables_router = {}
        trans_tables_router['h'] = self.TRANS_TABLE_ROUTER.get(h)
        trans_tables_router['k'] = self.TRANS_TABLE_ROUTER.get(k)
        trans_tables_router['l'] = self.TRANS_TABLE_ROUTER.get(l)
        trans_tables_router['m'] = self.TRANS_TABLE_ROUTER.get(m)
        trans_tables_router['qu'] = self.TRANS_TABLE_ROUTER.get(qu)
        trans_tables_router['s'] = self.TRANS_TABLE_ROUTER.get(s)
        trans_tables_router['t'] = self.TRANS_TABLE_ROUTER.get(t)
        trans_tables_router['v'] = self.TRANS_TABLE_ROUTER.get(v)
        trans_tables_router['i'] = self.TRANS_TABLE_ROUTER.get(i)

        for k, v in trans_tables_router.items():
            if v is None:
                if k == 'i':
                    raise ValueError(
                        f"Value for case of the standalone 'i' must be either 'i' or 'y'")
                else:
                    raise ValueError(
                        f"Value for the case of '{k}' onset consonant must be either 'i' or 'y'")

        self.trans_tables_router = trans_tables_router

    @classmethod
    def _generate_exception_phrases_mapping(cls, phrases: Iterable[str]) -> Dict:
        actual_syllable_pattern = fr"^{cls.SYLLABLE_PATTERN}[ -]?$"
        syllable_regex = re_compile(actual_syllable_pattern, re_IGNORECASE)
        tokenize_regex = re_compile(r"\w+[ -]?", re_IGNORECASE)
        results = {}
        for phrase in phrases:
            syllables = tokenize_regex.findall(phrase)
            combination_choices = []
            for syllable in syllables:
                match = syllable_regex.match(syllable)
                if match:
                    combination_choices.append(
                        (syllable.translate(cls.Y_TO_I_TRANS), syllable.translate(cls.I_TO_Y_TRANS)))
                else:
                    combination_choices.append((syllable, syllable))

            for combination in product(*combination_choices):
                results[''.join(combination)] = phrase

        return results

    @classmethod
    def from_preset_style(cls,
                          style:
                          Literal["i", "unified_i",
                                  "sinoviet_hklmqstv_y", "hklmqstv_y",
                                  "sinoviet_hklmqst_y", "hklmqst_y",
                                  "sinoviet_hklmqt_y", "hklmqt_y"]
                          = "sinoviet_hklmqt_y",
                          use_atomic_group=False,
                          ignore_likely_proper_nouns=True,
                          i_override_list=None,
                          max_repl_cache_size: Optional[int] = 0,
                          ) -> IYNormalizer:
        if style == "i":
            return IYNormalizer(
                use_atomic_group, ignore_likely_proper_nouns,
                h='i', k='i', l='i', m='i', qu='i', s='i', t='i', v='i', i='i',
                use_sinoviet_heuristic=False, i_override_list=[], max_repl_cache_size=max_repl_cache_size)
        elif style == "unified_i":
            return IYNormalizer(
                use_atomic_group, ignore_likely_proper_nouns,
                h='i', k='i', l='i', m='i', qu='y', s='i', t='i', v='i', i='y',
                use_sinoviet_heuristic=False, i_override_list=i_override_list, max_repl_cache_size=max_repl_cache_size)
        elif style == "sinoviet_hklmqstv_y":
            return IYNormalizer(
                use_atomic_group, ignore_likely_proper_nouns,
                h='y', k='y', l='y', m='y', qu='y', s='y', t='y', v='y', i='y',
                use_sinoviet_heuristic=True, i_override_list=i_override_list, max_repl_cache_size=max_repl_cache_size)
        elif style == "hklmqstv_y":
            return IYNormalizer(
                use_atomic_group, ignore_likely_proper_nouns,
                h='y', k='y', l='y', m='y', qu='y', s='y', t='y', v='y', i='y',
                use_sinoviet_heuristic=False, i_override_list=i_override_list, max_repl_cache_size=max_repl_cache_size)
        elif style == "sinoviet_hklmqst_y":
            return IYNormalizer(
                use_atomic_group, ignore_likely_proper_nouns,
                h='y', k='y', l='y', m='y', qu='y', s='y', t='y', v='i', i='y',
                use_sinoviet_heuristic=True, i_override_list=i_override_list, max_repl_cache_size=max_repl_cache_size)
        elif style == "hklmqst_y":
            return IYNormalizer(
                use_atomic_group, ignore_likely_proper_nouns,
                h='y', k='y', l='y', m='y', qu='y', s='y', t='y', v='i', i='y',
                use_sinoviet_heuristic=False, i_override_list=i_override_list, max_repl_cache_size=max_repl_cache_size)
        elif style == "sinoviet_hklmqt_y":
            return IYNormalizer(
                use_atomic_group, ignore_likely_proper_nouns,
                h='y', k='y', l='y', m='y', qu='y', s='i', t='y', v='i', i='y',
                use_sinoviet_heuristic=True, i_override_list=i_override_list, max_repl_cache_size=max_repl_cache_size)
        elif style == "hklmqt_y":
            return IYNormalizer(
                use_atomic_group, ignore_likely_proper_nouns,
                h='y', k='y', l='y', m='y', qu='y', s='i', t='y', v='i', i='y',
                use_sinoviet_heuristic=False, i_override_list=i_override_list, max_repl_cache_size=max_repl_cache_size)
        else:
            return IYNormalizer()

    @property
    def max_repl_cache_size(self):
        return self._max_repl_cache_size

    @max_repl_cache_size.setter
    def max_repl_cache_size(self, value: Optional[int]):
        if value == 0:
            self._get_non_exceptional_replacement = self.__get_non_exceptional_replacement
            self._get_replacement_maybe_cached = self._get_replacement
        else:
            self._get_non_exceptional_replacement = lru_cache(
                maxsize=value)(self.__get_non_exceptional_replacement)
            self._get_replacement_maybe_cached = lru_cache(
                maxsize=value)(self._get_replacement)
        self._max_repl_cache_size = value

    def _get_normalized_form(self, match: re_Match):
        match_str: str = match.group()
        if self.ignore_likely_proper_nouns:
            if match_str == match_str.capitalize():
                match_pos = match.pos
                if match_pos > 0:  # not at the start of the string
                    return match_str

        if not match.group(1) and (len(match_str) > 1):  # exception phrase found
            return self._get_replacement_maybe_cached(match_str)
        else:
            onset = (match.group(1) or '').lower()
            return self._get_non_exceptional_replacement(match_str, onset)

    def __get_non_exceptional_replacement(self, match_str: str, onset: str) -> str:
        if self.use_sinoviet_heuristic:
            match_lower_str = match_str.lower()
            # non-existent Sino-Vietnamese tokens
            # Source: https://ling.ussh.vnu.edu.vn/vi/nghien-cuu-khoa-hoc/chuong-trinh-de-tai-du-an/ban-tiep-ve-chuyen-i-ngan-y-dai-605.html
            if match_lower_str in {'hỳ', 'lỳ', 'lỷ', 'lỹ', 'mỷ', 'mý', 'sỳ', 'sý', 'sỵ', 'tỹ'}:
                return match_str.translate(self.Y_TO_I_TRANS)
            # non-existent non-Sino-Vietnamese tokens
            elif match_lower_str in {'kỉ', 'lỉ', 'mĩ', 'sí'}:
                return match_str.translate(self.I_TO_Y_TRANS)
            elif match_lower_str in {'hì', 'lì', 'lỉ', 'lĩ', 'mỉ', 'mí', 'sì', 'sí', 'sị', 'tĩ', 'kỷ', 'lỷ', 'mỹ', 'sý', }:
                return match_str

        if onset:
            return match_str.translate(self.trans_tables_router[onset])
        else:
            return match_str.translate(self.trans_tables_router['i'])

    def replace(self, text: str) -> str:
        return self.regex.sub(lambda match: self._get_normalized_form(match), text)

    def __call__(self, text: str) -> str:
        return self.replace(text)


_TEXT_NORMALIZE_REPLACE_TRANSLATIONS = str.maketrans(
    '：“”‘’ー  \u200b\ufeff「」【】«»『』《》〖〗〔〕', ':""\'\'-    """"""""""""""')
_TEXT_NORMALIZE_REMOVE_TRANSLATIONS = str.maketrans('', '', '└*♪＊★♥')
_TEXT_NORMALIZE_REMOVE_PUNCT_TRANS = str.maketrans(
    '', '', r"!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~")


def normalize_text(text: str, clean_redudant_spaces=True,
                   strip_punctuation=False,
                   do_normalize_confusables=False,
                   normalize_tone_placement=True):

    text = nfc_normalize(text.strip()).translate(
        _TEXT_NORMALIZE_REPLACE_TRANSLATIONS).translate(_TEXT_NORMALIZE_REMOVE_TRANSLATIONS)
    if do_normalize_confusables:
        text = normalize_confusables(text)
    if strip_punctuation:
        text = text.translate(_TEXT_NORMALIZE_REMOVE_PUNCT_TRANS)
    if clean_redudant_spaces:
        text = re_sub(r" +", " ", text)
    text = re_sub(r"([!?])\1{1,}", r"\1", text)
    text = re_sub('-{2,}', '', text)
    text = re_sub(r'\.{4,}|…', '...', text)
    if normalize_tone_placement:
        text = normalize_tone_placement_new_style(text)
    return text.strip()


_CLEAN_SLUG_SPACES_REGEX = re_compile(r'[ -]+')


def clean_slug(text: str, sep='_'):
    slug = remove_diacritics(text.lower())
    slug = NON_WORD_CHARS_REGEX.sub('', slug)
    return _CLEAN_SLUG_SPACES_REGEX.sub(sep, slug)
