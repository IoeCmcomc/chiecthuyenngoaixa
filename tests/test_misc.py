# -*- coding: utf-8 -*-

from ctnx.misc import remove_diacritics, remove_tones, sep_tone_from_char, separate_tone, normalize_confusables, normalize
# from ctnx.constants import CONFUSABLE_CHAR_TRANS


def test_remove_diacritics():
    assert remove_diacritics(
        "Ở đời cái gì cũng thế, con người bản tính vốn lười biếng, đôi khi mình hãy cứ để cho mình rơi vào hoàn cảnh bị ép buộc phải làm, không khéo lại làm được một cái gì."
    ) == \
        "O doi cai gi cung the, con nguoi ban tinh von luoi bieng, doi khi minh hay cu de cho minh roi vao hoan canh bi ep buoc phai lam, khong kheo lai lam duoc mot cai gi."
    
    assert remove_diacritics("Nếu em có dỗi thì cũng chỉ muốn hờn dỗi mỗi anh thôi") == "Neu em co doi thi cung chi muon hon doi moi anh thoi"
    assert remove_diacritics("Em gửi chị báo cáo sự cố giải trình") == ("Em gui chi bao cao su co giai trinh")
    assert remove_diacritics("Anh ơi! Ba má em không có nhà, em đang coi quán, đến ngay đi anh, muộn lắm rồi. Tiện thể mua báo mới nhé, ở nhà toàn báo cũ... Mà thôi không cần mua báo đâu, em vừa mất kính rồi, không nhìn được nữa anh ơi, đến ngay đi... muộn lắm rồi.") == \
                            ("Anh oi! Ba ma em khong co nha, em dang coi quan, den ngay di anh, muon lam roi. Tien the mua bao moi nhe, o nha toan bao cu... Ma thoi khong can mua bao dau, em vua mat kinh roi, khong nhin duoc nua anh oi, den ngay di... muon lam roi.")
    assert remove_diacritics("Em đang thử đầm với đứa bạn") == ("Em dang thu dam voi dua ban")
    assert remove_diacritics("Cô mắng, em sợ quá, không muốn học nữa") == ("Co mang, em so qua, khong muon hoc nua")
    assert remove_diacritics("Cãi lộn gì thế?") == ("Cai lon gi the?")

def test_sep_tone_from_char():
    assert sep_tone_from_char('ế') == ('/', 'ê')
    assert sep_tone_from_char('ổ') == ('?', 'ô')
    assert sep_tone_from_char('ừ') == ('\\', 'ư')
    assert sep_tone_from_char('ị') == ('.', 'i')
    assert sep_tone_from_char('ã') == ('~', 'a')
    assert sep_tone_from_char('ô') == ('', 'ô')
    assert sep_tone_from_char('m') == ('', 'm')


def test_separate_tone():
    assert separate_tone('Nguyễn') == ('Nguyên', '~')
    assert separate_tone('và') == ('va', '\\')
    assert separate_tone('nghiêng') == ('nghiêng', '')


def test_remove_tones():
    assert remove_tones(
        "Có lẽ suốt một đời cầm máy ảnh chưa bao giờ tôi được thấy một cảnh \"đắt\" trời cho như vậy: trước mặt tôi là một bức tranh mực tầu của một danh họa thời cổ."
    ) == \
        "Co le suôt môt đơi câm may anh chưa bao giơ tôi đươc thây môt canh \"đăt\" trơi cho như vây: trươc măt tôi la môt bưc tranh mưc tâu cua môt danh hoa thơi cô."


def test_normalize_confusables():
    assert normalize_confusables(
        "Là đàn ôทɢ мà ρᏂảเ Ꭶốทɢ, cư 𝚡ử ทᏂư мột ᴄô ɢáเ suốt мột τᏂời ɢเɑท dài τᏂì tui ҜᏂôทɢ nghĩ ra ทổi") == \
        "Là đàn ông mà phải sống, cư xử như một cô gái suốt một thời gian dài thì tui không nghĩ ra nổi"
