# -*- coding: utf-8 -*-

from unicodedata import name as unicode_name, lookup as unicode_lookup, normalize as unicode_normalize
from functools import lru_cache
from re import compile as re_compile, escape as re_escape, IGNORECASE as re_IGNORECASE

from .constants import TONES, TONE_NAMES, NO_TONE_CHAR_TRANS, CONFUSABLE_CHAR_TRANS, BASE_TONE_PLACEMENT_REPLACE_PAIRS

def normalize_confusables(text: str) -> str:
    """Converts a confusable text to a potentially normal text.
    
    Replace similar-looking characters and homoglyphs with theirs equivalent
    Vietnamese characters. Small cap letters will be converted to lowercase.
    """
    return text.translate(CONFUSABLE_CHAR_TRANS)

def normalize(text: str) -> str:
    """Converts combining Unicode characters to theirs equivalent precomposed characters."""
    return unicode_normalize('NFC', text)

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

@lru_cache(maxsize=160)
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
        name = unicode_name(char)
        #print(name)
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

    text = normalize(text)
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
        if word_boundary == r'\b':
            regex_string = word_boundary + regex_string + word_boundary
        elif word_boundary:
            regex_string = rf"(?<!{word_boundary})" + regex_string + rf"(?!{word_boundary})"
        if case_sensitive:
            self.regex = re_compile(regex_string)
        else:
            self.regex = re_compile(regex_string, re_IGNORECASE)

    def _build_trie_regex_str(self, dictionary: dict):
        return self._trie_to_regex_str(self._make_trie(list(dictionary.keys())))

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
                output += self._escape(ch) + self._trie_to_regex_str(sub_trie, depth+1)
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
            mapping[reverse_sent_case(from_chars)] = reverse_sent_case(to_chars)
    
    return mapping

normalize_tone_placement_new_style = DictBasedOnePassStrReplacer(generate_tone_placement_replace_mapping())
normalize_tone_placement_old_style = DictBasedOnePassStrReplacer(generate_tone_placement_replace_mapping(old_to_new=False))