# -*- coding: utf-8 -*-

from .constants import CHAR_ORDER_DICT
from .misc import remove_tones

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