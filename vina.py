# -*- coding: utf-8 -*-

import unicodedata
import time
from pprint import pprint
from random import shuffle


order = r"0123456789aAàÀáÁảẢãÃạẠăĂằẰắẮẳẲẵẴặẶâÂầẦẩẨẫẪấẤậẬbBcCdDđĐeEèÈéÉẻẺẽẼẹẸêÊềỀếẾểỂễỄệỆfFgGhHiIìÌíÍỉỈĩĨịỊjJkKlLmMnNoOòÒóÓỏỎõÕọỌôÔồỒốỐổỔỗỖộỘơƠờỜớỚởỞỡỠợỢpPqQrRsStTuUùÙúÚủỦũŨụỤưƯừỪứỨửỬữỮựỰvVwWxXyYỳỲýÝỷỶỹỸỵỴzZ"
order_dict = {letter:order.index(letter) for letter in order}

full_order_dict = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'a': 10,'A': 11, 'à': 12, 'À': 13, 'á': 14, 'Á': 15,'ả': 16, 'Ả': 17, 'ã': 18, 'Ã': 19, 'ạ': 20,'Ạ': 21, 'ă': 22, 'Ă': 23, 'ằ': 24, 'Ằ': 25,'ắ': 26, 'Ắ': 27, 'ẳ': 28, 'Ẳ': 29, 'ẵ': 30,'Ẵ': 31, 'ặ': 32, 'Ặ': 33, 'â': 34, 'Â': 35,'ầ': 36, 'Ầ': 37, 'ẩ': 38, 'Ẩ': 39, 'ẫ': 40,'Ẫ': 41, 'ấ': 42, 'Ấ': 43, 'ậ': 44, 'Ậ': 45,'b': 46, 'B': 47, 'c': 48, 'C': 49, 'd': 50,'D': 51, 'đ': 52, 'Đ': 53, 'e': 54, 'E': 55,'è': 56, 'È': 57, 'é': 58, 'É': 59, 'ẻ': 60,'Ẻ': 61, 'ẽ': 62, 'Ẽ': 63, 'ẹ': 64, 'Ẹ': 65,'ê': 66, 'Ê': 67, 'ề': 68, 'Ề': 69, 'ế': 70,'Ế': 71, 'ể': 72, 'Ể': 73, 'ễ': 74, 'Ễ': 75,'ệ': 76, 'Ệ': 77, 'f': 78, 'F': 79, 'g': 80,'G': 81, 'h': 82, 'H': 83, 'i': 84, 'I': 85,'ì': 86, 'Ì': 87, 'í': 88, 'Í': 89, 'ỉ': 90,'Ỉ': 91, 'ĩ': 92, 'Ĩ': 93, 'ị': 94, 'Ị': 95,'j': 96, 'J': 97, 'k': 98, 'K': 99, 'l': 100, 'L': 101, 'm': 102, 'M': 103, 'n': 104, 'N': 105, 'o': 106, 'O': 107, 'ò': 108, 'Ò': 109, 'ó': 110, 'Ó': 111, 'ỏ': 112, 'Ỏ': 113, 'õ': 114, 'Õ': 115, 'ọ': 116, 'Ọ': 117, 'ô': 118, 'Ô': 119, 'ồ': 120, 'Ồ': 121, 'ố': 122, 'Ố': 123, 'ổ': 124, 'Ổ': 125, 'ỗ': 126, 'Ỗ': 127, 'ộ': 128, 'Ộ': 129, 'ơ': 130, 'Ơ': 131, 'ờ': 132, 'Ờ': 133, 'ớ': 134, 'Ớ': 135, 'ở': 136, 'Ở': 137, 'ỡ': 138, 'Ỡ': 139, 'ợ': 140, 'Ợ': 141, 'p': 142, 'P': 143, 'q': 144, 'Q': 145, 'r': 146, 'R': 147, 's': 148, 'S': 149, 't': 150, 'T': 151, 'u': 152, 'U': 153, 'ù': 154, 'Ù': 155, 'ú': 156, 'Ú': 157, 'ủ': 158, 'Ủ': 159, 'ũ': 160, 'Ũ': 161, 'ụ': 162, 'Ụ': 163, 'ư': 164, 'Ư': 165, 'ừ': 166, 'Ừ': 167, 'ứ': 168, 'Ứ': 169, 'ử': 170, 'Ử': 171, 'ữ': 172, 'Ữ': 173, 'ự': 174, 'Ự': 175, 'v': 176, 'V': 177, 'w': 178, 'W': 179, 'x': 180, 'X': 181, 'y': 182, 'Y': 183, 'ỳ': 184, 'Ỳ': 185, 'ý': 186, 'Ý': 187, 'ỷ': 188, 'Ỷ': 189, 'ỹ': 190, 'Ỹ': 191, 'ỵ': 192, 'Ỵ': 193, 'z': 194, 'Z': 195}

