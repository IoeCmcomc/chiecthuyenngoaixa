# -*- coding: utf-8 -*-

import unicodedata
from unicodedata import name as unicode_name, lookup as unicode_lookup
from functools import lru_cache

from .constants import TONES, TONE_NAMES, NO_TONE_CHAR_TRANS

def normalize(text: str) -> str:
    return unicodedata.normalize('NFC', text)

def remove_tones(text: str) -> str:
    return text.translate(NO_TONE_CHAR_TRANS)

def remove_diacritics(text: str) -> str:
    SPECIAL_TRANS = str.maketrans('đĐ', 'dD')
    return unicodedata.normalize('NFKD', text.translate(SPECIAL_TRANS)).encode('ascii', 'ignore').decode()

@lru_cache(maxsize=160)
def sep_tone_from_char(char: str):
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
        print(i, name, nname, tone, text[i-5:i+5])
        raise

def separate_tone(text: str, all=False):
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