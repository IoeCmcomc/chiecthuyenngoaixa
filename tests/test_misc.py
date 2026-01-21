# -*- coding: utf-8 -*-

import logging
import pytest
import random

from ctnx.misc import remove_diacritics, remove_tones, sep_tone_from_char, separate_tone, normalize_confusables, normalize_tone_placement_new_style, normalize_tone_placement_old_style, IYNormalizer
from ctnx.syllable import Syllable, NewStyleTonePlacer, OldStyleTonePlacer


def test_remove_diacritics():
    assert remove_diacritics(
        "Ở đời cái gì cũng thế, con người bản tính vốn lười biếng, đôi khi mình hãy cứ để cho mình rơi vào hoàn cảnh bị ép buộc phải làm, không khéo lại làm được một cái gì."
    ) == \
        "O doi cai gi cung the, con nguoi ban tinh von luoi bieng, doi khi minh hay cu de cho minh roi vao hoan canh bi ep buoc phai lam, khong kheo lai lam duoc mot cai gi."

    assert remove_diacritics(
        "Nếu em có dỗi thì cũng chỉ muốn hờn dỗi mỗi anh thôi") == "Neu em co doi thi cung chi muon hon doi moi anh thoi"
    assert remove_diacritics("Em gửi chị báo cáo sự cố giải trình") == (
        "Em gui chi bao cao su co giai trinh")
    assert remove_diacritics("Anh ơi! Ba má em không có nhà, em đang coi quán, đến ngay đi anh, muộn lắm rồi. Tiện thể mua báo mới nhé, ở nhà toàn báo cũ... Mà thôi không cần mua báo đâu, em vừa mất kính rồi, không nhìn được nữa anh ơi, đến ngay đi... muộn lắm rồi.") == \
                            ("Anh oi! Ba ma em khong co nha, em dang coi quan, den ngay di anh, muon lam roi. Tien the mua bao moi nhe, o nha toan bao cu... Ma thoi khong can mua bao dau, em vua mat kinh roi, khong nhin duoc nua anh oi, den ngay di... muon lam roi.")
    assert remove_diacritics("Em đang thử đầm với đứa bạn") == (
        "Em dang thu dam voi dua ban")
    assert remove_diacritics("Cô mắng, em sợ quá, không muốn học nữa") == (
        "Co mang, em so qua, khong muon hoc nua")
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
    assert normalize_confusables("Bằпg cách ɴày, ᴄó ɫһể xả sạᴄһ 𝘷à ᴛιếᴛ kiệm ɴướᴄ Һơᶇ.") == \
        "Bằng cách này, có thể xả sạch và tiết kiệm nước hơn."
    assert normalize_confusables("“Tôi тɾả điểm ϲհσ mấy người, mấy người ϲó тɾả bố ϲհσ tôi đượϲ кհôռɢ”") == \
        "\"Tôi trả điểm cho mấy người, mấy người có trả bố cho tôi được không\""
    assert normalize_confusables("Mấy ɑι như HĿV Mɑι Đứͼ Chυnɡ, U80 vẫn ‘độι nắnɡ mưɑ’ mυốn bảo vệ HCV SEA Gɑmes, mơ ƙì тíͼh vĩ đạι ở World Cυp") == \
        "Mấy ai như HLV Mai Đức Chung, U80 vẫn 'đội nắng mưa' muốn bảo vệ HCV SEA Games, mơ kì tích vĩ đại ở World Cup"
    assert normalize_confusables("Cô ɢáᎥ тɾẻ đột ռᏂᎥên biếɳ ᏂìɳᏂ ǥiữa đường, cởi sạch đồ ngủ để thay bộ váy ѕexy, ở ռᏂà cháu ngoαռ lắm ռᏂưռɢ ít khi ở ռᏂà") == \
        "Cô gái trẻ đột nhiên biến hình giữa đường, cởi sạch đồ ngủ để thay bộ váy sexy, ở nhà cháu ngoan lắm nhưng ít khi ở nhà"

    assert normalize_confusables("""ᴛìᴍ ɴɢườɪ ɢõ đề ᴄươɴɢ
𝟻𝟶ᴋ  / 𝟷 ʙàɪ ᴛɪếɴɢ ᴠɪệᴛ
𝟷𝟶𝟶ᴋ  / 𝟷 ʙàɪ ᴛɪếɴɢ ᴀɴʜ
ᴋ ɢɪớɪ ʜạɴ ʙàɪ ᴄó ᴛʜể ᴄʜọɴ ʙàɪ để ʟàᴍ
ᴄᴠ ᴄó ᴛʜậᴛ ɴɢʜɪêᴍ ᴛúᴄ 𝟷𝟶𝟶%
ʟàᴍ ᴛʀêɴ đᴛʜᴏᴀɪ/ʟᴀᴘᴛᴏᴘ đềᴜ đượᴄ
ʟươ-ɴɢ ɴʜậɴ ᴛʜᴇᴏ ʙàɪ""") == """tìm người gõ đề cương
50k  / 1 bài tiếng việt
100k  / 1 bài tiếng anh
k giới hạn bài có thể chọn bài để làm
cv có thật nghiêm túc 100%
làm trên đthoai/laptop đều được
lươ-ng nhận theo bài"""

    assert normalize_confusables("""𝘉𝘢̆̀𝘯𝘨 𝘓𝘢́𝘪 𝘟𝘦 𝘛𝘰𝘢̀𝘯 𝘘𝘶𝘰̂́𝘤 (63 𝘵𝘪̉𝘯𝘩 𝘵𝘩𝘢̀𝘯𝘩) 5-10 𝘯𝘨𝘢̀𝘺 𝘯𝘩𝘢̣̂𝘯
𝘉𝘈̆̀𝘕𝘎 𝘗𝘏𝘖̂𝘐 𝘊𝘏𝘜𝘈̂̉𝘕 𝘚𝘖𝘐 𝘙𝘖̣𝘐 𝘛𝘏𝘖𝘈̉𝘐 𝘔𝘈́𝘐
✅𝘖𝘵𝘰̂: 𝘉1-𝘉2-𝘊
✅𝘟𝘦 𝘮𝘢́𝘺: 𝘈1 - 𝘈2 - 𝘈3
✅𝘕𝘢̂𝘯𝘨 𝘏𝘢̣𝘯𝘨 : 𝘋-𝘌-𝘍𝘊
👉𝘈𝘯 𝘛𝘰𝘢̀𝘯 - 𝘕𝘩𝘢𝘯𝘩 𝘊𝘩𝘰́𝘯𝘨 - 𝘉𝘢̉𝘰 𝘔𝘢̣̂𝘵 𝘵𝘩𝘰̂𝘯𝘨 𝘵𝘪𝘯 𝘒𝘩𝘢́𝘤𝘩 𝘏𝘢̀𝘯𝘨. 𝘊𝘰́ 𝘩𝘰̂̀ 𝘴𝘰̛ 𝘨𝘰̂́𝘤 + 𝘤𝘩𝘶̛́𝘯𝘨 𝘤𝘩𝘪̉ đ𝘢̀𝘰 𝘵𝘢̣𝘰 𝘬𝘦̀𝘮 𝘵𝘩𝘦𝘰
👉𝘎𝘪𝘢̂́𝘺 𝘱𝘩𝘦́𝘱 𝘭𝘢́𝘪 𝘹𝘦 𝘤𝘰́ 𝘮𝘢̃ 𝘘𝘙 đ𝘪𝘦̣̂𝘯 𝘵𝘶̛̉ 𝘤𝘩𝘰̂́𝘯𝘨 𝘨𝘪𝘢̉
💥 𝘏𝘰̂̃ 𝘵𝘳𝘰̛̣ 𝘬𝘩𝘰̂𝘯𝘨 𝘤𝘢̂̀𝘯 đ𝘪 𝘵𝘩𝘪, 𝘤𝘰́ 𝘯𝘨𝘶̛𝘰̛̀𝘪 𝘵𝘩𝘪 𝘩𝘰̣̂ 𝘷𝘢̀ 𝘣𝘢𝘰 đ𝘢̣̂𝘶
💥 𝘔𝘪𝘦̂̃𝘯 𝘱𝘩𝘪́ 𝘨𝘪𝘢𝘰 𝘩𝘢̀𝘯𝘨 𝘵𝘢̣̂𝘯 𝘵𝘢𝘺""") == """Bằng Lái Xe Toàn Quốc (63 tỉnh thành) 5-10 ngày nhận
BẰNG PHÔI CHUẨN SOI RỌI THOẢI MÁI
✅Otô: B1-B2-C
✅Xe máy: A1 - A2 - A3
✅Nâng Hạng : D-E-FC
👉An Toàn - Nhanh Chóng - Bảo Mật thông tin Khách Hàng. Có hồ sơ gốc + chứng chỉ đào tạo kèm theo
👉Giấy phép lái xe có mã QR điện tử chống giả
💥 Hỗ trợ không cần đi thi, có người thi hộ và bao đậu
💥 Miễn phí giao hàng tận tay"""

    assert(normalize_confusables("""ʜỗ ᴛʀợ ʟàᴍ ɢɪấʏ ᴘʜéᴘ ʟáɪ xᴇ ᴋʜôɴɢ ᴄầɴ đɪ ᴛʜɪ- sẽ ᴄó ɴʜâɴ ᴠɪêɴ ᴛʜɪ ʜộ
Ưᴜ ᴛɪêɴ ᴄʜᴏ ᴄôɴɢ ɴʜâɴ, ɴɢườɪ ᴋʜôɴɢ ᴄó ᴛʜờɪ ɢɪᴀɴ ᴛʜɪ
#ʙʟx xᴇ ᴍáʏ: ᴀ𝟷, ᴀ𝟸, ᴀ𝟹
Ô ᴛô : ʙ𝟷, ʙ𝟸 , ᴄ, ᴅ, ᴇ, ғᴄ,...
ʙằɴ.ɢ ᴄᴏ́ ʜồ sơ ɢốᴄ ʜợᴘ ʟệ, ᴅùɴɢ ᴘʜầɴ ᴍềᴍ ᴄʜᴜʏêɴ ᴅụɴɢ để ǫᴜéᴛ
ᴍã ǫʀ ᴋɪểᴍ ᴛʀᴀ ᴛʜậᴛ ɢɪả
ᴄó ɴɢườɪ ᴛʜɪ ʜộ ᴛừ ᴀ-ᴢ
Đượᴄ ᴋɪểᴍ ᴛʀᴀ ᴛʀướᴄ ᴋʜɪ ᴛʜᴀɴʜ ᴛᴏáɴ - ᴅùɴɢ ᴘʜầɴ ᴍềᴍ ᴄʜᴜʏêɴ ᴅụɴɢ ᴋɪểᴍ ᴛʀᴀ
ᴋʜôɴɢ ɴʜậɴ ᴄọᴄ- ᴋʜôɴɢ ᴛʜᴜ ᴘʜụ ᴘʜí
ᴍɪễɴ ᴘʜí ɢɪᴀᴏ ʙ.ằ.ɴɢ ᴛᴏàɴ ǫᴜốᴄ
""") == """hỗ trợ làm giấy phép lái xe không cần đi thi- sẽ có nhân viên thi hộ
Ưu tiên cho công nhân, người không có thời gian thi
#blx xe máy: a1, a2, a3
Ô tô : b1, b2 , c, d, e, fc,...
bằn.g có hồ sơ gốc hợp lệ, dùng phần mềm chuyên dụng để quét
mã qr kiểm tra thật giả
có người thi hộ từ a-z
Được kiểm tra trước khi thanh toán - dùng phần mềm chuyên dụng kiểm tra
không nhận cọc- không thu phụ phí
miễn phí giao b.ằ.ng toàn quốc
""")
    
    assert normalize_confusables("""Dịch Vụ 𝘽ằng Cấp 
☑️ Tất cả các trường học trên toàn quốc. 
- Đ𝑎̣𝑖 𝐻𝑜̣𝑐 
- 𝐶𝑎𝑜 Đ𝑎̆̉𝑛𝑔 
- 𝑇𝑟𝑢𝑛𝑔 𝐶𝑎̂́𝑝 
- 𝐶𝑎̂́𝑝 3 - 𝑇𝐻𝑃𝑇 - 𝑇𝐻𝐶𝑆
👍 Giao Hàng Tận Nơi - #Không_Cần_Đặt_Cọc 
- Tem - Mộc - Chữ Ký chuẩn B.G.D 
- Bao công chứng toàn quốc 
- Bao xin việc, nhập học, xuất khẩu lao động.
💥 KIỂM TRA OK MỚI THANH TOÁN TIỀN 💥
""") == """Dịch Vụ Bằng Cấp 
☑️ Tất cả các trường học trên toàn quốc. 
- Đại Học 
- Cao Đẳng 
- Trung Cấp 
- Cấp 3 - THPT - THCS
👍 Giao Hàng Tận Nơi - #Không_Cần_Đặt_Cọc 
- Tem - Mộc - Chữ Ký chuẩn B.G.D 
- Bao công chứng toàn quốc 
- Bao xin việc, nhập học, xuất khẩu lao động.
💥 KIỂM TRA 0K MỚI THANH T0ÁN TIỀN 💥
"""