def deaccent(t):
    r = t.replace('Đ', 'D').replace('đ', 'd')
    r = unicodedata.normalize('NFKD', r).encode('ascii', 'ignore').decode()
    return r


def numtotext(n):
    digits = ('không', 'một', 'hai', 'ba', 'bốn', 'năm', 'sáu', 'bảy', 'tám', 'chín', 'mười')
    levels = ('đơn vị', 'nghìn', 'triệu')
    
    def per_digit(n):
        return [digits[int(s)] for s in str(n)]
    
    def per_thousand(n, linh=False):
        tarr = []
        if 100 <= n <= 999:
            n1, n2 = divmod(n, 100)
            tarr.append(digits[n1])
            tarr.append('trăm')
            if 1 <= n2 <= 9:
                tarr.append('linh')
            n = n2
        if 1 <= n <= 10:
            if linh:
                tarr.append('linh')
            tarr.append(digits[n])
        elif n <= 99 and n != 0:
            n1, n2 = divmod(n, 10)
            ele = digits[n2]
            if n1 == 1:
                tarr.append('mười')
            else:
                tarr.append(digits[n1])
                tarr.append('mươi')
                if n2 == 1:
                    ele = 'mốt'
                elif n2 == 4:
                    ele = 'tư'
            if n2 == 5:
                ele = 'lăm'
            if ele != 'không': tarr.append(ele)
        return tarr
    
    tarr = []
    if not isinstance(n, (int, float)):
        raise Exception('Invaild type. The first parameter must be an integer or a float.')
    if int(n) == 0:
        tarr.append('không')
    elif int(n) < 0:
        tarr.append('âm')
        n = abs(n)
    ns = str(n)
    if isinstance(n, float) and '.' in ns:
        decimal = True
        intn, decn = ns.split('.')
        ns = intn
    else:
        decimal = False
    
    length = len(ns)
    splited = [ns[0:len(ns) % 3]] + [ns[i:i+3] for i in range(len(ns) % 3, len(ns), 3)]
    splited = list(filter(None, splited))
    
    for part in splited:
        pn = int(part)
        if pn != 0:
            if part[0] == '0' and 1 <= pn <= 99:
                tarr.append('không trăm')
                linh = True
            else:
                linh = False
            tarr.extend(per_thousand(pn, linh))
            bilis, thous = divmod((length - 1) // 3, 3)
            if thous > 0:
                tarr.append(levels[thous])
            tarr.extend(['tỉ'] * bilis)
        length -= 3
    
    if decimal:
        tarr.append('phẩy')
        if len(decn) == 2 and decn[0] == 1:
            tarr.extend(per_thousand(int(decn)))
        else:
            tarr.extend(per_digit(int(decn)))
    tarr = list(filter(None, tarr))
    return ' '. join(tarr)

def separate_tone(t, id=False, all=False):
    tones = ('', '\\', '/', '?', '~', '.')
    tone_names = ('(Placeholder)', 'GRAVE', 'ACUTE', 'HOOK ABOVE', 'TILDE', 'DOT BELOW')
    t = unicodedata.normalize('NFC', t)
    
    for i, lett in enumerate(t):
        tone = tones[0]
        try:
            name = unicodedata.name(lett)
        except ValueError:
            continue
        nname = ''
        
        for ti, tname in enumerate(tone_names):
            if tname in name:
                tone = tones[ti]
                nname = name.replace(tname, '')
                break
        
        if nname.endswith('WITH '):
            nname = nname[:-5]
        elif nname.endswith('AND '):
            nname = nname[:-4]
        nname = nname.strip()
        
        if nname != '':
            t = list(t)
            try:
                t[i] = unicodedata.lookup(nname)
            except KeyError:
                print(i, name, nname, tone, t[i-5:i+5])
                raise KeyError
            t = ''.join(t)
        
        if tone != '' and not all: break
    
    if not id:
        return [t, ''+tone]
    else:
        return [t, ti] if tone != '' else [t, -1]

def separate_syllable(t):
    head_consonants = ('b', 'ch', 'c', 'd', 'đ', 'gh', 'gi', 'g', 'h', 'kh', 'k', 'l', 'm', 'ngh', 'ng', 'nh', 'ng',
    'n', 'ph', 'p', 'qu', 'r', 's', 'th', 'tr', 't', 'v', 'x')
    wowels = ('a', 'ă', 'â', 'e', 'ê', 'i', 'o', 'ô', 'ơ', 'u', 'ư', 'y')
    diphthongs = ('ai', 'ao', 'au', 'ay', 'âu', 'ây', 'eo', 'êu', 'ia', 'iê', 'iu', 'oa', 'oe', 'oi',
    'oo', 'ôi',    'ơi', 'ua', 'uâ', 'uê', 'ui', 'uô', 'uơ', 'uy', 'ưa', 'ưi', 'ươ', 'ưu')
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

def merge_tone(lett, tone):
    tones = ('(Placeholder)', '\\', '/', '?', '~', '.')
    tone_names = ('', 'GRAVE', 'ACUTE', 'HOOK ABOVE', 'TILDE', 'DOT BELOW')
    
    name = unicodedata.name(lett)
    
    for ti, ton in enumerate(tones):
        if tone == ton:
            if 'WITH' in name:
                name += ' AND '
            else:
                name += ' WITH '
            name += tone_names[ti]
            break
    
    return unicodedata.lookup(name)

def merge_syllable(hcon, phthong, tcon, tone, old=False):
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
    order_dict = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'a': 10,'A': 11, 'à': 12, 'À': 13, 'á': 14, 'Á': 15,'ả': 16, 'Ả': 17, 'ã': 18, 'Ã': 19, 'ạ': 20,'Ạ': 21, 'ă': 22, 'Ă': 23, 'ằ': 24, 'Ằ': 25,'ắ': 26, 'Ắ': 27, 'ẳ': 28, 'Ẳ': 29, 'ẵ': 30,'Ẵ': 31, 'ặ': 32, 'Ặ': 33, 'â': 34, 'Â': 35,'ầ': 36, 'Ầ': 37, 'ẩ': 38, 'Ẩ': 39, 'ẫ': 40,'Ẫ': 41, 'ấ': 42, 'Ấ': 43, 'ậ': 44, 'Ậ': 45,'b': 46, 'B': 47, 'c': 48, 'C': 49, 'd': 50,'D': 51, 'đ': 52, 'Đ': 53, 'e': 54, 'E': 55,'è': 56, 'È': 57, 'é': 58, 'É': 59, 'ẻ': 60,'Ẻ': 61, 'ẽ': 62, 'Ẽ': 63, 'ẹ': 64, 'Ẹ': 65,'ê': 66, 'Ê': 67, 'ề': 68, 'Ề': 69, 'ế': 70,'Ế': 71, 'ể': 72, 'Ể': 73, 'ễ': 74, 'Ễ': 75,'ệ': 76, 'Ệ': 77, 'f': 78, 'F': 79, 'g': 80,'G': 81, 'h': 82, 'H': 83, 'i': 84, 'I': 85,'ì': 86, 'Ì': 87, 'í': 88, 'Í': 89, 'ỉ': 90,'Ỉ': 91, 'ĩ': 92, 'Ĩ': 93, 'ị': 94, 'Ị': 95,'j': 96, 'J': 97, 'k': 98, 'K': 99, 'l': 100, 'L': 101, 'm': 102, 'M': 103, 'n': 104, 'N': 105, 'o': 106, 'O': 107, 'ò': 108, 'Ò': 109, 'ó': 110, 'Ó': 111, 'ỏ': 112, 'Ỏ': 113, 'õ': 114, 'Õ': 115, 'ọ': 116, 'Ọ': 117, 'ô': 118, 'Ô': 119, 'ồ': 120, 'Ồ': 121, 'ố': 122, 'Ố': 123, 'ổ': 124, 'Ổ': 125, 'ỗ': 126, 'Ỗ': 127, 'ộ': 128, 'Ộ': 129, 'ơ': 130, 'Ơ': 131, 'ờ': 132, 'Ờ': 133, 'ớ': 134, 'Ớ': 135, 'ở': 136, 'Ở': 137, 'ỡ': 138, 'Ỡ': 139, 'ợ': 140, 'Ợ': 141, 'p': 142, 'P': 143, 'q': 144, 'Q': 145, 'r': 146, 'R': 147, 's': 148, 'S': 149, 't': 150, 'T': 151, 'u': 152, 'U': 153, 'ù': 154, 'Ù': 155, 'ú': 156, 'Ú': 157, 'ủ': 158, 'Ủ': 159, 'ũ': 160, 'Ũ': 161, 'ụ': 162, 'Ụ': 163, 'ư': 164, 'Ư': 165, 'ừ': 166, 'Ừ': 167, 'ứ': 168, 'Ứ': 169, 'ử': 170, 'Ử': 171, 'ữ': 172, 'Ữ': 173, 'ự': 174, 'Ự': 175, 'v': 176, 'V': 177, 'w': 178, 'W': 179, 'x': 180, 'X': 181, 'y': 182, 'Y': 183, 'ỳ': 184, 'Ỳ': 185, 'ý': 186, 'Ý': 187, 'ỷ': 188, 'Ỷ': 189, 'ỹ': 190, 'Ỹ': 191, 'ỵ': 192, 'Ỵ': 193, 'z': 194, 'Z': 195}
    def __init__(self, t=''):
        self.t = t
        self.untoned = remove_tones(t)
    def __repr__(self):
        return "<visort_key #{} '{}' ('{}')>".format(id(self), self.t, self.untoned)
    def __lt__(self, other):
        len_st, len_ot = len(self.t), len(other.t)
        d = visorted_key.order_dict
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

