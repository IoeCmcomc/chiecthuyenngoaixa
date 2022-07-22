# -*- coding: utf-8 -*-

import unicodedata
from misc import separate_tone

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