from typing import Union


def num_to_text(n: Union[int, float]):
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
        if 1 <= n <= 9:
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
        raise TypeError('The first parameter must be an integer or a float.')
    if int(n) == 0:
        tarr.append('không')
    elif int(n) < 0:
        tarr.append('âm')
        n = abs(n)
    ns = str(n)
    if isinstance(n, float) and '.' in ns:
        is_decimal = True
        intn, decn = ns.split('.')
        ns = intn
    else:
        is_decimal = False
    
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
    
    if is_decimal:
        tarr.append('phẩy')
        if len(decn) == 2 and decn[0] == 1:
            tarr.extend(per_thousand(int(decn)))
        else:
            tarr.extend(per_digit(int(decn)))
    tarr = list(filter(None, tarr))
    return ' '. join(tarr)