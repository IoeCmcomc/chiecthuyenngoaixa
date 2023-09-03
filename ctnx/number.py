# -*- coding: utf-8 -*-

from typing import Union, AnyStr, Generator
from decimal import Decimal, InvalidOperation


def num_to_words(n: Union[int, float, AnyStr, Decimal]) -> str:
    """Convert a number to Vietnamese words.

    Convert a number to its Vietnamese formal spoken form. It supports
    long numbers (both integers and decimals).

    Parameters
    ----------
    n : int, float, Decimal or str
        The number to be converted. If `n` is a str, it will be converted
        to a Decimal object.

    Returns
    -------
    str
        The spoken form of the number
    
    Raises
    ------
    TypeError
        If the input's type is neither int, float, str nor Decimal

    ValueError
        If the input string does not represent a valid number
    """
    
    digits = ('không', 'một', 'hai', 'ba', 'bốn', 'năm', 'sáu', 'bảy', 'tám', 'chín', 'mười')
    levels = ('đơn vị', 'nghìn', 'triệu')

    def partition(string: str, n: int) -> Generator:
        """Split a string from right to left to chunks of size n"""
        length = len(string)
        mod = length % n
        
        if mod != 0:
            yield string[0:mod]
            
        for i in range(mod, length, n):
            yield string[i:i+n]

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
    
    def per_billions(part: str):
        length = len(part)
        
        tarr = []
        for part in partition(part, 3):
            pn = int(part)
            if pn != 0:
                if part[0] == '0' and 1 <= pn <= 99:
                    tarr.append('không trăm')
                    linh = True
                else:
                    linh = False
                tarr.extend(per_thousand(pn, linh))
                thous = ((length - 1) // 3) % 3
                if thous > 0:
                    tarr.append(levels[thous])
            length -= 3
        return tarr

    text_list = []
    if isinstance(n, str):
        try:
            n = Decimal(n)
        except InvalidOperation as e:
            raise ValueError(f"'{n}' is not a valid number.")
    elif not isinstance(n, (int, float, Decimal)):
        raise TypeError('The first parameter must be an integer or a float.')
    if int(n) == 0:
        text_list.append('không')
    elif int(n) < 0:
        text_list.append('âm')
        n = abs(n)
    num_str = str(n)
    decimal_str = ''
    if '.' in num_str:
        is_decimal = True
        int_str, decimal_str = num_str.split('.')
        num_str = int_str
    else:
        is_decimal = False
    
    length = len(num_str)
    
    for part in partition(num_str, 9):
        part_num = int(part)
        if part_num != 0:
            text_list.extend(per_billions(part))
            bilis = (length - 1) // 9
            text_list.extend(['tỉ'] * bilis)
        length -= 9
    
    if is_decimal:
        text_list.append('phẩy')
        if decimal_str != '0':
            decimal_str = decimal_str.rstrip('0')
        if 2 <= len(decimal_str) <= 3:
            dec_int = int(decimal_str)
            if decimal_str[0] == '0' and 1 <= dec_int <= 99:
                text_list.append('không trăm')
            text_list.extend(per_thousand(dec_int))
        else:
            text_list.extend(per_digit(int(decimal_str)))
    text_list = list(filter(None, text_list))
    return ' '. join(text_list)