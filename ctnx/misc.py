# -*- coding: utf-8 -*-

import unicodedata

def normalize(text: str) -> str:
    return unicodedata.normalize('NFC', text)

def remove_tones(t):
    tletters_dict = {'a': 'a', 'à': 'a', 'á': 'a', 'ả': 'a', 'ã': 'a', 'ạ': 'a', 'ă': 'ă', 'ằ': 'ă', 'ắ': 'ă', 'ẳ': 'ă', 'ẵ': 'ă', 'ặ': 'ă', 'â': 'â', 'ầ': 'â', 'ấ': 'â', 'ẩ': 'â', 'ẫ': 'â', 'ậ': 'â', 'e': 'e', 'è': 'e', 'é': 'e', 'ẻ': 'e', 'ẽ': 'e', 'ẹ': 'e', 'ê': 'ê', 'ề': 'ê', 'ế': 'ê', 'ể': 'ê', 'ễ': 'ê', 'ệ': 'ê', 'i': 'i', 'ì': 'i', 'í': 'i', 'ỉ': 'i', 'ĩ': 'i', 'ị': 'i', 'o': 'o', 'ò': 'o', 'ó': 'o', 'ỏ': 'o', 'õ': 'o', 'ọ': 'o', 'ô': 'ô', 'ồ': 'ô', 'ố': 'ô', 'ổ': 'ô', 'ỗ': 'ô', 'ộ': 'ô', 'ơ': 'ơ', 'ờ': 'ơ', 'ớ': 'ơ', 'ở': 'ơ', 'ỡ': 'ơ', 'ợ': 'ơ', 'u': 'u', 'ù': 'u', 'ú': 'u', 'ủ': 'u', 'ũ': 'u', 'ụ': 'u', 'ư': 'ư', 'ừ': 'ư', 'ứ': 'ư', 'ử': 'ư', 'ữ': 'ư', 'ự': 'ư', 'y': 'y', 'ỳ': 'y', 'ý': 'y', 'ỷ': 'y', 'ỹ': 'y', 'ỵ': 'y', 'A': 'A', 'À': 'A', 'Á': 'A', 'Ả': 'A', 'Ã': 'A', 'Ạ': 'A', 'Ă': 'Ă', 'Ằ': 'Ă', 'Ắ': 'Ă', 'Ẳ': 'Ă', 'Ẵ': 'Ă', 'Ặ': 'Ă', 'Â': 'Â', 'Ầ': 'Â', 'Ấ': 'Â', 'Ẩ': 'Â', 'Ẫ': 'Â', 'Ậ': 'Â', 'E': 'E', 'È': 'E', 'É': 'E', 'Ẻ': 'E', 'Ẽ': 'E', 'Ẹ': 'E', 'Ê': 'Ê', 'Ề': 'Ê', 'Ế': 'Ê', 'Ể': 'Ê', 'Ễ': 'Ê', 'Ệ': 'Ê', 'I': 'I', 'Ì': 'I', 'Í': 'I', 'Ỉ': 'I', 'Ĩ': 'I', 'Ị': 'I', 'O': 'O', 'Ò': 'O', 'Ó': 'O', 'Ỏ': 'O', 'Õ': 'O', 'Ọ': 'O', 'Ô': 'Ô', 'Ồ': 'Ô', 'Ố': 'Ô', 'Ổ': 'Ô', 'Ỗ': 'Ô', 'Ộ': 'Ô', 'Ơ': 'Ơ', 'Ờ': 'Ơ', 'Ớ': 'Ơ', 'Ở': 'Ơ', 'Ỡ': 'Ơ', 'Ợ': 'Ơ', 'U': 'U', 'Ù': 'U', 'Ú': 'U', 'Ủ': 'U', 'Ũ': 'U', 'Ụ': 'U', 'Ư': 'Ư', 'Ừ': 'Ư', 'Ứ': 'Ư', 'Ử': 'Ư', 'Ữ': 'Ư', 'Ự': 'Ư', 'Y': 'Y', 'Ỳ': 'Y', 'Ý': 'Y', 'Ỷ': 'Y', 'Ỹ': 'Y', 'Ỵ': 'Y', b'\xcc\x81'.decode() : '', b'\xcc\x80'.decode() : '', b'\xcc\x89'.decode() : '', b'\xcc\x83'.decode() : '', b'\xcc\xa3'.decode() : ''}
    r = ''    
    for c in t:
            r += tletters_dict.get(c, c)
    return r

def deaccent(t):
    r = t.replace('Đ', 'D').replace('đ', 'd')
    r = unicodedata.normalize('NFKD', r).encode('ascii', 'ignore').decode()
    return r

def separate_tone(t, id=False, all=False):
    tones = ('', '\\', '/', '?', '~', '.')
    tone_names = ('(Placeholder)', 'GRAVE', 'ACUTE', 'HOOK ABOVE', 'TILDE', 'DOT BELOW')
    t = unicodedata.normalize('NFC', t)
    tone = ''

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