def test_normalize_tone_placement_new_style():
    assert normalize_tone_placement_new_style(
        "PHÓA PHÒA PHỎA PHÕA phọa, PHÓE PHÒE PHỎE PHÕE phọe, ÚY ÙY ỦY ŨY ụy, XÓONG XÒONG XỎONG XÕONG xọong, CỐÔNG CỒÔNG CỔÔNG CỖÔNG cộông"
        ) == (
        "PHOÁ PHOÀ PHOẢ PHOÃ phoạ, PHOÉ PHOÈ PHOẺ PHOẼ phoẹ, UÝ UỲ UỶ UỸ uỵ, XOÓNG XOÒNG XOỎNG XOÕNG xoọng, CÔỐNG CÔỒNG CÔỔNG CÔỖNG côộng"
        )

def test_normalize_tone_placement_old_style():
    assert normalize_tone_placement_old_style(
        "PHOÁ PHOÀ PHOẢ PHOÃ phoạ, PHOÉ PHOÈ PHOẺ PHOẼ phoẹ, UÝ UỲ UỶ UỸ uỵ, XOÓNG XOÒNG XOỎNG XOÕNG xoọng, CÔỐNG CÔỒNG CÔỔNG CÔỖNG côộng"
        ) == (
        "PHÓA PHÒA PHỎA PHÕA phọa, PHÓE PHÒE PHỎE PHÕE phọe, ÚY ÙY ỦY ŨY ụy, XÓONG XÒONG XỎONG XÕONG xọong, CỐÔNG CỒÔNG CỔÔNG CỖÔNG cộông"
        )

