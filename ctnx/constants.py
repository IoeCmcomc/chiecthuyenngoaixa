# -*- coding: utf-8 -*-

import re

TONES = ('', '\\', '/', '?', '~', '.')

TONE_NAMES = ('?', 'GRAVE', 'ACUTE', 'HOOK ABOVE', 'TILDE', 'DOT BELOW')

CHAR_ORDER_DICT = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'a': 10, 'A': 11, 'à': 12, 'À': 13, 'á': 14, 'Á': 15, 'ả': 16, 'Ả': 17, 'ã': 18, 'Ã': 19, 'ạ': 20, 'Ạ': 21, 'ă': 22, 'Ă': 23, 'ằ': 24, 'Ằ': 25, 'ắ': 26, 'Ắ': 27, 'ẳ': 28, 'Ẳ': 29, 'ẵ': 30, 'Ẵ': 31, 'ặ': 32, 'Ặ': 33, 'â': 34, 'Â': 35, 'ầ': 36, 'Ầ': 37, 'ẩ': 38, 'Ẩ': 39, 'ẫ': 40, 'Ẫ': 41, 'ấ': 42, 'Ấ': 43, 'ậ': 44, 'Ậ': 45, 'b': 46, 'B': 47, 'c': 48, 'C': 49, 'd': 50, 'D': 51, 'đ': 52, 'Đ': 53, 'e': 54, 'E': 55, 'è': 56, 'È': 57, 'é': 58, 'É': 59, 'ẻ': 60, 'Ẻ': 61, 'ẽ': 62, 'Ẽ': 63, 'ẹ': 64, 'Ẹ': 65, 'ê': 66, 'Ê': 67, 'ề': 68, 'Ề': 69, 'ế': 70, 'Ế': 71, 'ể': 72, 'Ể': 73, 'ễ': 74, 'Ễ': 75, 'ệ': 76, 'Ệ': 77, 'f': 78, 'F': 79, 'g': 80, 'G': 81, 'h': 82, 'H': 83, 'i': 84, 'I': 85, 'ì': 86, 'Ì': 87, 'í': 88, 'Í': 89, 'ỉ': 90, 'Ỉ': 91, 'ĩ': 92, 'Ĩ': 93, 'ị': 94, 'Ị': 95, 'j': 96, 'J': 97, 'k': 98, 'K': 99, 'l': 100, 'L': 101, 'm': 102,
                   'M': 103, 'n': 104, 'N': 105, 'o': 106, 'O': 107, 'ò': 108, 'Ò': 109, 'ó': 110, 'Ó': 111, 'ỏ': 112, 'Ỏ': 113, 'õ': 114, 'Õ': 115, 'ọ': 116, 'Ọ': 117, 'ô': 118, 'Ô': 119, 'ồ': 120, 'Ồ': 121, 'ố': 122, 'Ố': 123, 'ổ': 124, 'Ổ': 125, 'ỗ': 126, 'Ỗ': 127, 'ộ': 128, 'Ộ': 129, 'ơ': 130, 'Ơ': 131, 'ờ': 132, 'Ờ': 133, 'ớ': 134, 'Ớ': 135, 'ở': 136, 'Ở': 137, 'ỡ': 138, 'Ỡ': 139, 'ợ': 140, 'Ợ': 141, 'p': 142, 'P': 143, 'q': 144, 'Q': 145, 'r': 146, 'R': 147, 's': 148, 'S': 149, 't': 150, 'T': 151, 'u': 152, 'U': 153, 'ù': 154, 'Ù': 155, 'ú': 156, 'Ú': 157, 'ủ': 158, 'Ủ': 159, 'ũ': 160, 'Ũ': 161, 'ụ': 162, 'Ụ': 163, 'ư': 164, 'Ư': 165, 'ừ': 166, 'Ừ': 167, 'ứ': 168, 'Ứ': 169, 'ử': 170, 'Ử': 171, 'ữ': 172, 'Ữ': 173, 'ự': 174, 'Ự': 175, 'v': 176, 'V': 177, 'w': 178, 'W': 179, 'x': 180, 'X': 181, 'y': 182, 'Y': 183, 'ỳ': 184, 'Ỳ': 185, 'ý': 186, 'Ý': 187, 'ỷ': 188, 'Ỷ': 189, 'ỹ': 190, 'Ỹ': 191, 'ỵ': 192, 'Ỵ': 193, 'z': 194, 'Z': 195}

CHAR_ORDER_STRING = r"0123456789aAàÀáÁảẢãÃạẠăĂằẰắẮẳẲẵẴặẶâÂầẦẩẨẫẪấẤậẬbBcCdDđĐeEèÈéÉẻẺẽẼẹẸêÊềỀếẾểỂễỄệỆfFgGhHiIìÌíÍỉỈĩĨịỊjJkKlLmMnNoOòÒóÓỏỎõÕọỌôÔồỒốỐổỔỗỖộỘơƠờỜớỚởỞỡỠợỢpPqQrRsStTuUùÙúÚủỦũŨụỤưƯừỪứỨửỬữỮựỰvVwWxXyYỳỲýÝỷỶỹỸỵỴzZ"

VIETNAMESE_CHARSET_REGEX = re.compile(
    r"[a-z àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệđìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵ]+", re.IGNORECASE)

NO_TONE_CHAR_TRANS = str.maketrans("àáảãạằắẳẵặầấẩẫậèéẻẽẹềếểễệìíỉĩịòóỏõọồốổỗộờớởỡợùúủũụừứửữựỳýỷỹỵÀÁẢÃẠẰẮẲẴẶẦẤẨẪẬÈÉẺẼẸỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌỒỐỔỖỘỜỚỞỠỢÙÚỦŨỤỪỨỬỮỰỲÝỶỸỴ",
                                   "aaaaaăăăăăâââââeeeeeêêêêêiiiiioooooôôôôôơơơơơuuuuuưưưưưyyyyyAAAAAĂĂĂĂĂÂÂÂÂÂEEEEEÊÊÊÊÊIIIIIOOOOOÔÔÔÔÔƠƠƠƠƠUUUUUƯƯƯƯƯYYYYY")

