# -*- coding: utf-8 -*-

from .misc import normalize, separate_tone

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

class Syllable:
    initials = ('b', 'ch', 'c', 'd', 'đ', 'gh', 'gi', 'g', 'h', 'kh', 'k', 'l', 'm', 'ngh', 'ng', 'nh', 'ng',
    'n', 'ph', 'p', 'q', 'r', 's', 'th', 'tr', 't', 'v', 'x', '')
    vowels = ('a', 'ă', 'â', 'e', 'ê', 'i', 'o', 'ô', 'ơ', 'u', 'ư', 'y')
    diphthongs = ('ai', 'ao', 'au', 'ay', 'âu', 'ây', 'eo', 'êu', 'ia', 'iê', 'iu', 'oa', 'oe', 'oi',
    'oo', 'ôi', 'ơi', 'ua', 'uâ', 'ue', 'uê', 'ui', 'uô', 'uơ', 'uy', 'ưa', 'ưi', 'ươ', 'ưu', 'yê')
    triphthongs = ('iêu', 'oai', 'oay', 'uay', 'uây', 'uôi', 'uya', 'ươi', 'ươu', 'yêu')
    special_triphthongs = ('uyê',)
    phthongs = special_triphthongs + triphthongs + diphthongs + vowels
    finals = ('ch', 'c', 'm', 'ng', 'nh', 'n', 'p', 't', '')
    tones = ('', '\\', '/', '?', '~', '.')
    tone_names = ('', 'GRAVE', 'ACUTE', 'HOOK ABOVE', 'TILDE', 'DOT BELOW')
    
    strict_mode = False

    
    def __init__(self, initial, phthong, final, tone=''):
        self.initial = initial
        self.phthong = phthong
        self.final = final
        self.tone = tone
   		
    def __repr__(self):
       return "Syllable({}, {}, {}, {})".format(self.initial, self.phthong, self.final, self.tone)
       
    def __str__(self):
       return self.toString()
       
    def __bool__(self):
        return True
    
    @classmethod
    def fromString(cls, string):
        string = normalize(string).lower()
        if ' ' in string: return
        syll = string
    
        initial = phthong = final = tone = ''
    
        for item in cls.initials:
            if string.startswith(item):
                initial = item
                string = string[len(item):]
                break
        
        string, tone = separate_tone(string)
        
        for item in cls.phthongs:
            if string.startswith(item):
                phthong = item
                string = string[len(item):]
                break
        else:
            raise Exception(f"Invaild syllable: {syll}")
        
        for item in cls.finals:
            if string.startswith(item):
                final = item
                string = string[len(item):]
                break
                
        if string != '':
            raise Exception(f"Unexpected characters '{string}' after a syllable")
                
        return Syllable(initial, phthong, final, tone)
       
    def toString(self, old = False):
        initial = self.initial
        phthong = self.phthong
        final = self.final
        tone = self.tone
        
        high_priorites = ('ê', 'ơ')
        phth_list = list(phthong)

        def new_rule(phthong):
            if len(phthong) == 1:
                phth_list[0] = merge_tone(phthong, tone)
            elif len(phthong) == 2:
                if phthong == 'ua':
                    if initial == 'q':
                        phth_list[1] = merge_tone(phth_list[1], tone)
                    else:
                        phth_list[0] = merge_tone(phth_list[0], tone)
                elif phthong.startswith(('u', 'o')) \
                or phth_list[1] in {'â', 'ê', 'ô', 'ơ', 'ư'}:
                    phth_list[1] = merge_tone(phth_list[1], tone)
                else:
                    phth_list[0] = merge_tone(phth_list[0], tone)
            elif len(phthong) == 3:
                if phthong in self.special_triphthongs:
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
                    if final == '':
                        phth_list[0] = merge_tone(phth_list[0], tone)
                    else:
                        phth_list[1] = merge_tone(phth_list[1], tone)
                elif len(phthong) == 3:
                    phth_list[1] = merge_tone(phth_list[1], tone)
            return ''.join(phth_list)
    
        merge_func = old_rule if old else new_rule
        return ''.join((initial, merge_func(phthong), final))

    @property
    def initial(self):
        return self._initial

    @initial.setter
    def initial(self, value):
        value = value.lower()
        original = value
        if hasattr(self, "_initial"):
            if value == self.initial: return
        if value in self.initials:
            if hasattr(self, "_phthong"):
                if value in {'ng', 'ngh'}:
                    value = 'ngh' if (self.phthong[0] in {'e', 'ê', 'i'}) else 'ng'
                elif value in {'c', 'k'}:
                    value = 'k' if (self.phthong[0] in {'e', 'ê', 'i', 'y'}) else 'c'
                elif value == 'q':
                    phthongChars = list(self.phthong)
                    print( phthongChars )
                    if phthongChars[0] != 'u':
                        phthongChars[0] = 'u'
                        self.phthong = ''.join(phthongChars)
            if self.strict_mode and (value != original):
                raise ValueError(f"Invaild initial consonant: {original}")
            else:
                self._initial = value
        else:
            raise ValueError("Invaild initial consonant: {}".format(value))
    
    @property
    def phthong(self):
         return self._phthong
        
    @phthong.setter
    def phthong(self, value):
        value = value.lower()
        original = value
        original_initial = self.initial
        if value in self.phthongs:
            if hasattr(self, "_initial"):
                if self.initial in {'ng', 'ngh'}:
                    self.initial = 'ngh' if (value[0] in {'e', 'ê', 'i'}) else 'ng'
                elif self.initial in {'c', 'k', 'q'}:
                    if value[0] in {'e', 'ê', 'i', 'y'}:
                         self.initial = 'k'
                    elif value[0] != 'u':
                         self.initial = 'c'
            if self.strict_mode and (self.initial != original_initial):
                raise ValueError(f"Invaild phthong: {original}")
            else:
                self._phthong = value
        else:
            raise ValueError("Invaild phthong: {}".format(value))

    @property
    def final(self):
         return self._final
        
    @final.setter
    def final(self, value):
        if value.lower() in self.finals:
            self._final = value
        else:
            raise ValueError("Invaild final consonant: ' {}".format(value))

    @property
    def tone(self):
         return self._tone
        
    @tone.setter
    def tone(self, value):
        if value in self.tones:
            if hasattr(self, "_final"):
                if (self.final in {'c', 'p', 't'}) and not (value in {'/', '.'}):
                    if self.strict_mode:
                        raise ValueError(f"Invaild tone: {value}")
                    elif value in {'', '\\', '?'}:
                        value = '.'
                    elif value == '~':
                        value = '/'
            self._tone = value
        else:
            raise ValueError("Invaild tone: {}".format(value))