def generate_random_syllables(n=10):
    Syllable.tone_placer = OldStyleTonePlacer
    string = ' '.join(str(Syllable.from_string(random.choice(Syllable.ONSETS) + random.choice((
        'uế', 'uề', 'uể', 'uễ', 'uệ',
        'óa', 'òa', 'ỏa', 'ủy', 'ũy', 'ụy', 'òe', 'ỏe', 'õe', 'ủa',
        'oả', 'oạ', 'uý', 'uỳ', 'oẽ', 'oẹ'))))
        + random.choice(('', '', '', '', '', ',', '.', ';', '?', ':')) for _ in range(n))
    Syllable.tone_placer = NewStyleTonePlacer
    return string

@pytest.fixture
def dataset_tone_normalization():
    random.seed(67)

    data = generate_random_syllables(50000)
    # print(data)
    return data

def test_new_style_tone_normalize(benchmark, dataset_tone_normalization):
    result = benchmark(normalize_tone_placement_new_style, dataset_tone_normalization)
    assert len(result) == len(dataset_tone_normalization)

def test_i_y_normalizer():
    normalizer = IYNormalizer()
    assert normalizer("kiếm lời") == "kiếm lời"
    assert normalizer("Í em sao") == "Ý em sao"
    assert normalizer("vì sao") == "vì sao"
    assert normalizer(
        "HI VỌNG quí ca sĩ Ly Ly hát í tứ mĩ miều, li kỳ, vì diệu"
        ) == (
        "HY VỌNG quý ca sĩ Ly Ly hát ý tứ mỹ miều, ly kỳ, vì diệu"
        )