def remove_tones(t):
    tletters_dict = {'a': 'a', 'à': 'a', 'á': 'a', 'ả': 'a', 'ã': 'a', 'ạ': 'a', 'ă': 'ă', 'ằ': 'ă', 'ắ': 'ă', 'ẳ': 'ă', 'ẵ': 'ă', 'ặ': 'ă', 'â': 'â', 'ầ': 'â', 'ấ': 'â', 'ẩ': 'â', 'ẫ': 'â', 'ậ': 'â', 'e': 'e', 'è': 'e', 'é': 'e', 'ẻ': 'e', 'ẽ': 'e', 'ẹ': 'e', 'ê': 'ê', 'ề': 'ê', 'ế': 'ê', 'ể': 'ê', 'ễ': 'ê', 'ệ': 'ê', 'i': 'i', 'ì': 'i', 'í': 'i', 'ỉ': 'i', 'ĩ': 'i', 'ị': 'i', 'o': 'o', 'ò': 'o', 'ó': 'o', 'ỏ': 'o', 'õ': 'o', 'ọ': 'o', 'ô': 'ô', 'ồ': 'ô', 'ố': 'ô', 'ổ': 'ô', 'ỗ': 'ô', 'ộ': 'ô', 'ơ': 'ơ', 'ờ': 'ơ', 'ớ': 'ơ', 'ở': 'ơ', 'ỡ': 'ơ', 'ợ': 'ơ', 'u': 'u', 'ù': 'u', 'ú': 'u', 'ủ': 'u', 'ũ': 'u', 'ụ': 'u', 'ư': 'ư', 'ừ': 'ư', 'ứ': 'ư', 'ử': 'ư', 'ữ': 'ư', 'ự': 'ư', 'y': 'y', 'ỳ': 'y', 'ý': 'y', 'ỷ': 'y', 'ỹ': 'y', 'ỵ': 'y', 'A': 'A', 'À': 'A', 'Á': 'A', 'Ả': 'A', 'Ã': 'A', 'Ạ': 'A', 'Ă': 'Ă', 'Ằ': 'Ă', 'Ắ': 'Ă', 'Ẳ': 'Ă', 'Ẵ': 'Ă', 'Ặ': 'Ă', 'Â': 'Â', 'Ầ': 'Â', 'Ấ': 'Â', 'Ẩ': 'Â', 'Ẫ': 'Â', 'Ậ': 'Â', 'E': 'E', 'È': 'E', 'É': 'E', 'Ẻ': 'E', 'Ẽ': 'E', 'Ẹ': 'E', 'Ê': 'Ê', 'Ề': 'Ê', 'Ế': 'Ê', 'Ể': 'Ê', 'Ễ': 'Ê', 'Ệ': 'Ê', 'I': 'I', 'Ì': 'I', 'Í': 'I', 'Ỉ': 'I', 'Ĩ': 'I', 'Ị': 'I', 'O': 'O', 'Ò': 'O', 'Ó': 'O', 'Ỏ': 'O', 'Õ': 'O', 'Ọ': 'O', 'Ô': 'Ô', 'Ồ': 'Ô', 'Ố': 'Ô', 'Ổ': 'Ô', 'Ỗ': 'Ô', 'Ộ': 'Ô', 'Ơ': 'Ơ', 'Ờ': 'Ơ', 'Ớ': 'Ơ', 'Ở': 'Ơ', 'Ỡ': 'Ơ', 'Ợ': 'Ơ', 'U': 'U', 'Ù': 'U', 'Ú': 'U', 'Ủ': 'U', 'Ũ': 'U', 'Ụ': 'U', 'Ư': 'Ư', 'Ừ': 'Ư', 'Ứ': 'Ư', 'Ử': 'Ư', 'Ữ': 'Ư', 'Ự': 'Ư', 'Y': 'Y', 'Ỳ': 'Y', 'Ý': 'Y', 'Ỷ': 'Y', 'Ỹ': 'Y', 'Ỵ': 'Y', b'\xcc\x81'.decode() : '', b'\xcc\x80'.decode() : '', b'\xcc\x89'.decode() : '', b'\xcc\x83'.decode() : '', b'\xcc\xa3'.decode() : ''}
    r = ''    
    for c in t:
            r += tletters_dict.get(c, c)
    return r


from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

with PyCallGraph(output=GraphvizOutput()):
    t = "Cộng hòa Xã hội chủ nghĩa Việt Nam"
    print(noilais(t))
   