# The following confusable characters are extracted and modified 
# from a subset of Unicode 15.1 confusables:
# https://www.unicode.org/Public/security/15.1.0/confusables.txt
CONFUSABLES_OLD = {
    '՝': "'",
    '＇': "'",
    '‘': "'",
    '’': "'",
    '‛': "'",
    '′': "'",
    '‵': "'",
    '՚': "'",
    '`': "'",
    '`': "'",
    '｀': "'",
    '´': "'",
    '΄': "'",
    '´': "'",
    '᾽': "'",
    '᾿': "'",
    '῾': "'",
    'ʹ': "'",
    'ʹ': "'",
    'ˈ': "'",
    'ˊ': "'",
    'ˋ': "'",
    '˴': "'",
    'ʻ': "'",
    'ʽ': "'",
    'ʼ': "'",
    'ʾ': "'",
    'ꞌ': "'",
    'ᑊ': "'",
    'ᛌ': "'",
    '﹍': '_',
    '﹎': '_',
    '﹏': '_',
    'Ꝛ': '2',
    'Ƨ': '2',
    'Ϩ': '2',
    'Ꙅ': '2',
    'ᒿ': '2',
    'ꛯ': '2',
    'Ɜ': '3',
    'Ȝ': '3',
    'Ʒ': '3',
    'Ꝫ': '3',
    'Ⳍ': '3',
    'З': '3',
    'Ӡ': '3',
    'Ꮞ': '4',
    'Ƽ': '5',
    'Ⳓ': '6',
    'б': '6',
    'Ꮾ': '6',
    'ଃ': '8',
    '৪': '8',
    '੪': '8',
    'ȣ': '8',
    'Ȣ': '8',
    '੧': '9',
    '୨': '9',
    '৭': '9',
    '൭': '9',
    'Ꝯ': '9',
    'Ⳋ': '9',
    '⍺': 'a',
    'ａ': 'a',
    'ɑ': 'a',
    'α': 'a',
    'а': 'a',
    'Ａ': 'A',
    'Α': 'A',
    'А': 'A',
    'Ꭺ': 'A',
    'ᗅ': 'A',
    'ꓮ': 'A',
    'Ƅ': 'b',
    'Ь': 'b',
    'Ꮟ': 'b',
    'ᑲ': 'b',
    'ᖯ': 'b',
    'Ｂ': 'B',
    'ℬ': 'B',
    'Ꞵ': 'B',
    'Β': 'B',
    'В': 'B',
    'Ᏼ': 'B',
    'ᗷ': 'B',
    'ꓐ': 'B',
    'ｃ': 'c',
    'ⅽ': 'c',
    'ᴄ': 'c',
    'ϲ': 'c',
    'ⲥ': 'c',
    'с': 'c',
    'ꮯ': 'c',
    'Ｃ': 'C',
    'Ⅽ': 'C',
    'ℂ': 'C',
    'ℭ': 'C',
    'Ϲ': 'C',
    'Ⲥ': 'C',
    'С': 'C',
    'Ꮯ': 'C',
    'ꓚ': 'C',
    'ⅾ': 'd',
    'ⅆ': 'd',
    'ԁ': 'd',
    'Ꮷ': 'd',
    'ᑯ': 'd',
    'ꓒ': 'd',
    'Ⅾ': 'D',
    'ⅅ': 'D',
    'Ꭰ': 'D',
    'ᗞ': 'D',
    'ᗪ': 'D',
    'ꓓ': 'D',
    '℮': 'e',
    'ｅ': 'e',
    'ℯ': 'e',
    'ⅇ': 'e',
    'ꬲ': 'e',
    'е': 'e',
    'ҽ': 'e',
    '⋿': 'E',
    'Ｅ': 'E',
    'ℰ': 'E',
    'Ε': 'E',
    'Е': 'E',
    'ⴹ': 'E',
    'Ꭼ': 'E',
    'ꓰ': 'E',
    'ꬵ': 'f',
    'ꞙ': 'f',
    'ſ': 'f',
    'ẝ': 'f',
    'ք': 'f',
    'ℱ': 'F',
    'Ꞙ': 'F',
    'Ϝ': 'F',
    'ᖴ': 'F',
    'ꓝ': 'F',
    'ｇ': 'g',
    'ℊ': 'g',
    'ɡ': 'g',
    'ᶃ': 'g',
    'ƍ': 'g',
    'ց': 'g',
    'Ԍ': 'G',
    'Ꮐ': 'G',
    'Ᏻ': 'G',
    'ꓖ': 'G',
    'ｈ': 'h',
    'ℎ': 'h',
    'һ': 'h',
    'հ': 'h',
    'Ꮒ': 'h',
    'Ｈ': 'H',
    'ℋ': 'H',
    'ℌ': 'H',
    'ℍ': 'H',
    'Η': 'H',
    'Ⲏ': 'H',
    'Н': 'H',
    'Ꮋ': 'H',
    'ᕼ': 'H',
    'ꓧ': 'H',
    '˛': 'i',
    '⍳': 'i',
    'ｉ': 'i',
    'ⅰ': 'i',
    'ℹ': 'i',
    'ⅈ': 'i',
    'ı': 'i',
    'ɪ': 'i',
    'ɩ': 'i',
    'ι': 'i',
    'ι': 'i',
    'ͺ': 'i',
    'і': 'i',
    'ꙇ': 'i',
    'ӏ': 'i',
    'ꭵ': 'i',
    'Ꭵ': 'i',
    'ｊ': 'j',
    'ⅉ': 'j',
    'ϳ': 'j',
    'ј': 'j',
    'Ｊ': 'J',
    'Ʝ': 'J',
    'Ϳ': 'J',
    'Ј': 'J',
    'Ꭻ': 'J',
    'ᒍ': 'J',
    'ꓙ': 'J',
    'K': 'K',
    'Ｋ': 'K',
    'Κ': 'K',
    'Ⲕ': 'K',
    'К': 'K',
    'Ꮶ': 'K',
    'ᛕ': 'K',
    'ꓗ': 'K',
    '|': 'l',
    '∣': 'l',
    '⏽': 'l',
    '￨': 'l',
    '۱': 'l',
    'I': 'l',
    'Ｉ': 'l',
    'Ⅰ': 'l',
    'ℐ': 'l',
    'ℑ': 'l',
    'Ɩ': 'l',
    'ｌ': 'l',
    'ⅼ': 'l',
    'ℓ': 'l',
    'ǀ': 'l',
    'Ι': 'l',
    'Ⲓ': 'l',
    'І': 'l',
    'Ӏ': 'l',
    'ⵏ': 'l',
    'ᛁ': 'l',
    'ꓲ': 'l',
    'Ⅼ': 'L',
    'ℒ': 'L',
    'Ⳑ': 'L',
    'Ꮮ': 'L',
    'ᒪ': 'L',
    'ꓡ': 'L',
    'Ｍ': 'M',
    'Ⅿ': 'M',
    'ℳ': 'M',
    'Μ': 'M',
    'Ϻ': 'M',
    'Ⲙ': 'M',
    'М': 'M',
    'Ꮇ': 'M',
    'ᗰ': 'M',
    'ᛖ': 'M',
    'ꓟ': 'M',
    'ո': 'n',
    'ռ': 'n',
    'Ｎ': 'N',
    'ℕ': 'N',
    'Ν': 'N',
    'Ⲛ': 'N',
    'ꓠ': 'N',
    'ం': 'o',
    'ಂ': 'o',
    'ം': 'o',
    'ං': 'o',
    '०': 'o',
    '੦': 'o',
    '૦': 'o',
    '௦': 'o',
    '౦': 'o',
    '೦': 'o',
    '൦': 'o',
    '๐': 'o',
    '໐': 'o',
    '၀': 'o',
    '۵': 'o',
    'ｏ': 'o',
    'ℴ': 'o',
    'ᴏ': 'o',
    'ᴑ': 'o',
    'ꬽ': 'o',
    'ο': 'o',
    'σ': 'o',
    'ⲟ': 'o',
    'о': 'o',
    'ჿ': 'o',
    'օ': 'o',
    'ഠ': 'o',
    'ဝ': 'o',
#    '0': 'O',
    '০': 'O',
    '୦': 'O',
    '〇': 'O',
    'Ｏ': 'O',
    'Ο': 'O',
    'Ⲟ': 'O',
    'О': 'O',
    'Օ': 'O',
    'ⵔ': 'O',
    'ዐ': 'O',
    'ଠ': 'O',
    'ꓳ': 'O',
    '⍴': 'p',
    'ｐ': 'p',
    'ρ': 'p',
    'ϱ': 'p',
    'ⲣ': 'p',
    'р': 'p',
    'Ｐ': 'P',
    'ℙ': 'P',
    'Ρ': 'P',
    'Ⲣ': 'P',
    'Р': 'P',
    'Ꮲ': 'P',
    'ᑭ': 'P',
    'ꓑ': 'P',
    'ԛ': 'q',
    'գ': 'q',
    'զ': 'q',
    'ℚ': 'Q',
    'ⵕ': 'Q',
    'ꭇ': 'r',
    'ꭈ': 'r',
    'ᴦ': 'r',
    'ⲅ': 'r',
    'г': 'r',
    'ꮁ': 'r',
    'ℛ': 'R',
    'ℜ': 'R',
    'ℝ': 'R',
    'Ʀ': 'R',
    'Ꭱ': 'R',
    'Ꮢ': 'R',
    'ᖇ': 'R',
    'ꓣ': 'R',
    'ｓ': 's',
    'ꜱ': 's',
    'ƽ': 's',
    'ѕ': 's',
    'ꮪ': 's',
    'Ｓ': 'S',
    'Ѕ': 'S',
    'Տ': 'S',
    'Ꮥ': 'S',
    'Ꮪ': 'S',
    'ꓢ': 'S',
    '⊤': 'T',
    '⟙': 'T',
    'Ｔ': 'T',
    'Τ': 'T',
    'Ⲧ': 'T',
    'Т': 'T',
    'Ꭲ': 'T',
    'ꓔ': 'T',
    'ꞟ': 'u',
    'ᴜ': 'u',
    'ꭎ': 'u',
    'ꭒ': 'u',
    'ʋ': 'u',
    'υ': 'u',
    'ս': 'u',
    '∪': 'U',
    '⋃': 'U',
    'Ս': 'U',
    'ሀ': 'U',
    'ᑌ': 'U',
    'ꓴ': 'U',
    '∨': 'v',
    '⋁': 'v',
    'ｖ': 'v',
    'ⅴ': 'v',
    'ᴠ': 'v',
    'ν': 'v',
    'ѵ': 'v',
    'ꮩ': 'v',
    '۷': 'V',
    'Ⅴ': 'V',
    'Ѵ': 'V',
    'ⴸ': 'V',
    'Ꮩ': 'V',
    'ᐯ': 'V',
    'ꛟ': 'V',
    'ꓦ': 'V',
    'ɯ': 'w',
    'ᴡ': 'w',
    'ѡ': 'w',
    'ԝ': 'w',
    'ա': 'w',
    'ꮃ': 'w',
    'Ԝ': 'W',
    'Ꮃ': 'W',
    'Ꮤ': 'W',
    'ꓪ': 'W',
    '᙮': 'x',
    '×': 'x',
    '⤫': 'x',
    '⤬': 'x',
    '⨯': 'x',
    'ｘ': 'x',
    'ⅹ': 'x',
    'х': 'x',
    'ᕁ': 'x',
    'ᕽ': 'x',
    '᙭': 'X',
    '╳': 'X',
    'Ｘ': 'X',
    'Ⅹ': 'X',
    'Ꭓ': 'X',
    'Χ': 'X',
    'Ⲭ': 'X',
    'Х': 'X',
    'ⵝ': 'X',
    'ᚷ': 'X',
    'ꓫ': 'X',
    'ɣ': 'y',
    'ᶌ': 'y',
    'ｙ': 'y',
    'ʏ': 'y',
    'ỿ': 'y',
    'ꭚ': 'y',
    'γ': 'y',
    'ℽ': 'y',
    'у': 'y',
    'ү': 'y',
    'ყ': 'y',
    'Ｙ': 'Y',
    'Υ': 'Y',
    'ϒ': 'Y',
    'Ⲩ': 'Y',
    'У': 'Y',
    'Ү': 'Y',
    'Ꭹ': 'Y',
    'Ꮍ': 'Y',
    'ꓬ': 'Y',
    'ᴢ': 'z',
    'ꮓ': 'z',
    'Ｚ': 'Z',
    'ℤ': 'Z',
    'ℨ': 'Z',
    'Ζ': 'Z',
    'Ꮓ': 'Z',
    'ꓜ': 'Z',
}

