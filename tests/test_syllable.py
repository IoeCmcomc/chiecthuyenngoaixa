# -*- coding: utf-8 -*-

import pytest

from ctnx.syllable import Syllable, NewStyleTonePlacer

to_string_dataset = "Do bạch kim rất quý sẽ để lắp vô xương".split()

def test_Syllable_eq():
    assert Syllable('x', 'i', 'n') == Syllable('x', 'i', 'n')

def test_from_string():
    assert Syllable.from_string('xin') == Syllable('x', 'i', 'n')
    assert Syllable.from_string('Việt') == Syllable('v', 'iê', 't', '.')
    assert Syllable.from_string('giá') == Syllable('gi', 'a', '', '/')
    assert Syllable.from_string('nghỉ') == Syllable('ngh', 'i', '', '?')
    assert Syllable.from_string('nguồn') == Syllable('ng', 'uô', 'n', '\\')
    assert Syllable.from_string('xoong') == Syllable('x', 'oo', 'ng', '')
    assert Syllable.from_string('khuya') == Syllable('kh', 'uya', '', '')
    assert Syllable.from_string('cứu') == Syllable('c', 'ưu', '', '/')
    assert Syllable.from_string('đẽo') == Syllable('đ', 'eo', '', '~')
    assert Syllable.from_string('ăn') == Syllable('', 'ă', 'n', '')
    assert Syllable.from_string('nghiêng') == Syllable('ngh', 'iê', 'ng', '')
    assert Syllable.from_string('mía') == Syllable('m', 'ia', '', '/')
    assert Syllable.from_string('yểng') == Syllable('', 'yê', 'ng', '?')
    assert Syllable.from_string('iêu') == Syllable('', 'iêu', '', '')
    assert Syllable.from_string('quà') == Syllable('qu', 'a', '', '\\')
    assert Syllable.from_string('loá') == Syllable('l', 'oa', '', '/')
    assert Syllable.from_string('quện') == Syllable('qu', 'ê', 'n', '.')
    assert Syllable.from_string('thuở') == Syllable('th', 'uơ', '', '?')
    assert Syllable.from_string('ế') == Syllable('', 'ê', '', '/')
    assert Syllable.from_string('Huỳnh') == Syllable('h', 'uy', 'nh', '\\')
    assert Syllable.from_string('tuýp') == Syllable('t', 'uy', 'p', '/')
    assert Syllable.from_string('quớt') == Syllable('qu', 'ơ', 't', '/')
    
def test_from_string_AUTO_CORRECT_disabled():
    Syllable.AUTO_CORRECT = False
    assert Syllable.from_string('Huỳnh') == Syllable('h', 'uy', 'nh', '\\')
    assert Syllable.from_string('quýnh') == Syllable('qu', 'y', 'nh', '/')
    Syllable.AUTO_CORRECT = True

def test_to_string():
    assert Syllable.tone_placer == NewStyleTonePlacer
    assert str(Syllable.from_string('Hóa')) == 'hoá'

@pytest.mark.parametrize("string", to_string_dataset)
def test_to_string_batch(string):
    assert str(Syllable.from_string(string)) == string.lower()