# -*- coding: utf-8 -*-

"""This module contains legacy functions, classes and unused functions."""

import unicodedata
from .misc import separate_tone
from .constants import CHAR_ORDER_DICT

def remove_tones(t):
    tletters_dict = {'a': 'a', 'à': 'a', 'á': 'a', 'ả': 'a', 'ã': 'a', 'ạ': 'a', 'ă': 'ă', 'ằ': 'ă', 'ắ': 'ă', 'ẳ': 'ă', 'ẵ': 'ă', 'ặ': 'ă', 'â': 'â', 'ầ': 'â', 'ấ': 'â', 'ẩ': 'â', 'ẫ': 'â', 'ậ': 'â', 'e': 'e', 'è': 'e', 'é': 'e', 'ẻ': 'e', 'ẽ': 'e', 'ẹ': 'e', 'ê': 'ê', 'ề': 'ê', 'ế': 'ê', 'ể': 'ê', 'ễ': 'ê', 'ệ': 'ê', 'i': 'i', 'ì': 'i', 'í': 'i', 'ỉ': 'i', 'ĩ': 'i', 'ị': 'i', 'o': 'o', 'ò': 'o', 'ó': 'o', 'ỏ': 'o', 'õ': 'o', 'ọ': 'o', 'ô': 'ô', 'ồ': 'ô', 'ố': 'ô', 'ổ': 'ô', 'ỗ': 'ô', 'ộ': 'ô', 'ơ': 'ơ', 'ờ': 'ơ', 'ớ': 'ơ', 'ở': 'ơ', 'ỡ': 'ơ', 'ợ': 'ơ', 'u': 'u', 'ù': 'u', 'ú': 'u', 'ủ': 'u', 'ũ': 'u', 'ụ': 'u', 'ư': 'ư', 'ừ': 'ư', 'ứ': 'ư', 'ử': 'ư', 'ữ': 'ư', 'ự': 'ư', 'y': 'y', 'ỳ': 'y', 'ý': 'y', 'ỷ': 'y', 'ỹ': 'y', 'ỵ': 'y', 'A': 'A', 'À': 'A', 'Á': 'A', 'Ả': 'A', 'Ã': 'A', 'Ạ': 'A', 'Ă': 'Ă', 'Ằ': 'Ă', 'Ắ': 'Ă', 'Ẳ': 'Ă', 'Ẵ': 'Ă', 'Ặ': 'Ă', 'Â': 'Â', 'Ầ': 'Â', 'Ấ': 'Â', 'Ẩ': 'Â', 'Ẫ': 'Â', 'Ậ': 'Â', 'E': 'E', 'È': 'E', 'É': 'E', 'Ẻ': 'E', 'Ẽ': 'E', 'Ẹ': 'E', 'Ê': 'Ê', 'Ề': 'Ê', 'Ế': 'Ê', 'Ể': 'Ê', 'Ễ': 'Ê', 'Ệ': 'Ê', 'I': 'I', 'Ì': 'I', 'Í': 'I', 'Ỉ': 'I', 'Ĩ': 'I', 'Ị': 'I', 'O': 'O', 'Ò': 'O', 'Ó': 'O', 'Ỏ': 'O', 'Õ': 'O', 'Ọ': 'O', 'Ô': 'Ô', 'Ồ': 'Ô', 'Ố': 'Ô', 'Ổ': 'Ô', 'Ỗ': 'Ô', 'Ộ': 'Ô', 'Ơ': 'Ơ', 'Ờ': 'Ơ', 'Ớ': 'Ơ', 'Ở': 'Ơ', 'Ỡ': 'Ơ', 'Ợ': 'Ơ', 'U': 'U', 'Ù': 'U', 'Ú': 'U', 'Ủ': 'U', 'Ũ': 'U', 'Ụ': 'U', 'Ư': 'Ư', 'Ừ': 'Ư', 'Ứ': 'Ư', 'Ử': 'Ư', 'Ữ': 'Ư', 'Ự': 'Ư', 'Y': 'Y', 'Ỳ': 'Y', 'Ý': 'Y', 'Ỷ': 'Y', 'Ỹ': 'Y', 'Ỵ': 'Y', b'\xcc\x81'.decode() : '', b'\xcc\x80'.decode() : '', b'\xcc\x89'.decode() : '', b'\xcc\x83'.decode() : '', b'\xcc\xa3'.decode() : ''}
    r = ''    
    for c in t:
            r += tletters_dict.get(c, c)
    return r

def separate_syllable(t):
    head_consonants = ('b', 'ch', 'c', 'd', 'đ', 'gh', 'gi', 'g', 'h', 'kh', 'k', 'l', 'm', 'ngh', 'ng', 'nh', 'ng',
    'n', 'ph', 'p', 'qu', 'r', 's', 'th', 'tr', 't', 'v', 'x')
    wowels = ('a', 'ă', 'â', 'e', 'ê', 'i', 'o', 'ô', 'ơ', 'u', 'ư', 'y')
    diphthongs = ('ai', 'ao', 'au', 'ay', 'âu', 'ây', 'eo', 'êu', 'ia', 'iê', 'iu', 'oa', 'oe', 'oi',
    'oo', 'ôi',    'ơi', 'ua', 'uâ', 'uê', 'ui', 'uô', 'uơ', 'uy', 'ưa', 'ưi', 'ươ', 'ưu', 'yê')
    triphthongs = ('iêu', 'oai', 'oay', 'uay', 'uây', 'uya', 'ươi', 'ươu', 'yêu')
    special_triphthongs = ('uyê',)
    phthongs = special_triphthongs + triphthongs + diphthongs + wowels
    tail_consonants = ('ch', 'c', 'm', 'ng', 'nh', 'n', 'p', 't')
    
    r = []
    t = unicodedata.normalize('NFC', t)
    if ' ' in t: return
    
    r.append('')
    for part in head_consonants:
        tl = t.lower()
        if tl.startswith(part):
            r[-1] = t[:len(part)]
            t = t[len(part):]
            break
    
    t, tone = separate_tone(t)
    
    r.append('')
    for part in phthongs:
        tl = t.lower()
        if tl.startswith(part):
            r[-1] = t[:len(part)]
            t = t[len(part):]
            break
    
    r.append('')
    for part in tail_consonants:
        tl = t.lower()
        if tl.startswith(part):
            r[-1] = t[:len(part)]
            t = t[len(part):]
            break
    
    r.append(tone)
    
    return r

