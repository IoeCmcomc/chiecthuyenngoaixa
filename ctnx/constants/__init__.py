# -*- coding: utf-8 -*-

import re

ALPHABET = "aăâbcdđeêghiklmnoôơpqrstuưvxy"

TONES = ('', '\\', '/', '?', '~', '.')

TONE_NAMES = ('?', 'GRAVE', 'ACUTE', 'HOOK ABOVE', 'TILDE', 'DOT BELOW')

DEFAULT_TONE_ORDER = ('', '/', '\\', '?', '~', '.')

VOWEL_TONE_TO_CHAR = {
    'a': {'': 'a', '.': 'ạ', '/': 'á', '?': 'ả', '\\': 'à', '~': 'ã'},
    'e': {'': 'e', '.': 'ẹ', '/': 'é', '?': 'ẻ', '\\': 'è', '~': 'ẽ'},
    'i': {'': 'i', '.': 'ị', '/': 'í', '?': 'ỉ', '\\': 'ì', '~': 'ĩ'},
    'o': {'': 'o', '.': 'ọ', '/': 'ó', '?': 'ỏ', '\\': 'ò', '~': 'õ'},
    'u': {'': 'u', '.': 'ụ', '/': 'ú', '?': 'ủ', '\\': 'ù', '~': 'ũ'},
    'y': {'': 'y', '.': 'ỵ', '/': 'ý', '?': 'ỷ', '\\': 'ỳ', '~': 'ỹ'},
    'â': {'': 'â', '.': 'ậ', '/': 'ấ', '?': 'ẩ', '\\': 'ầ', '~': 'ẫ'},
    'ê': {'': 'ê', '.': 'ệ', '/': 'ế', '?': 'ể', '\\': 'ề', '~': 'ễ'},
    'ô': {'': 'ô', '.': 'ộ', '/': 'ố', '?': 'ổ', '\\': 'ồ', '~': 'ỗ'},
    'ă': {'': 'ă', '.': 'ặ', '/': 'ắ', '?': 'ẳ', '\\': 'ằ', '~': 'ẵ'},
    'ơ': {'': 'ơ', '.': 'ợ', '/': 'ớ', '?': 'ở', '\\': 'ờ', '~': 'ỡ'},
    'ư': {'': 'ư', '.': 'ự', '/': 'ứ', '?': 'ử', '\\': 'ừ', '~': 'ữ'}
}

CHAR_TO_TONE_AND_VOWEL = {char: (tone, vowel) for vowel, chars in VOWEL_TONE_TO_CHAR.items() for tone, char in chars.items()}

VIETNAMESE_CHARSET_REGEX = re.compile(
    r"[a-z àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệđìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵ]+", re.IGNORECASE)

NO_TONE_CHAR_TRANS = str.maketrans("àáảãạằắẳẵặầấẩẫậèéẻẽẹềếểễệìíỉĩịòóỏõọồốổỗộờớởỡợùúủũụừứửữựỳýỷỹỵÀÁẢÃẠẰẮẲẴẶẦẤẨẪẬÈÉẺẼẸỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌỒỐỔỖỘỜỚỞỠỢÙÚỦŨỤỪỨỬỮỰỲÝỶỸỴ",
                                   "aaaaaăăăăăâââââeeeeeêêêêêiiiiioooooôôôôôơơơơơuuuuuưưưưưyyyyyAAAAAĂĂĂĂĂÂÂÂÂÂEEEEEÊÊÊÊÊIIIIIOOOOOÔÔÔÔÔƠƠƠƠƠUUUUUƯƯƯƯƯYYYYY")

BASE_TONE_PLACEMENT_REPLACE_PAIRS = [
    ('òa', 'oà'), ('óa', 'oá'), ('ỏa', 'oả'), ('õa', 'oã'), ('ọa', 'oạ'),
    ('òe', 'oè'), ('óe', 'oé'), ('ỏe', 'oẻ'), ('õe', 'oẽ'), ('ọe', 'oẹ'),
    ('ùy', 'uỳ'), ('úy', 'uý'), ('ủy', 'uỷ'), ('ũy', 'uỹ'), ('ụy', 'uỵ'),
    ('òo', 'oò'), ('óo', 'oó'), ('ỏo', 'oỏ'), ('õo', 'oõ'), ('ọo', 'oọ'),
    ('ồô', 'ôồ'), ('ốô', 'ôố'), ('ổô', 'ôổ'), ('ỗô', 'ôỗ'), ('ộô', 'ôộ'), 
]

# Rimes without tones 
ALL_RIMES = [
    "a", "ac", "ach", "ai", "am", "an", "ang", "anh", "ao", "ap", "at", "au", "ay",
    "oa", "oac", "oach", "oai", "oam", "oan", "oang", "oanh", "oao", "oap", "oat", "oau", "oay",
    "ăc", "ăm", "ăn", "ăng", "ăp", "ăt",
    "oăc", "oăm", "oăn", "oăng", "oăp", "oăt",
    "âc", "âm", "ân", "âng", "âp", "ât", "âu", "ây",
    "uâc", "uâm", "uân", "uâng", "uâp", "uât", "uây",
    "e", "ec", "em", "en", "eng", "eo", "ep", "et",
    "oe", "oec", "oem", "oen", "oeng", "oeo", "oep", "oet",
    "ê", "êch", "êm", "ên", "ênh", "êp", "êt", "êu",
    "uê", "uêch", "uêm", "uên", "uênh", "uêp", "uêt", "uêu",
    "i", "ia", "ich", "im", "in", "inh", "ip", "it", "iu", "y",
    "uy", "uya", "uych", "uym", "uyn", "uynh", "uyp", "uyt", "uyu",
    "iêc", "iêm", "iên", "iêng", "iêp", "iêt", "iêu", "yêm", "yên", "yêng", "yêt", "yêu",
    "uyêc", "uyêm", "uyên", "uyêng", "uyêp", "uyêt", "uyêu",
    "o", "oc", "oi", "om", "on", "ong", "op", "ot",
    "oong", "ooc",
    "ô", "ôc", "ôm", "ôn", "ông", "ôp", "ôt", "ôi",
    "ôông", "ôôc",
    "ơ", "ơi", "ơm", "ơn", "ơp", "ơt",
    "uơ", "uơi", "uơm", "uơn", "uơp", "uơt",
    "u", "uc", "ui", "um", "un", "ung", "up", "ut",
    "ua",
    "uôc", "uôi", "uôm", "uôn", "uông", "uôp", "uôt",
    "ư", "ưc", "ưi", "ưm", "ưn", "ưng", "ưp", "ưt", "ưu",
    "ưa",
    "ươc", "ươi", "ươm", "ươn", "ương", "ươp", "ươt", "ươu",
    # ví dụ: ngoao ngoao, nhoẻn miệng, quạu, quơ quào, dầu luyn, ngoem ngoém, ngoằn ngoèo,
    # lở loét, loằng ngoằng, xập xoèng, xoèng xoèng, hoặc, oái oăm, xoăn, co quắp,
    # thoăn thoắt, 
]

NON_WORD_CHARS_REGEX = re.compile(r"[^\w ]+", re.UNICODE)