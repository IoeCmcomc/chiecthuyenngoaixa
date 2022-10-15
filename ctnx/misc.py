# -*- coding: utf-8 -*-

from unicodedata import name as unicode_name, lookup as unicode_lookup, normalize as unicode_normalize
from functools import lru_cache

from .constants import TONES, TONE_NAMES, NO_TONE_CHAR_TRANS

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
        return ('', '')
    nname = ''
    tone = ''
        
    for ti, tname in enumerate(TONE_NAMES):
        if tname in name:
            tone = TONES[ti]
            nname = name.replace(tname, '')
            break
    else:
        return ('', '')
        
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