CONFUSABLES = {
    ' ': " ",
    ' ': " ",
    ' ': " ",
    ' ': " ",
    ' ': " ",
    ' ': " ",
    ' ': " ",
    ' ': " ",
    ' ': " ",
    ' ': " ",
    ' ': " ",
    ' ': " ",
    ' ': " ",
    ' ': " ",
    ' ': " ",
    '﹍': "_",
    '﹎': "_",
    '﹏': "_",
    '‐': "-",
    '‑': "-",
    '‒': "-",
    '–': "-",
    '﹘': "-",
    '⁃': "-",
    '˗': "-",
    '−': "-",
    '➖': "-",
    'Ⲻ': "-",
    '～': "〜",
    '‚': ",",
    '¸': ",",
    'ꓹ': ",",
    '⸲': "،",
    ';': ";",
    'ः': ":",
    'ઃ': ":",
    '：': ":",
    '։': ":",
    '᛬': ":",
    '︰': ":",
    '᠃': ":",
    '᠉': ":",
    '⁚': ":",
    '˸': ":",
    '꞉': ":",
    '∶': ":",
    'ː': ":",
    'ꓽ': ":",
    '！': "!",
    'ǃ': "!",
    'ⵑ': "!",
    'ʔ': "?",
    'Ɂ': "?",
    'ॽ': "?",
    'Ꭾ': "?",
    'ꛫ': "?",
    '𝅭': ".",
    '․': ".",
    '꘎': ".",
    '۰': ".",
    'ꓸ': ".",
    '・': "·",
    '･': "·",
    '᛫': "·",
    '·': "·",
    '⸱': "·",
    '𐄁': "·",
    '•': "·",
    '‧': "·",
    '∙': "·",
    '⋅': "·",
    'ꞏ': "·",
    'ᐧ': "·",
    '꠰': "।",
    '՝': "'",
    '＇': "'",
    '‘': "'",
    '’': "'",
    '‛': "'",
    '′': "'",
    '‵': "'",
    '՚': "'",
    '`': "'",
    '`': "'",
    '｀': "'",
    '´': "'",
    '΄': "'",
    '´': "'",
    '᾽': "'",
    '᾿': "'",
    '῾': "'",
    'ʹ': "'",
    'ʹ': "'",
    'ˈ': "'",
    'ˊ': "'",
    'ˋ': "'",
    '˴': "'",
    'ʻ': "'",
    'ʽ': "'",
    'ʼ': "'",
    'ʾ': "'",
    'ꞌ': "'",
    'ᑊ': "'",
    'ᛌ': "'",
    '𖽑': "'",
    '𖽒': "'",
    '［': "(",
    '❨': "(",
    '❲': "(",
    '〔': "(",
    '﴾': "(",
    '］': ")",
    '❩': ")",
    '❳': ")",
    '〕': ")",
    '﴿': ")",
    '❴': "{",
    '𝄔': "{",
    '❵': "}",
    '〚': "⟦",
    '〛': "⟧",
    '⟨': "❬",
    '〈': "❬",
    '〈': "❬",
    '㇛': "❬",
    'く': "❬",
    '𡿨': "❬",
    '⟩': "❭",
    '〉': "❭",
    '〉': "❭",
    '＾': "︿",
    '⸿': "¶",
    '⁎': "*",
    '∗': "*",
    '𐌟': "*",
    '᜵': "/",
    '⁁': "/",
    '∕': "/",
    '⁄': "/",
    '╱': "/",
    '⟋': "/",
    '⧸': "/",
    '𝈺': "/",
    '㇓': "/",
    '〳': "/",
    'Ⳇ': "/",
    'ノ': "/",
    '丿': "/",
    '⼃': "/",
    '＼': "\\",
    '﹨': "\\",
    '∖': "\\",
    '⟍': "\\",
    '⧵': "\\",
    '⧹': "\\",
    '𝈏': "\\",
    '𝈻': "\\",
    '㇔': "\\",
    '丶': "\\",
    '⼂': "\\",
    'ꝸ': "&",
    '૰': "॰",
    '𑂻': "॰",
    '𑇇': "॰",
    '⚬': "॰",
    '𑇛': "꣼",
    '៙': "๏",
    '៕': "๚",
    '៚': "๛",
    '༌': "་",
    '˄': "^",
    'ˆ': "^",
    '꙾': "ˇ",
    '˘': "ˇ",
    '‾': "ˉ",
    '﹉': "ˉ",
    '﹊': "ˉ",
    '﹋': "ˉ",
    '﹌': "ˉ",
    '¯': "ˉ",
    '￣': "ˉ",
    '▔': "ˉ",
    '͵': "ˏ",
    '˻': "˪",
    '꜖': "˪",
    '꜔': "˫",
    '。': "˳",
    '⸰': "°",
    '˚': "°",
    '∘': "°",
    '○': "°",
    '◦': "°",
    '௵': "௳",
    'Ⓒ': "©",
    'Ⓡ': "®",
    'Ⓟ': "℗",
    '𝈛': "⅄",
    '⯬': "↞",
    '⯭': "↟",
    '⯮': "↠",
    '⯯': "↡",
    '↵': "↲",
    '𝛛': "∂",
    '𝜕': "∂",
    '𝝏': "∂",
    '𝞉': "∂",
    '𝟃': "∂",
    '⌀': "∅",
    '𝛁': "∇",
    '𝛻': "∇",
    '𝜵': "∇",
    '𝝯': "∇",
    '𝞩': "∇",
    '𑢨': "∇",
    '█': "∎",
    '■': "∎",
    '⨿': "∐",
    '᛭': "+",
    '➕': "+",
    '𐊛': "+",
    '➗': "÷",
    '‹': "<",
    '❮': "<",
    '˂': "<",
    '𝈶': "<",
    'ᐸ': "<",
    'ᚲ': "<",
    '᐀': "=",
    '⹀': "=",
    '゠': "=",
    '꓿': "=",
    '›': ">",
    '❯': ">",
    '˃': ">",
    '𝈷': ">",
    'ᐳ': ">",
    '𖼿': ">",
    '⁓': "~",
    '˜': "~",
    '῀': "~",
    '∼': "~",
    '⋀': "∧",
    '⸫': "∴",
    '⸪': "∵",
    '⸬': "∷",
    '𑇞': "≈",
    '♎': "≏",
    '🝞': "≏",
    '≣': "≡",
    '⨃': "⊍",
    '⨄': "⊎",
    '𝈸': "⊏",
    '𝈹': "⊐",
    '⨅': "⊓",
    '⨆': "⊔",
    '⨂': "⊗",
    '⍟': "⊛",
    '🝱': "⊠",
    '🝕': "⊡",
    '◁': "⊲",
    '▷': "⊳",
    '︴': "⌇",
    '◠': "⌒",
    '⨽': "⌙",
    '⌥': "⌤",
    '⧇': "⌻",
    '◎': "⌾",
    '⦾': "⌾",
    '⧅': "⍂",
    '⦰': "⍉",
    '⏃': "⍋",
    '⏂': "⍎",
    '⏁': "⍕",
    '⏆': "⍭",
    '☸': "⎈",
    '︵': "⏜",
    '︶': "⏝",
    '︷': "⏞",
    '︸': "⏟",
    '︹': "⏠",
    '︺': "⏡",
    '▱': "⏥",
    '⏼': "⏻",
    '︱': "│",
    '｜': "│",
    '┃': "│",
    '┏': "┌",
    '┣': "├",
    '▐': "▌",
    '▗': "▖",
    '▝': "▘",
    '☐': "□",
    '￭': "▪",
    '▸': "▶",
    '►': "▶",
    '⳩': "☧",
    '🜊': "☩",
    '🌒': "☽",
    '🌙': "☽",
    '⏾': "☾",
    '🌘': "☾",
    '⧙': "⦚",
    '🜺': "⧟",
    '⨾': "⨟",
    '𐆠': "⳨",
    '⓪': "🄍",
    '↺': "🄎",
    '˙': "ॱ",
    'ൎ': "ॱ",
    '－': "ー",
    '—': "ー",
    '―': "ー",
    '─': "ー",
    '━': "ー",
    '㇐': "ー",
    'ꟷ': "ー",
    'ᅳ': "ー",
    'ㅡ': "ー",
    '一': "ー",
    '⼀': "ー",
    '₤': "£",
    '〒': "₸",
    '〶': "₸",
    '᭜': "᭐",
    '꧆': "꧐",
    '𑓑': "১",
    '೧': "౧",
    'ၥ': "၁",
    '①': "1",
    '⑩': "10",
    '𝟐': "2",
    '𝟚': "2",
    '𝟤': "2",
    '𝟮': "2",
    '𝟸': "2",
    '🯲': "2",
    'Ꝛ': "2",
    'Ƨ': "2",
    'Ϩ': "2",
    'Ꙅ': "2",
    'ᒿ': "2",
    'ꛯ': "2",
    '૨': "2",
    '𑓒': "2",
    '೨': "2",
    '②': "2",
    '𝈆': "3",
    '𝟑': "3",
    '𝟛': "3",
    '𝟥': "3",
    '𝟯': "3",
    '𝟹': "3",
    '🯳': "3",
    'Ɜ': "3",
    'Ȝ': "3",
    'Ʒ': "3",
    'Ꝫ': "3",
    'Ⳍ': "3",
    'З': "3",
    'Ӡ': "3",
    '𖼻': "3",
    '𑣊': "3",
    '૩': "3",
    '③': "3",
    '𝟒': "4",
    '𝟜': "4",
    '𝟦': "4",
    '𝟰': "4",
    '𝟺': "4",
    '🯴': "4",
    'Ꮞ': "4",
    '𑢯': "4",
    '④': "4",
    '𝟓': "5",
    '𝟝': "5",
    '𝟧': "5",
    '𝟱': "5",
    '𝟻': "5",
    '🯵': "5",
    'Ƽ': "5",
    '𑢻': "5",
    '⑤': "5",
    '𝟔': "6",
    '𝟞': "6",
    '𝟨': "6",
    '𝟲': "6",
    '𝟼': "6",
    '🯶': "6",
    'Ⳓ': "6",
    'б': "6",
    'Ꮾ': "6",
    '𑣕': "6",
    '⑥': "6",
    '𝈒': "7",
    '𝟕': "7",
    '𝟟': "7",
    '𝟩': "7",
    '𝟳': "7",
    '𝟽': "7",
    '🯷': "7",
    '𐓒': "7",
    '𑣆': "7",
    '⑦': "7",
    'ଃ': "8",
    '৪': "8",
    '੪': "8",
    '𝟖': "8",
    '𝟠': "8",
    '𝟪': "8",
    '𝟴': "8",
    '𝟾': "8",
    '🯸': "8",
    'ȣ': "8",
    'Ȣ': "8",
    '𐌚': "8",
    '⑧': "8",
    '੧': "9",
    '୨': "9",
    '৭': "9",
    '൭': "9",
    '𝟗': "9",
    '𝟡': "9",
    '𝟫': "9",
    '𝟵': "9",
    '𝟿': "9",
    '🯹': "9",
    'Ꝯ': "9",
    'Ⳋ': "9",
    '𑣌': "9",
    '𑢬': "9",
    '𑣖': "9",
    '⑨': "9",
    '⍺': "a",
    'ａ': "a",
    '𝐚': "a",
    '𝑎': "a",
    '𝒂': "a",
    '𝒶': "a",
    '𝓪': "a",
    '𝔞': "a",
    '𝕒': "a",
    '𝖆': "a",
    '𝖺': "a",
    '𝗮': "a",
    '𝘢': "a",
    '𝙖': "a",
    '𝚊': "a",
    'ɑ': "a",
    'α': "a",
    '𝛂': "a",
    '𝛼': "a",
    '𝜶': "a",
    '𝝰': "a",
    '𝞪': "a",
    'а': "a",
    'Ａ': "A",
    '𝐀': "A",
    '𝐴': "A",
    '𝑨': "A",
    '𝒜': "A",
    '𝓐': "A",
    '𝔄': "A",
    '𝔸': "A",
    '𝕬': "A",
    '𝖠': "A",
    '𝗔': "A",
    '𝘈': "A",
    '𝘼': "A",
    '𝙰': "A",
    'Α': "A",
    '𝚨': "A",
    '𝛢': "A",
    '𝜜': "A",
    '𝝖': "A",
    '𝞐': "A",
    'А': "A",
    'Ꭺ': "A",
    'ᗅ': "A",
    'ꓮ': "A",
    '𖽀': "A",
    '𐊠': "A",
    'ǎ': "ă",
    'Ǎ': "Ă",
    'ȧ': "a",
    'Ȧ': "A",
    'ẚ': "ả",
    'ꭺ': "A",
    '𝐛': "b",
    '𝑏': "b",
    '𝒃': "b",
    '𝒷': "b",
    '𝓫': "b",
    '𝔟': "b",
    '𝕓': "b",
    '𝖇': "b",
    '𝖻': "b",
    '𝗯': "b",
    '𝘣': "b",
    '𝙗': "b",
    '𝚋': "b",
    'Ƅ': "b",
    'Ь': "b",
    'Ꮟ': "b",
    'ᑲ': "b",
    'ᖯ': "b",
    'Ｂ': "B",
    'ℬ': "B",
    '𝐁': "B",
    '𝐵': "B",
    '𝑩': "B",
    '𝓑': "B",
    '𝔅': "B",
    '𝔹': "B",
    '𝕭': "B",
    '𝖡': "B",
    '𝗕': "B",
    '𝘉': "B",
    '𝘽': "B",
    '𝙱': "B",
    'Ꞵ': "B",
    'Β': "B",
    '𝚩': "B",
    '𝛣': "B",
    '𝜝': "B",
    '𝝗': "B",
    '𝞑': "B",
    'В': "B",
    'Ᏼ': "B",
    'ᗷ': "B",
    'ꓐ': "B",
    '𐊂': "B",
    '𐊡': "B",
    '𐌁': "B",
    'в': "B",
    'ᏼ': "B",
    'ｃ': "c",
    'ⅽ': "c",
    '𝐜': "c",
    '𝑐': "c",
    '𝒄': "c",
    '𝒸': "c",
    '𝓬': "c",
    '𝔠': "c",
    '𝕔': "c",
    '𝖈': "c",
    '𝖼': "c",
    '𝗰': "c",
    '𝘤': "c",
    '𝙘': "c",
    '𝚌': "c",
    'ᴄ': "c",
    'ϲ': "c",
    'ⲥ': "c",
    'с': "c",
    'ꮯ': "c",
    '𐐽': "c",
    '🝌': "C",
    '𑣲': "C",
    '𑣩': "C",
    'Ｃ': "C",
    'Ⅽ': "C",
    'ℂ': "C",
    'ℭ': "C",
    '𝐂': "C",
    '𝐶': "C",
    '𝑪': "C",
    '𝒞': "C",
    '𝓒': "C",
    '𝕮': "C",
    '𝖢': "C",
    '𝗖': "C",
    '𝘊': "C",
    '𝘾': "C",
    '𝙲': "C",
    'Ϲ': "C",
    'Ⲥ': "C",
    'С': "C",
    'Ꮯ': "C",
    'ꓚ': "C",
    '𐊢': "C",
    '𐌂': "C",
    '𐐕': "C",
    '𐔜': "C",
    '⋴': "e",
    'ɛ': "e",
    'ε': "e",
    'ϵ': "e",
    '𝛆': "e",
    '𝛜': "e",
    '𝜀': "e",
    '𝜖': "e",
    '𝜺': "e",
    '𝝐': "e",
    '𝝴': "e",
    '𝞊': "e",
    '𝞮': "e",
    '𝟄': "e",
    'ⲉ': "e",
    'є': "e",
    'ԑ': "e",
    'ꮛ': "e",
    '𑣎': "e",
    '𐐩': "e",
    '€': "e",
    'Ⲉ': "e",
    'Є': "e",
    'ⅾ': "d",
    'ⅆ': "d",
    '𝐝': "d",
    '𝑑': "d",
    '𝒅': "d",
    '𝒹': "d",
    '𝓭': "d",
    '𝔡': "d",
    '𝕕': "d",
    '𝖉': "d",
    '𝖽': "d",
    '𝗱': "d",
    '𝘥': "d",
    '𝙙': "d",
    '𝚍': "d",
    'ԁ': "d",
    'Ꮷ': "d",
    'ᑯ': "d",
    'ꓒ': "d",
    'Ⅾ': "D",
    'ⅅ': "D",
    '𝐃': "D",
    '𝐷': "D",
    '𝑫': "D",
    '𝒟': "D",
    '𝓓': "D",
    '𝔇': "D",
    '𝔻': "D",
    '𝕯': "D",
    '𝖣': "D",
    '𝗗': "D",
    '𝘋': "D",
    '𝘿': "D",
    '𝙳': "D",
    'Ꭰ': "D",
    'ᗞ': "D",
    'ᗪ': "D",
    'ꓓ': "D",
    'ꭰ': "D",
    '℮': "e",
    'ｅ': "e",
    'ℯ': "e",
    'ⅇ': "e",
    '𝐞': "e",
    '𝑒': "e",
    '𝒆': "e",
    '𝓮': "e",
    '𝔢': "e",
    '𝕖': "e",
    '𝖊': "e",
    '𝖾': "e",
    '𝗲': "e",
    '𝘦': "e",
    '𝙚': "e",
    '𝚎': "e",
    'ꬲ': "e",
    'е': "e",
    'ҽ': "e",
    '⋿': "E",
    'Ｅ': "E",
    'ℰ': "E",
    '𝐄': "E",
    '𝐸': "E",
    '𝑬': "E",
    '𝓔': "E",
    '𝔈': "E",
    '𝔼': "E",
    '𝕰': "E",
    '𝖤': "E",
    '𝗘': "E",
    '𝘌': "E",
    '𝙀': "E",
    '𝙴': "E",
    'Ε': "E",
    '𝚬': "E",
    '𝛦': "E",
    '𝜠': "E",
    '𝝚': "E",
    '𝞔': "E",
    'Е': "E",
    'ⴹ': "E",
    'Ꭼ': "E",
    'ꓰ': "E",
    '𑢦': "E",
    '𑢮': "E",
    '𐊆': "E",
    'ě': "e",
    'Ě': "E",
    'ꭼ': "E",
    '𝈡': "E",
    'ℇ': "E",
    'Ԑ': "E",
    'Ꮛ': "E",
    '𖼭': "E",
    '𐐁': "E",
    '𝐟': "f",
    '𝑓': "f",
    '𝒇': "f",
    '𝒻': "f",
    '𝓯': "f",
    '𝔣': "f",
    '𝕗': "f",
    '𝖋': "f",
    '𝖿': "f",
    '𝗳': "f",
    '𝘧': "f",
    '𝙛': "f",
    '𝚏': "f",
    'ꬵ': "f",
    'ꞙ': "f",
    'ſ': "f",
    'ẝ': "f",
    'ք': "f",
    '𝈓': "F",
    'ℱ': "F",
    '𝐅': "F",
    '𝐹': "F",
    '𝑭': "F",
    '𝓕': "F",
    '𝔉': "F",
    '𝔽': "F",
    '𝕱': "F",
    '𝖥': "F",
    '𝗙': "F",
    '𝘍': "F",
    '𝙁': "F",
    '𝙵': "F",
    'Ꞙ': "F",
    'Ϝ': "F",
    '𝟊': "F",
    'ᖴ': "F",
    'ꓝ': "F",
    '𑣂': "F",
    '𑢢': "F",
    '𐊇': "F",
    '𐊥': "F",
    '𐔥': "F",
    'ｇ': "g",
    'ℊ': "g",
    '𝐠': "g",
    '𝑔': "g",
    '𝒈': "g",
    '𝓰': "g",
    '𝔤': "g",
    '𝕘': "g",
    '𝖌': "g",
    '𝗀': "g",
    '𝗴': "g",
    '𝘨': "g",
    '𝙜': "g",
    '𝚐': "g",
    'ɡ': "g",
    'ᶃ': "g",
    'ƍ': "g",
    'ց': "g",
    '𝐆': "G",
    '𝐺': "G",
    '𝑮': "G",
    '𝒢': "G",
    '𝓖': "G",
    '𝔊': "G",
    '𝔾': "G",
    '𝕲': "G",
    '𝖦': "G",
    '𝗚': "G",
    '𝘎': "G",
    '𝙂': "G",
    '𝙶': "G",
    'Ԍ': "G",
    'Ꮐ': "G",
    'Ᏻ': "G",
    'ꓖ': "G",
    'ᶢ': "g",
    'ǧ': "g",
    'Ǧ': "G",
    'ǵ': "g",
    'ԍ': "G",
    'ꮐ': "G",
    'ᏻ': "G",
    'ｈ': "h",
    'ℎ': "h",
    '𝐡': "h",
    '𝒉': "h",
    '𝒽': "h",
    '𝓱': "h",
    '𝔥': "h",
    '𝕙': "h",
    '𝖍': "h",
    '𝗁': "h",
    '𝗵': "h",
    '𝘩': "h",
    '𝙝': "h",
    '𝚑': "h",
    'һ': "h",
    'հ': "h",
    'Ꮒ': "h",
    'Ｈ': "H",
    'ℋ': "H",
    'ℌ': "H",
    'ℍ': "H",
    '𝐇': "H",
    '𝐻': "H",
    '𝑯': "H",
    '𝓗': "H",
    '𝕳': "H",
    '𝖧': "H",
    '𝗛': "H",
    '𝘏': "H",
    '𝙃': "H",
    '𝙷': "H",
    'Η': "H",
    '𝚮': "H",
    '𝛨': "H",
    '𝜢': "H",
    '𝝜': "H",
    '𝞖': "H",
    'Ⲏ': "H",
    'Н': "H",
    'Ꮋ': "H",
    'ᕼ': "H",
    'ꓧ': "H",
    '𐋏': "H",
    'ᵸ': "F",
    'н': "ʜ",
    'ꮋ': "ʜ",
    'Ԋ': "H",
    'ꞕ': "h",
    '˛': "i",
    '⍳': "i",
    'ｉ': "i",
    'ⅰ': "i",
    'ℹ': "i",
    'ⅈ': "i",
    '𝐢': "i",
    '𝑖': "i",
    '𝒊': "i",
    '𝒾': "i",
    '𝓲': "i",
    '𝔦': "i",
    '𝕚': "i",
    '𝖎': "i",
    '𝗂': "i",
    '𝗶': "i",
    '𝘪': "i",
    '𝙞': "i",
    '𝚒': "i",
    'ı': "i",
    '𝚤': "i",
    'ɪ': "i",
    'ɩ': "i",
    'ι': "i",
    'ι': "i",
    'ͺ': "i",
    '𝛊': "i",
    '𝜄': "i",
    '𝜾': "i",
    '𝝸': "i",
    '𝞲': "i",
    'і': "i",
    'ꙇ': "i",
    'ӏ': "i",
    'ꭵ': "i",
    'Ꭵ': "i",
    '𑣃': "i",
    'ⓛ': "I",
    'ǐ': "i",
    'Ǐ': "I",
    'ｊ': "j",
    'ⅉ': "j",
    '𝐣': "j",
    '𝑗': "j",
    '𝒋': "j",
    '𝒿': "j",
    '𝓳': "j",
    '𝔧': "j",
    '𝕛': "j",
    '𝖏': "j",
    '𝗃': "j",
    '𝗷': "j",
    '𝘫': "j",
    '𝙟': "j",
    '𝚓': "j",
    'ϳ': "j",
    'ј': "j",
    'Ｊ': "j",
    '𝐉': "J",
    '𝐽': "J",
    '𝑱': "J",
    '𝒥': "J",
    '𝓙': "J",
    '𝔍': "J",
    '𝕁': "J",
    '𝕵': "J",
    '𝖩': "J",
    '𝗝': "J",
    '𝘑': "J",
    '𝙅': "J",
    '𝙹': "J",
    'Ʝ': "J",
    'Ϳ': "J",
    'Ј': "J",
    'Ꭻ': "J",
    'ᒍ': "J",
    'ꓙ': "J",
    '𝚥': "ȷ",
    'յ': "ȷ",
    'ꭻ': "j",
    '𝐤': "k",
    '𝑘': "k",
    '𝒌': "k",
    '𝓀': "k",
    '𝓴': "k",
    '𝔨': "k",
    '𝕜': "k",
    '𝖐': "k",
    '𝗄': "k",
    '𝗸': "k",
    '𝘬': "k",
    '𝙠': "k",
    '𝚔': "k",
    'K': "K",
    'Ｋ': "K",
    '𝐊': "K",
    '𝐾': "K",
    '𝑲': "K",
    '𝒦': "K",
    '𝓚': "K",
    '𝔎': "K",
    '𝕂': "K",
    '𝕶': "K",
    '𝖪': "K",
    '𝗞': "K",
    '𝘒': "K",
    '𝙆': "K",
    '𝙺': "K",
    'Κ': "K",
    '𝚱': "K",
    '𝛫': "K",
    '𝜥': "K",
    '𝝟': "K",
    '𝞙': "K",
    'Ⲕ': "K",
    'К': "K",
    'Ꮶ': "K",
    'ᛕ': "K",
    'ꓗ': "K",
    '𐔘': "K",
    '|': "l",
    '∣': "l",
    '⏽': "l",
    '￨': "l",
    '1': "l",
    '۱': "l",
    '𐌠': "l",
    '𝟏': "l",
    '𝟙': "l",
    '𝟣': "l",
    '𝟭': "l",
    '𝟷': "l",
    '🯱': "l",
    'I': "l",
    'Ｉ': "l",
    'Ⅰ': "l",
    'ℐ': "l",
    'ℑ': "l",
    '𝐈': "l",
    '𝐼': "l",
    '𝑰': "l",
    '𝓘': "l",
    '𝕀': "l",
    '𝕴': "l",
    '𝖨': "l",
    '𝗜': "l",
    '𝘐': "l",
    '𝙄': "l",
    '𝙸': "l",
    'Ɩ': "l",
    'ｌ': "l",
    'ⅼ': "l",
    'ℓ': "l",
    '𝐥': "l",
    '𝑙': "l",
    '𝒍': "l",
    '𝓁': "l",
    '𝓵': "l",
    '𝔩': "l",
    '𝕝': "l",
    '𝖑': "l",
    '𝗅': "l",
    '𝗹': "l",
    '𝘭': "l",
    '𝙡': "l",
    '𝚕': "l",
    'ǀ': "l",
    'Ι': "l",
    '𝚰': "l",
    '𝛪': "l",
    '𝜤': "l",
    '𝝞': "l",
    '𝞘': "l",
    'Ⲓ': "l",
    'І': "l",
    'Ӏ': "l",
    'ⵏ': "l",
    'ᛁ': "l",
    'ꓲ': "l",
    '𖼨': "l",
    '𐊊': "l",
    '𐌉': "l",
    '𝈪': "L",
    'Ⅼ': "L",
    'ℒ': "L",
    '𝐋': "L",
    '𝐿': "L",
    '𝑳': "L",
    '𝓛': "L",
    '𝔏': "L",
    '𝕃': "L",
    '𝕷': "L",
    '𝖫': "L",
    '𝗟': "L",
    '𝘓': "L",
    '𝙇': "L",
    '𝙻': "L",
    'Ⳑ': "L",
    'Ꮮ': "L",
    'ᒪ': "L",
    'ꓡ': "L",
    '𖼖': "L",
    '𑢣': "L",
    '𑢲': "L",
    '𐐛': "L",
    '𐔦': "L",
    'ⳑ': "L",
    'ꮮ': "L",
    '𐑃': "L",
    'Ｍ': "M",
    'Ⅿ': "M",
    'ℳ': "M",
    '𝐌': "M",
    '𝑀': "M",
    '𝑴': "M",
    '𝓜': "M",
    '𝔐': "M",
    '𝕄': "M",
    '𝕸': "M",
    '𝖬': "M",
    '𝗠': "M",
    '𝘔': "M",
    '𝙈': "M",
    '𝙼': "M",
    'Μ': "M",
    '𝚳': "M",
    '𝛭': "M",
    '𝜧': "M",
    '𝝡': "M",
    '𝞛': "M",
    'Ϻ': "M",
    'Ⲙ': "M",
    'М': "M",
    'Ꮇ': "M",
    'ᗰ': "M",
    'ᛖ': "M",
    'ꓟ': "M",
    '𐊰': "M",
    '𐌑': "M",
    '𝐧': "n",
    '𝑛': "n",
    '𝒏': "n",
    '𝓃': "n",
    '𝓷': "n",
    '𝔫': "n",
    '𝕟': "n",
    '𝖓': "n",
    '𝗇': "n",
    '𝗻': "n",
    '𝘯': "n",
    '𝙣': "n",
    '𝚗': "n",
    'ո': "n",
    'ռ': "n",
    'Ｎ': "N",
    'ℕ': "N",
    '𝐍': "N",
    '𝑁': "N",
    '𝑵': "N",
    '𝒩': "N",
    '𝓝': "N",
    '𝔑': "N",
    '𝕹': "N",
    '𝖭': "N",
    '𝗡': "N",
    '𝘕': "N",
    '𝙉': "N",
    '𝙽': "N",
    'Ν': "N",
    '𝚴': "N",
    '𝛮': "N",
    '𝜨': "N",
    '𝝢': "N",
    '𝞜': "N",
    'Ⲛ': "N",
    'ꓠ': "N",
    '𐔓': "N",
    'ం': "o",
    'ಂ': "o",
    'ം': "o",
    'ං': "o",
    '०': "o",
    '੦': "o",
    '૦': "o",
    '௦': "o",
    '౦': "o",
    '೦': "o",
    '൦': "o",
    '๐': "o",
    '໐': "o",
    '၀': "o",
    '۵': "o",
    'ｏ': "o",
    'ℴ': "o",
    '𝐨': "o",
    '𝑜': "o",
    '𝒐': "o",
    '𝓸': "o",
    '𝔬': "o",
    '𝕠': "o",
    '𝖔': "o",
    '𝗈': "o",
    '𝗼': "o",
    '𝘰': "o",
    '𝙤': "o",
    '𝚘': "o",
    'ᴏ': "o",
    'ᴑ': "o",
    'ꬽ': "o",
    'ο': "o",
    '𝛐': "o",
    '𝜊': "o",
    '𝝄': "o",
    '𝝾': "o",
    '𝞸': "o",
    'σ': "o",
    '𝛔': "o",
    '𝜎': "o",
    '𝝈': "o",
    '𝞂': "o",
    '𝞼': "o",
    'ⲟ': "o",
    'о': "o",
    'ჿ': "o",
    'օ': "o",
    'ഠ': "o",
    'ဝ': "o",
    '𐓪': "o",
    '𑣈': "o",
    '𑣗': "o",
    '𐐬': "o",
#    '0': "O",
    '০': "O",
    '୦': "O",
    '〇': "O",
    '𑓐': "O",
    '𑣠': "O",
    '𝟎': "O",
    '𝟘': "O",
    '𝟢': "O",
    '𝟬': "O",
    '𝟶': "O",
    '🯰': "O",
    'Ｏ': "O",
    '𝐎': "O",
    '𝑂': "O",
    '𝑶': "O",
    '𝒪': "O",
    '𝓞': "O",
    '𝔒': "O",
    '𝕆': "O",
    '𝕺': "O",
    '𝖮': "O",
    '𝗢': "O",
    '𝘖': "O",
    '𝙊': "O",
    '𝙾': "O",
    'Ο': "O",
    '𝚶': "O",
    '𝛰': "O",
    '𝜪': "O",
    '𝝤': "O",
    '𝞞': "O",
    'Ⲟ': "O",
    'О': "O",
    'Օ': "O",
    'ⵔ': "O",
    'ዐ': "O",
    'ଠ': "O",
    '𐓂': "O",
    'ꓳ': "O",
    '𑢵': "O",
    '𐊒': "O",
    '𐊫': "O",
    '𐐄': "O",
    '𐔖': "O",
    'ǒ': "o",
    'Ǒ': "O",
    'Ő': "O",
    '⍴': "p",
    'ｐ': "p",
    '𝐩': "p",
    '𝑝': "p",
    '𝒑': "p",
    '𝓅': "p",
    '𝓹': "p",
    '𝔭': "p",
    '𝕡': "p",
    '𝖕': "p",
    '𝗉': "p",
    '𝗽': "p",
    '𝘱': "p",
    '𝙥': "p",
    '𝚙': "p",
    'ρ': "p",
    'ϱ': "p",
    '𝛒': "p",
    '𝛠': "p",
    '𝜌': "p",
    '𝜚': "p",
    '𝝆': "p",
    '𝝔': "p",
    '𝞀': "p",
    '𝞎': "p",
    '𝞺': "p",
    '𝟈': "p",
    'ⲣ': "p",
    'р': "p",
    'Ｐ': "P",
    'ℙ': "P",
    '𝐏': "P",
    '𝑃': "P",
    '𝑷': "P",
    '𝒫': "P",
    '𝓟': "P",
    '𝔓': "P",
    '𝕻': "P",
    '𝖯': "P",
    '𝗣': "P",
    '𝘗': "P",
    '𝙋': "P",
    '𝙿': "P",
    'Ρ': "P",
    '𝚸': "P",
    '𝛲': "P",
    '𝜬': "P",
    '𝝦': "P",
    '𝞠': "P",
    'Ⲣ': "P",
    'Р': "P",
    'Ꮲ': "P",
    'ᑭ': "P",
    'ꓑ': "P",
    '𐊕': "P",
    'ᴩ': "P",
    'ꮲ': "P",
    '𝐪': "q",
    '𝑞': "q",
    '𝒒': "q",
    '𝓆': "q",
    '𝓺': "q",
    '𝔮': "q",
    '𝕢': "q",
    '𝖖': "q",
    '𝗊': "q",
    '𝗾': "q",
    '𝘲': "q",
    '𝙦': "q",
    '𝚚': "q",
    'ԛ': "q",
    'գ': "q",
    'զ': "q",
    'ℚ': "Q",
    '𝐐': "Q",
    '𝑄': "Q",
    '𝑸': "Q",
    '𝒬': "Q",
    '𝓠': "Q",
    '𝔔': "Q",
    '𝕼': "Q",
    '𝖰': "Q",
    '𝗤': "Q",
    '𝘘': "Q",
    '𝙌': "Q",
    '𝚀': "Q",
    'ⵕ': "Q",
    'ᶐ': "ɋ",
    'ᴋ': "K",
    'κ': "K",
    'ϰ': "K",
    '𝛋': "K",
    '𝛞': "K",
    '𝜅': "K",
    '𝜘': "K",
    '𝜿': "K",
    '𝝒': "K",
    '𝝹': "K",
    '𝞌': "K",
    '𝞳': "K",
    '𝟆': "K",
    'ⲕ': "K",
    'к': "K",
    'ꮶ': "K",
    '𝐫': "r",
    '𝑟': "r",
    '𝒓': "r",
    '𝓇': "r",
    '𝓻': "r",
    '𝔯': "r",
    '𝕣': "r",
    '𝖗': "r",
    '𝗋': "r",
    '𝗿': "r",
    '𝘳': "r",
    '𝙧': "r",
    '𝚛': "r",
    'ꭇ': "r",
    'ꭈ': "r",
    'ᴦ': "r",
    'ⲅ': "r",
    'г': "r",
    'ꮁ': "r",
    '𝈖': "R",
    'ℛ': "R",
    'ℜ': "R",
    'ℝ': "R",
    '𝐑': "R",
    '𝑅': "R",
    '𝑹': "R",
    '𝓡': "R",
    '𝕽': "R",
    '𝖱': "R",
    '𝗥': "R",
    '𝘙': "R",
    '𝙍': "R",
    '𝚁': "R",
    'Ʀ': "R",
    'Ꭱ': "R",
    'Ꮢ': "R",
    '𐒴': "R",
    'ᖇ': "R",
    'ꓣ': "R",
    '𖼵': "R",
    'ꭱ': "R",
    'ꮢ': "R",
    'ｓ': "s",
    '𝐬': "s",
    '𝑠': "s",
    '𝒔': "s",
    '𝓈': "s",
    '𝓼': "s",
    '𝔰': "s",
    '𝕤': "s",
    '𝖘': "s",
    '𝗌': "s",
    '𝘀': "s",
    '𝘴': "s",
    '𝙨': "s",
    '𝚜': "s",
    'ꜱ': "s",
    'ƽ': "s",
    'ѕ': "s",
    'ꮪ': "s",
    '𑣁': "s",
    '𐑈': "s",
    'Ｓ': "S",
    '𝐒': "S",
    '𝑆': "S",
    '𝑺': "S",
    '𝒮': "S",
    '𝓢': "S",
    '𝔖': "S",
    '𝕊': "S",
    '𝕾': "S",
    '𝖲': "S",
    '𝗦': "S",
    '𝘚': "S",
    '𝙎': "S",
    '𝚂': "S",
    'Ѕ': "S",
    'Տ': "S",
    'Ꮥ': "S",
    'Ꮪ': "S",
    'ꓢ': "S",
    '𖼺': "S",
    '𐊖': "S",
    '𐐠': "S",
    '𝐭': "t",
    '𝑡': "t",
    '𝒕': "t",
    '𝓉': "t",
    '𝓽': "t",
    '𝔱': "t",
    '𝕥': "t",
    '𝖙': "t",
    '𝗍': "t",
    '𝘁': "t",
    '𝘵': "t",
    '𝙩': "t",
    '𝚝': "t",
    '⊤': "T",
    '⟙': "T",
    '🝨': "T",
    'Ｔ': "T",
    '𝐓': "T",
    '𝑇': "T",
    '𝑻': "T",
    '𝒯': "T",
    '𝓣': "T",
    '𝔗': "T",
    '𝕋': "T",
    '𝕿': "T",
    '𝖳': "T",
    '𝗧': "T",
    '𝘛': "T",
    '𝙏': "T",
    '𝚃': "T",
    'Τ': "T",
    '𝚻': "T",
    '𝛵': "T",
    '𝜯': "T",
    '𝝩': "T",
    '𝞣': "T",
    'Ⲧ': "T",
    'Т': "T",
    'Ꭲ': "T",
    'ꓔ': "T",
    '𖼊': "T",
    '𑢼': "T",
    '𐊗': "T",
    '𐊱': "T",
    '𐌕': "T",
    'Ț': "T",
    'Ⴀ': "T",
    'τ': "T",
    '𝛕': "T",
    '𝜏': "T",
    '𝝉': "T",
    '𝞃': "T",
    '𝞽': "T",
    'т': "T",
    'ꭲ': "T",
    'ţ': "t",
    'ț': "t",
    'Ꮏ': "t",
    '𝐮': "u",
    '𝑢': "u",
    '𝒖': "u",
    '𝓊': "u",
    '𝓾': "u",
    '𝔲': "u",
    '𝕦': "u",
    '𝖚': "u",
    '𝗎': "u",
    '𝘂': "u",
    '𝘶': "u",
    '𝙪': "u",
    '𝚞': "u",
    'ꞟ': "u",
    'ᴜ': "u",
    'ꭎ': "u",
    'ꭒ': "u",
    'ʋ': "u",
    'υ': "u",
    '𝛖': "u",
    '𝜐': "u",
    '𝝊': "u",
    '𝞄': "u",
    '𝞾': "u",
    'ս': "u",
    '𐓶': "u",
    '𑣘': "u",
    '∪': "U",
    '⋃': "U",
    '𝐔': "U",
    '𝑈': "U",
    '𝑼': "U",
    '𝒰': "U",
    '𝓤': "U",
    '𝔘': "U",
    '𝕌': "U",
    '𝖀': "U",
    '𝖴': "U",
    '𝗨': "U",
    '𝘜': "U",
    '𝙐': "U",
    '𝚄': "U",
    'Ս': "U",
    'ሀ': "U",
    '𐓎': "U",
    'ᑌ': "U",
    'ꓴ': "U",
    '𖽂': "U",
    '𑢸': "U",
    'ǔ': "u",
    'Ǔ': "U",
    '∨': "v",
    '⋁': "v",
    'ｖ': "v",
    'ⅴ': "v",
    '𝐯': "v",
    '𝑣': "v",
    '𝒗': "v",
    '𝓋': "v",
    '𝓿': "v",
    '𝔳': "v",
    '𝕧': "v",
    '𝖛': "v",
    '𝗏': "v",
    '𝘃': "v",
    '𝘷': "v",
    '𝙫': "v",
    '𝚟': "v",
    'ᴠ': "v",
    'ν': "v",
    '𝛎': "v",
    '𝜈': "v",
    '𝝂': "v",
    '𝝼': "v",
    '𝞶': "v",
    'ѵ': "v",
    '𑜆': "v",
    'ꮩ': "v",
    '𑣀': "v",
    '𝈍': "V",
    '۷': "V",
    'Ⅴ': "V",
    '𝐕': "V",
    '𝑉': "V",
    '𝑽': "V",
    '𝒱': "V",
    '𝓥': "V",
    '𝔙': "V",
    '𝕍': "V",
    '𝖁': "V",
    '𝖵': "V",
    '𝗩': "V",
    '𝘝': "V",
    '𝙑': "V",
    '𝚅': "V",
    'Ѵ': "V",
    'ⴸ': "V",
    'Ꮩ': "V",
    'ᐯ': "V",
    'ꛟ': "V",
    'ꓦ': "V",
    '𖼈': "V",
    '𑢠': "V",
    '𐔝': "V",
    'ɯ': "w",
    '𝐰': "w",
    '𝑤': "w",
    '𝒘': "w",
    '𝓌': "w",
    '𝔀': "w",
    '𝔴': "w",
    '𝕨': "w",
    '𝖜': "w",
    '𝗐': "w",
    '𝘄': "w",
    '𝘸': "w",
    '𝙬': "w",
    '𝚠': "w",
    'ᴡ': "w",
    'ѡ': "w",
    'ԝ': "w",
    'ա': "w",
    '𑜊': "w",
    '𑜎': "w",
    '𑜏': "w",
    'ꮃ': "w",
    '𑣯': "W",
    '𑣦': "W",
    '𝐖': "W",
    '𝑊': "W",
    '𝑾': "W",
    '𝒲': "W",
    '𝓦': "W",
    '𝔚': "W",
    '𝕎': "W",
    '𝖂': "W",
    '𝖶': "W",
    '𝗪': "W",
    '𝘞': "W",
    '𝙒': "W",
    '𝚆': "W",
    'Ԝ': "W",
    'Ꮃ': "W",
    'Ꮤ': "W",
    'ꓪ': "W",
    'ᴍ': "M",
    'м': "M",
    'ꮇ': "M",
    '᙮': "x",
    '×': "x",
    '⤫': "x",
    '⤬': "x",
    '⨯': "x",
    'ｘ': "x",
    'ⅹ': "x",
    '𝐱': "x",
    '𝑥': "x",
    '𝒙': "x",
    '𝓍': "x",
    '𝔁': "x",
    '𝔵': "x",
    '𝕩': "x",
    '𝖝': "x",
    '𝗑': "x",
    '𝘅': "x",
    '𝘹': "x",
    '𝙭': "x",
    '𝚡': "x",
    'х': "x",
    'ᕁ': "x",
    'ᕽ': "x",
    '᙭': "X",
    '╳': "X",
    '𐌢': "X",
    '𑣬': "X",
    'Ｘ': "X",
    'Ⅹ': "X",
    '𝐗': "X",
    '𝑋': "X",
    '𝑿': "X",
    '𝒳': "X",
    '𝓧': "X",
    '𝔛': "X",
    '𝕏': "X",
    '𝖃': "X",
    '𝖷': "X",
    '𝗫': "X",
    '𝘟': "X",
    '𝙓': "X",
    '𝚇': "X",
    'Ꭓ': "X",
    'Χ': "X",
    '𝚾': "X",
    '𝛸': "X",
    '𝜲': "X",
    '𝝬': "X",
    '𝞦': "X",
    'Ⲭ': "X",
    'Х': "X",
    'ⵝ': "X",
    'ᚷ': "X",
    'ꓫ': "X",
    '𐊐': "X",
    '𐊴': "X",
    '𐌗': "X",
    '𐔧': "X",
    'ɣ': "y",
    'ᶌ': "y",
    'ｙ': "y",
    '𝐲': "y",
    '𝑦': "y",
    '𝒚': "y",
    '𝓎': "y",
    '𝔂': "y",
    '𝔶': "y",
    '𝕪': "y",
    '𝖞': "y",
    '𝗒': "y",
    '𝘆': "y",
    '𝘺': "y",
    '𝙮': "y",
    '𝚢': "y",
    'ʏ': "y",
    'ỿ': "y",
    'ꭚ': "y",
    'γ': "y",
    'ℽ': "y",
    '𝛄': "y",
    '𝛾': "y",
    '𝜸': "y",
    '𝝲': "y",
    '𝞬': "y",
    'у': "y",
    'ү': "y",
    'ყ': "y",
    '𑣜': "y",
    'Ｙ': "Y",
    '𝐘': "Y",
    '𝑌': "Y",
    '𝒀': "Y",
    '𝒴': "Y",
    '𝓨': "Y",
    '𝔜': "Y",
    '𝕐': "Y",
    '𝖄': "Y",
    '𝖸': "Y",
    '𝗬': "Y",
    '𝘠': "Y",
    '𝙔': "Y",
    '𝚈': "Y",
    'Υ': "Y",
    'ϒ': "Y",
    '𝚼': "Y",
    '𝛶': "Y",
    '𝜰': "Y",
    '𝝪': "Y",
    '𝞤': "Y",
    'Ⲩ': "Y",
    'У': "Y",
    'Ү': "Y",
    'Ꭹ': "Y",
    'Ꮍ': "Y",
    'ꓬ': "Y",
    '𖽃': "Y",
    '𑢤': "Y",
    '𐊲': "Y",
    'ʒ': "3",
    'ꝫ': "3",
    'ⳍ': "3",
    'ӡ': "3",
    'ჳ': "3",
    '𝐳': "z",
    '𝑧': "z",
    '𝒛': "z",
    '𝓏': "z",
    '𝔃': "z",
    '𝔷': "z",
    '𝕫': "z",
    '𝖟': "z",
    '𝗓': "z",
    '𝘇': "z",
    '𝘻': "z",
    '𝙯': "z",
    '𝚣': "z",
    'ᴢ': "z",
    'ꮓ': "z",
    '𑣄': "z",
    '𐋵': "Z",
    '𑣥': "Z",
    'Ｚ': "Z",
    'ℤ': "Z",
    'ℨ': "Z",
    '𝐙': "Z",
    '𝑍': "Z",
    '𝒁': "Z",
    '𝒵': "Z",
    '𝓩': "Z",
    '𝖅': "Z",
    '𝖹': "Z",
    '𝗭': "Z",
    '𝘡': "Z",
    '𝙕': "Z",
    '𝚉': "Z",
    'Ζ': "Z",
    '𝚭': "Z",
    '𝛧': "Z",
    '𝜡': "Z",
    '𝝛': "Z",
    '𝞕': "Z",
    'Ꮓ': "Z",
    'ꓜ': "Z",
    '𑢩': "Z",
}

