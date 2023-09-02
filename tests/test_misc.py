# -*- coding: utf-8 -*-

from ctnx.misc import remove_diacritics, remove_tones, sep_tone_from_char, separate_tone, normalize_confusables, normalize
from ctnx.constants import CONFUSABLE_CHAR_TRANS


def test_remove_diacritics():
    assert remove_diacritics(
        "Ở đời cái gì cũng thế, con người bản tính vốn lười biếng, đôi khi mình hãy cứ để cho mình rơi vào hoàn cảnh bị ép buộc phải làm, không khéo lại làm được một cái gì."
    ) == \
        "O doi cai gi cung the, con nguoi ban tinh von luoi bieng, doi khi minh hay cu de cho minh roi vao hoan canh bi ep buoc phai lam, khong kheo lai lam duoc mot cai gi."


def test_sep_tone_from_char():
    assert sep_tone_from_char('ế') == ('/', 'ê')


def test_separate_tone():
    assert separate_tone('Nguyễn') == ('Nguyên', '~')


def test_remove_tones():
    assert remove_tones(
        "Có lẽ suốt một đời cầm máy ảnh chưa bao giờ tôi được thấy một cảnh \"đắt\" trời cho như vậy: trước mặt tôi là một bức tranh mực tầu của một danh họa thời cổ."
    ) == \
        "Co le suôt môt đơi câm may anh chưa bao giơ tôi đươc thây môt canh \"đăt\" trơi cho như vây: trươc măt tôi la môt bưc tranh mưc tâu cua môt danh hoa thơi cô."


def test_normalize_confusables():
    assert normalize_confusables(
        "Là đàn ôทɢ мà ρᏂảเ Ꭶốทɢ, cư 𝚡ử ทᏂư мột ᴄô ɢáเ suốt мột τᏂời ɢเɑท dài τᏂì tui ҜᏂôทɢ nghĩ ra ทổi") == \
        "Là đàn ông mà phải sống, cư xử như một cô gái suốt một thời gian dài thì tui không nghĩ ra nổi"
