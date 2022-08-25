from typing import NamedTuple

class ParseError(ValueError):
    def __init__(self, message, pos: int, *args):
        self.message = message
        self.pos = pos
        
        super().__init__(message, *args)

PROVINCE_ID_DICT = {
    1: "Hà Nội",
    2: "Hà Giang",
    4: "Cao Bằng",
    6: "Bắc Kạn",
    8: "Tuyên Quang",
    10: "Lào Cai",
    11: "Điện Biên",
    12: "Lai Châu",
    14: "Sơn La",
    15: "Yên Bái",
    17: "Hoà Bình",
    19: "Thái Nguyên",
    20: "Lạng Sơn",
    22: "Quảng Ninh",
    24: "Bắc Giang",
    25: "Phú Thọ",
    26: "Vĩnh Phúc",
    27: "Bắc Ninh",
    28: "Hà Tây",
    30: "Hải Dương",
    31: "Hải Phòng",
    33: "Hưng Yên",
    34: "Thái Bình",
    35: "Hà Nam",
    36: "Nam Định",
    37: "Ninh Bình",
    38: "Thanh Hóa",
    40: "Nghệ An",
    42: "Hà Tĩnh",
    44: "Quảng Bình",
    45: "Quảng Trị",
    46: "Thừa Thiên – Huế",
    48: "Đà Nẵng",
    49: "Quảng Nam",
    51: "Quảng Ngãi",
    52: "Bình Định",
    54: "Phú Yên",
    56: "Khánh Hòa",
    58: "Ninh Thuận",
    60: "Bình Thuận",
    62: "Kon Tum",
    64: "Gia Lai",
    66: "Đắk Lắk",
    67: "Đắk Nông",
    68: "Lâm Đồng",
    70: "Bình Phước",
    72: "Tây Ninh",
    74: "Bình Dương",
    75: "Đồng Nai",
    77: "Bà Rịa – Vũng Tàu",
    79: "Hồ Chí Minh",
    80: "Long An",
    82: "Tiền Giang",
    83: "Bến Tre",
    84: "Trà Vinh",
    86: "Vĩnh Long",
    87: "Đồng Tháp",
    89: "An Giang",
    91: "Kiên Giang",
    92: "Cần Thơ",
    93: "Hậu Giang",
    94: "Sóc Trăng",
    95: "Bạc Liêu",
    96: "Cà Mau",
}