CONFUSABLE_OVERRIDES = {
    '“': '"',
    '”': '"',
    'O': '0',
    '𝟶': '0',
    '𝟷': '1',
    'ᴀ': 'a',
    'ʙ': 'b',
    'ß': 'b',
    'в': 'b',
    'ᏼ': 'b',
    'ͼ': 'c',
    'ċ': 'c',
    'ᴅ': 'd',
    'ᴆ': 'đ',
    'ᵭ': 'đ',
    'ƌ': 'đ',
    'ᴇ': 'e',
    'ꜰ': 'f',
    'ɢ': 'g',
    'ǥ': 'g',
    'н': 'h',
    'ʜ': 'h',
    'ɦ': 'h',
    'Һ': 'h',
    '𝚒': 'i',
    'เ': 'i',
    'ⱪ': 'k',
    'ᴋ': 'k',
    'к': 'k',
    'Ҝ': 'k',
    'ƙ': 'k',
    '𝚕': 'l',
    'ʟ': 'l',
    '꒒': 'l',
    'Ŀ': 'L',
    'ᴍ': 'm',
    'м': 'm',
    'ɴ': 'n',
    'ท': 'n',
    'п': 'n',
    'ṅ': 'n',
    'ᶇ': 'n',
    'ɳ': 'n',
    '𝚘': 'o',
    'ѻ': 'o',
    'ք': 'p',
    'ᴘ': 'p',
    'ק': 'p',
    'ꞯ': 'q',
    '𝚚': 'q',
    'ɾ': 'r',
    'ʀ': 'r',
    '𝚜': 's',
    'Ꭶ': 's',
    'т': 't',
    'ᴛ': 't',
    'τ': 't',
    'ɫ': 't',
    'v': 'v',
    '𝚡': 'x',
    'ÿ': 'y',
    'ɣ': 'y',
}

CONFUSABLE_CHAR_TRANS = str.maketrans({**CONFUSABLES, **CONFUSABLE_OVERRIDES})