def merge_tone(lett, atone):
    tones = ('(Placeholder)', '\\', '/', '?', '~', '.')
    tone_names = ('', 'GRAVE', 'ACUTE', 'HOOK ABOVE', 'TILDE', 'DOT BELOW')
    
    name = unicodedata.name(lett)
    
    for i, tone in enumerate(tones):
        if atone == tone:
            if 'WITH' in name:
                name += ' AND '
            else:
                name += ' WITH '
            name += tone_names[i]
            break
    
    return unicodedata.lookup(name)

def merge_syllable(hcon  , phthong, tcon, tone, old=False):
    special_triphthongs = ('uyê',)
    high_priorites = ('ê', 'ơ')
    
    phth_list = list(phthong)
    
    def new_rule(phthong):
        if len(phthong) == 1:
            phth_list[0] = merge_tone(phthong, tone)
        elif len(phthong) == 2:
            if phthong == 'ua':
                if hcon == 'q':
                    phth_list[1] = merge_tone(phth_list[1], tone)
                else:
                    phth_list[0] = merge_tone(phth_list[0], tone)
            elif phthong.startswith(('u', 'o')) \
            or phth_list[1] in {'â', 'ê', 'ô', 'ơ', 'ư'}:
                phth_list[1] = merge_tone(phth_list[1], tone)
            else:
                phth_list[0] = merge_tone(phth_list[0], tone)
        elif len(phthong) == 3:
            if phthong in special_triphthongs:
                phth_list[2] = merge_tone(phth_list[2], tone)
            else:
                phth_list[1] = merge_tone(phth_list[1], tone)
        return ''.join(phth_list)
    
    def old_rule(phthong):
        for x in high_priorites:
            if x in phthong:
                i = phth_list.index(x)
                phth_list[i] = merge_tone(phth_list[i], tone)
                break
        else:
            if len(phthong) == 1:
                phth_list[0] = merge_tone(phth_list[0], tone)
            elif len(phthong) == 2:
                if tcon == '':
                    phth_list[0] = merge_tone(phth_list[0], tone)
                else:
                    phth_list[1] = merge_tone(phth_list[1], tone)
            elif len(phthong) == 3:
                phth_list[1] = merge_tone(phth_list[1], tone)
        return ''.join(phth_list)

    if hcon == 'c' and phthong[0] in {'e', 'ê', 'i', 'y'}:
        hcon = 'k'
    if hcon == 'k' and phthong[0] not in {'e', 'ê', 'i', 'y'}:
        hcon = 'c'
    if hcon == 'ng' and phthong[0] in {'e', 'ê', 'i'}:
        hcon = 'ngh'
    if hcon == 'ngh' and phthong[0] not in {'e', 'ê', 'i'}:
        hcon = 'ng'

    # if tcon in ("c", "p", "t"):
        # if tone in ("", "\\", "?"): tone = "."
        # elif tone == "~": tone = "/"
    
    if old:
        return ''.join((hcon, old_rule(phthong), tcon))
    else:
        return ''.join((hcon, new_rule(phthong), tcon))

def noilais(w):
    def noilai_sub(syll_list, type = 0):
        for i in range(len(syll_list) // 2):
            syll1 = syll_list[i]
            syll2 = syll_list[-(i+1)]
            syll1_parts = separate_syllable(syll1)
            syll2_parts = separate_syllable(syll2)
            if type == 0:
                syll1_parts[0], syll2_parts[0] = syll2_parts[0], syll1_parts[0]
            elif type == 1:
                syll1_parts[1], syll2_parts[1] = syll2_parts[1], syll1_parts[1]
                syll1_parts[2], syll2_parts[2] = syll2_parts[2], syll1_parts[2]
            elif type == 2:
                syll1_parts[3], syll2_parts[3] = syll2_parts[3], syll1_parts[3]
            syll1 = merge_syllable(*syll1_parts)
            syll2 = merge_syllable(*syll2_parts)
            syll_list[i] = syll1
            syll_list[-(i+1)] = syll2
        return ' '.join(syll_list)
    
    r = list()
    w_sylls = w.split(' ')
    reversed_w_sylls = w_sylls[::-1]
    for i in range(3):
        r.append(noilai_sub(w_sylls, i))
        r.append(noilai_sub(reversed_w_sylls, i))
    return r

class visorted_key:
    def __init__(self, t=''):
        self.t = t
        self.untoned = remove_tones(t)

    def __repr__(self):
        return "<visort_key #{} '{}' ('{}')>".format(id(self), self.t, self.untoned)

    def __lt__(self, other):
        len_st, len_ot = len(self.t), len(other.t)
        d = CHAR_ORDER_DICT
        for i in range(min(len(self.t), len(other.t))):
            if self.t[i] != other.t[i]:
                if self.untoned[i] == other.untoned[i]:
                    if len_st != len_ot:
                        return len_st < len_ot
                if self.t[i] in d and other.t[i] in d:
                    return d[self.t[i]] < d[other.t[i]]
                else:
                    return self.t[i] < other.t[i]
        else:
            return len(self.t) < len(other.t)