COUNTRY_ID_DICT = {
 101: 'Afghanistan',
 102: 'Ai Cập',
 103: 'Albania',
 104: 'Algérie (An-giê-ri)',
 105: 'Andorra (An-đô-ra)',
 106: 'Angola (Ăng-gô-la)',
 107: 'Vương quốc Liên hiệp Anh và Bắc Ireland',
 108: 'Antigua và Barbuda (An-ti-goa và Bác-bu-da)',
 109: 'Áo',
 110: 'Ả Rập Saudi (Ả Rập Xê-út)',
 111: 'Argentina',
 112: 'Armenia (Ác-mê-ni-a)',
 113: 'Azerbaijan (A-giéc-bai-gian)',
 114: 'Cộng hòa Azerbaijan',
 115: 'Cộng hòa Ấn Độ',
 116: 'Bahamas (Ba-ha-mát)',
 117: 'Bahrain (Ba-ranh)',
 118: 'Ba Lan',
 119: 'Bangladesh (Băng-la-đét)',
 120: 'Barbados (Bác-ba-đốt)',
 121: 'Belarus (Bê-la-rút)',
 122: 'Belize (Bê-li-xê)',
 123: 'Benin (Bê-nanh)',
 124: 'Bhutan (Bu-tan)',
 125: 'Bỉ',
 126: 'Bolivia (Bô-li-vi-a)',
 127: 'Bosna và Hercegovina (Bốt-xni-a và Héc-dê-gô-vi-na)', 128: 'Botswana',
 129: 'Bồ Đào Nha',
 130: 'Bờ Biển Ngà (Cốt-đi-voa)',
 131: 'Brasil (Bra-xin)',
 132: 'Brunei (Bru-nây)',
 133: 'Bulgaria (Bungari)',
 134: 'Burkina Faso (Buốc-ki-na Pha-xô)',
 135: 'Burundi',
 136: 'Cabo Verde (Cáp Ve)',
 137: 'Các Tiểu Vương quốc Ả Rập Thống nhất',
 138: 'Cameroon (Ca-mơ-run)',
 139: 'Campuchia',
 140: 'Canada (Ca-na-đa; Gia Nã Đại)',
 141: 'Chile (Chi-lê)',
 142: 'Colombia (Cô-lôm-bi-a)',
 143: 'Comoros (Cô-mo)',
 144: 'Cộng hòa Congo (Công-gô; Congo-Brazzaville)',
 145: 'Cộng hòa Dân chủ Congo (Congo-Kinshasa)',
 146: 'Costa Rica (Cốt-xta Ri-ca)',
 147: 'Croatia (Crô-a-ti-a)',
 148: 'Cộng hòa Croatia',
 149: 'Cuba (Cu-ba)',
 150: 'Djibouti (Gi-bu-ti)',
 151: 'Dominica (Đô-mi-ni-ca)',
 152: 'Cộng hòa Dominicana (Đô-mi-ni-ca-na)',
 153: 'Đan Mạch',
 154: 'Đông Timor (Ti-mo Lex-te)',
 155: 'Đức',
 156: 'Ecuador (Ê-cu-a-đo)',
 157: 'El Salvador (En Xan-va-đo)',
 158: 'Eritrea (Ê-ri-tơ-ri-a)',
 159: 'Estonia (E-xtô-ni-a)',
 160: 'Ethiopia (Ê-t(h)i-ô-pi-a)',
 161: 'Fiji (Phi-gi)',
 162: 'Gabon (Ga-bông)',
 163: 'Gambia (Găm-bi-a)',
 164: 'Ghana (Ga-na)',
 165: 'Grenada (Grê-na-đa)',
 166: 'Gruzia (Gru-di-a)',
 167: 'Guatemala (Goa-tê-ma-la)',
 168: 'Guinea-Bissau (Ghi-nê Bít-xao)',
 169: 'Guinea Xích Đạo (Ghi-nê Xích Đạo)',
 170: 'Guinea (Ghi-nê)',
 171: 'Guyana (Gai-a-na)',
 172: 'Haiti (Ha-i-ti)',
 173: 'Hà Lan (Hòa Lan)',
 174: 'Hàn Quốc (Nam Hàn)',
 175: 'Hoa Kỳ (Mỹ)',
 176: 'Honduras (Hôn-đu-rát) (Ôn-đu-rát)',
 177: 'Hungary (Hung-ga-ri)',
 178: 'Hy Lạp',
 179: 'Iceland (Ai xơ len)',
 180: 'Indonesia (In-đô-nê-xi-a)',
 181: 'Iran',
 182: 'Iraq (I-rắc)',
 183: 'Ireland (Ai-len)',
 184: 'Israel (I-xra-en)',
 185: 'Jamaica (Gia-mai-ca)',
 186: 'Jordan (Gioóc-đan-ni)',
 187: 'Kazakhstan (Ca-dắc-xtan)',
 188: 'Kenya (Kê-nhi-a)',
 189: 'Kiribati',
 190: 'Kuwait (Cô-oét)',
 191: 'Síp',
 192: 'Kyrgyzstan (Cư-rơ-gư-xtan)',
 193: 'Lào',
 194: 'Latvia (Lat-vi-a)',
 195: 'Lesotho (Lê-xô-thô)',
 196: 'Li ban (Li-băng)',
 197: 'Liberia (Li-bê-ri-a)',
 198: 'Libya (Li-bi)',
 199: 'Liechtenstein (Lích-ten-xtai)',
 200: 'Litva (Lít-va)',
 201: 'Luxembourg (Lúc-xem-bua)',
 202: 'Macedonia (Mã Cơ Đốn) (Ma-xê-đô-ni-a)',
 203: 'Madagascar',
 204: 'Malawi (Ma-la-uy)',
 205: 'Malaysia (Mã Lai Tây Á) (Ma-lay-xi-a)',
 206: 'Maldives (Man-di-vơ)',
 207: 'Mali',
 208: 'Malta (Man-ta)',
 209: 'Maroc',
 210: 'Quần đảo Marshall',
 211: 'Mauritanie (Mô-ri-ta-ni)',
 212: 'Mauritius (Mô-ri-xơ)',
 213: 'Mexico (Mê-hi-cô)',
 214: 'Micronesia (Mi-crô-nê-di)',
 215: 'Moldova (Môn-đô-va)',
 216: 'Monaco (Mô-na-cô)',
 217: 'Mông Cổ',
 218: 'Montenegro (Môn-tê-nê-grô)',
 219: 'Mozambique (Mô-dăm-bích)',
 220: 'Myanma (Mi-an-ma)',
 221: 'Namibia (Na-mi-bi-a)',
 222: 'Nam Sudan',
 223: 'Nam Phi',
 224: 'Nauru (Nau-ru)',
 225: 'Na Uy',
 226: 'Nepal (Nê-pan)',
 227: 'New Zealand (Niu Di-lân) (Tân Tây Lan)',
 228: 'Nicaragua (Ni-ca-ra-goa)',
 229: 'Niger (Ni-giê)',
 230: 'Nigeria (Ni-giê-ri-a)',
 231: 'Nga',
 232: 'Nhật Bản',
 233: 'Oman (Ô-man)',
 234: 'Pakistan (Pa-kít-xtan)',
 235: 'Palau (Pa-lau)',
 236: 'Panama (Pa-na-ma)',
 237: 'Papua New Guinea (Pa-pua Niu Ghi-nê)',
 238: 'Paraguay (Pa-ra-goay)',
 239: 'Peru (Pê-ru)',
 240: 'Pháp (Pháp Lan Tây)',
 241: 'Phần Lan',
 242: 'Philippines (Phi-líp-pin)',
 243: 'Qatar (Ca-ta)',
 244: 'Romania (Ru-ma-ni, Lỗ Ma Ni)',
 245: 'Rwanda (Ru-an-đa)',
 246: 'Saint Kitts và Nevis (Xanh Kít và Nê-vít)',
 247: 'Saint Lucia (San-ta Lu-xi-a)',
 248: 'Saint Vincent và Grenadines (Xanh Vin-xen và Grê-na-din)',
 249: 'Samoa (Xa-moa)',
 250: 'San Marino (San Ma-ri-nô)',
 251: 'São Tomé và Príncipe (Sao Tô-mê và Prin-xi-pê)',
 252: 'Séc (Tiệp)',
 253: 'Sénégal (Xê-nê-gan)',
 254: 'Serbia (Xéc-bi-a)',
 255: 'Seychelles (Xây-sen)',
 256: 'Sierra Leone (Xi-ê-ra Lê-ôn)',
 257: 'Singapore (Xinh-ga-po)',
 258: 'Slovakia (Xlô-va-ki-a)',
 259: 'Slovenia (Xlô-ven-ni-a)',
 260: 'Solomon (Xô-lô-môn)',
 261: 'Somalia (Xô-ma-li)',
 262: 'Sri Lanka (Xri Lan-ca)',
 263: 'Sudan (Xu-đăng)',
 264: 'Suriname (Xu-ri-nam)',
 265: 'Swaziland (Xoa-di-len)',
 266: 'Syria (Xi-ri)',
 267: 'Tajikistan (Tát-gi-kít-xtan)',
 268: 'Tanzania (Tan-da-ni-a)',
 269: 'Tây Ban Nha',
 270: 'Tchad (Sát)',
 271: 'Thái Lan',
 272: 'Thổ Nhĩ Kỳ',
 273: 'Thụy Điển',
 274: 'Thụy Sĩ (Thụy Sỹ)',
 275: 'Togo (Tô-gô)',
 276: 'Tonga (Tông-ga)',
 277: 'Triều Tiên',
 278: 'Trinidad và Tobago (Tri-ni-đát và Tô-ba-gô)',
 279: 'Trung Quốc',
 280: 'Trung Phi',
 281: 'Tunisia (Tuy-ni-di)',
 282: 'Turkmenistan (Tuốc-mê-ni-xtan)',
 283: 'Tuvalu',
 284: 'Úc (Ốt-xrây-li-a)',
 285: 'Uganda (U-gan-đa)',
 286: 'Ukraina (U-crai-na)',
 287: 'Uruguay (U-ru-goay)',
 288: 'Uzbekistan (U-dơ-bê-kít-xtan)',
 289: 'Vanuatu (Va-nu-a-tu)',
 290: 'Thành Vatican (Va-ti-căng)/Tòa Thánh',
 291: 'Venezuela (Vê-nê-xu(y)-ê-la)',
 292: 'Ý (I-ta-li-a)',
 293: 'Yemen (Y-ê-men)',
 294: 'Zambia (Dăm-bi-a)',
 295: 'Zimbabwe (Dim-ba-bu-ê)'
}

class CccdResult(NamedTuple):
    id: str
    is_male: bool
    birth_year: int
    birth_country: str
    birth_province: str = None

def parse_cccd(raw) -> CccdResult:
    code = raw
    if isinstance(raw, int):
        code = f'{raw:012}'
    if len(code) != 12:
        raise ParseError("A citizen ID number must have 12 digits", 0)
    country = None
    province = None
    if code[0] == '0':
        country = "vn"
        try:
            province = PROVINCE_ID_DICT[int(code[1:3])]
        except KeyError:
            raise ParseError(f"Invalid province ID: {code[1:3]}", 1)
    else:
        try:
            country = COUNTRY_ID_DICT[int(code[0:3])]
        except KeyError:
            raise ParseError(f"Invalid country ID: {code[0:3]}", 0)
    century_code, gender = divmod(int(code[3]), 2)
    is_male = gender == 0
    year = 1900 + century_code * 100 + int(code[4:6])
    id = code[6:]
    return CccdResult(id, is_male, year, country, province)

def is_valid_cccd(raw) -> bool:
    try:
        parse_cccd(raw)
        return True
    except ParseError:
        return False