def test_i_y_normalizer_sinoviet_heuristic():
    normalizer_enabled = IYNormalizer(use_sinoviet_heuristic=True, i_override_list=[])
    assert normalizer_enabled(
        "hỳ hì, quản lí các cá nhân và công ti mĩ phẩm lỳ lợm, cố í trục lợi hàng tỉ đồng, vi phạm qui định cực kỳ tinh vy"
    ) == (
        "hì hì, quản lý các cá nhân và công ty mỹ phẩm lì lợm, cố ý trục lợi hàng tỷ đồng, vi phạm quy định cực kỳ tinh vi"
    )
    normalizer_disabled = IYNormalizer(use_sinoviet_heuristic=False, i_override_list=[])
    assert normalizer_disabled(
        "hỳ hì, quản lí các cá nhân và công ti mĩ phẩm lỳ lợm, cố í trục lợi hàng tỉ đồng, vi phạm qui định cực kỳ tinh vy"
    ) == (
        "hỳ hỳ, quản lý các cá nhân và công ty mỹ phẩm lỳ lợm, cố ý trục lợi hàng tỷ đồng, vi phạm quy định cực kỳ tinh vi"
    )

# Tests are genarated by Gemini 3, fixed by me
TEST_I_Y_NORMALIZER_DEFAULT_I_EXCEPTIONS_CASES = [
    (
        "Cậu ấy hỳ hục cả buổi để kỳ cọ cái sàn đen sỳ và hôi sỳ cho thật kỹ càng và tỷ mỷ.",
        "Cậu ấy hì hục cả buổi để kì cọ cái sàn đen sì và hôi sì cho thật kĩ càng và tỉ mỉ."
    ),
    (
        "Lão nhà giàu ky bo, suốt ngày lo ky cóp và tính toán chi ly từng đồng, dù trong tay có bạc tỷ và hứa sẽ đãi ngộ hậu hỹ.",
        "Lão nhà giàu ki bo, suốt ngày lo ki cóp và tính toán chi li từng đồng, dù trong tay có bạc tỉ và hứa sẽ đãi ngộ hậu hĩ."
    ),
    (
        "Bà chủ cân một ky-lô-gam bột mỳ và khoai mỳ, thêm chút mỳ chính, không sai một my ly hay một tý ty nào.",
        "Bà chủ cân một ki-lô-gam bột mì và khoai mì, thêm chút mì chính, không sai một mi li hay một tí ti nào."
    ),
    (
        "Mọi người sì sụp ăn bát mỳ sợi nóng hổi.",
        "Mọi người sì sụp ăn bát mì sợi nóng hổi."
    ),
    (
        "Cô gái trông vẻ ngoài cù mỳ, đôi mi mắt cong, nhưng thực ra rất lỳ lợm và kỹ tính, lúc nào cũng cười hỷ hả với đôi mắt ty hý.",
        "Cô gái trông vẻ ngoài cù mì, đôi mi mắt cong, nhưng thực ra rất lì lợm và kĩ tính, lúc nào cũng cười hỉ hả với đôi mắt ti hí."
    ),
    (
        "Thằng bé hý hoáy sửa đồ chơi, chốc chốc lại tý toáy tỳ tay lên bàn, miệng thì thầm tỷ tê trong tiếng mưa rơi tý tách.",
        "Thằng bé hí hoáy sửa đồ chơi, chốc chốc lại tí toáy tì tay lên bàn, miệng thì thầm tỉ tê trong tiếng mưa rơi tí tách."
    ),
    (
        "Nó cười hy hy rồi lại hỳ hỳ, vẻ mặt hý hửng và hý hởn như vừa nhận được quà.",
        "Nó cười hi hi rồi lại hì hì, vẻ mặt hí hửng và hí hởn như vừa nhận được quà."
    ),
    (
        "Chiếc va ly cũ kỹ của cụ kỵ để lại nằm dưới gốc cây sy, bên trong là cuốn vở kẻ ô ly đã nhẵn lỳ theo thời gian.",
        "Chiếc va li cũ kĩ của cụ kị để lại nằm dưới gốc cây si, bên trong là cuốn vở kẻ ô li đã nhẵn lì theo thời gian."
    ),
    (
        "Đừng tỵ nạnh chuyện lỳ xì ít hay nhiều, nó chỉ trả lời lý nhí rồi quay sang hỷ mũi ở góc ky-ốt.",
        "Đừng tị nạnh chuyện lì xì ít hay nhiều, nó chỉ trả lời lí nhí rồi quay sang hỉ mũi ở góc ki-ốt."
    ),
    (
        "Tấm biển làm bằng my-ca được gia cố bởi khung ty-tan và hợp chất sy-lic.",
        "Tấm biển làm bằng mi-ca được gia cố bởi khung ti-tan và hợp chất si-lic."
    )
]

@pytest.mark.parametrize("input, output", TEST_I_Y_NORMALIZER_DEFAULT_I_EXCEPTIONS_CASES)
def test_i_y_normalizer_default_i_exceptions(input, output):
    normalizer = IYNormalizer(use_sinoviet_heuristic=False)
    assert normalizer(input) == output

# Tests are genarated by Gemini 3, fixed by me
TEST_I_Y_NORMALIZER_PRESET_INPUT = "bác sĩ gan lì dán mí và quí mến người hì hục lập kỉ lục ở công ti hùng vĩ."
TEST_I_Y_NORMALIZER_PRESETS = (
    ("i", "bác sĩ gan lì dán mí và quí mến người hì hục lập kỉ lục ở công ti hùng vĩ."),
    ("unified_i", "bác sĩ gan lì dán mí và quý mến người hì hục lập kỉ lục ở công ti hùng vĩ."),
    ("sinoviet_hklmqstv_y", "bác sỹ gan lì dán mí và quý mến người hì hục lập kỷ lục ở công ty hùng vỹ."),
    ("hklmqstv_y", "bác sỹ gan lỳ dán mý và quý mến người hì hục lập kỷ lục ở công ty hùng vỹ."),
    ("sinoviet_hklmqst_y", "bác sỹ gan lì dán mí và quý mến người hì hục lập kỷ lục ở công ty hùng vĩ."),
    ("hklmqst_y", "bác sỹ gan lỳ dán mý và quý mến người hì hục lập kỷ lục ở công ty hùng vĩ."),
    ("sinoviet_hklmqt_y", "bác sĩ gan lì dán mí và quý mến người hì hục lập kỷ lục ở công ty hùng vĩ."),
    ("hklmqt_y", "bác sĩ gan lỳ dán mý và quý mến người hì hục lập kỷ lục ở công ty hùng vĩ."),
)

@pytest.mark.parametrize("preset, output", TEST_I_Y_NORMALIZER_PRESETS)
def test_i_y_normalizer_preset(preset, output):
    normalizer = IYNormalizer.from_preset_style(preset)
    assert normalizer(TEST_I_Y_NORMALIZER_PRESET_INPUT) == output