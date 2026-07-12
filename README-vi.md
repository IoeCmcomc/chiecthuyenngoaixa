# chiecthuyenngoaixa

[![GitHub issues](https://img.shields.io/github/issues/IoeCmcomc/chiecthuyenngoaixa)](https://github.com/IoeCmcomc/chiecthuyenngoaixa/issues)
[![GitHub license](https://img.shields.io/github/license/IoeCmcomc/chiecthuyenngoaixa)](https://github.com/IoeCmcomc/chiecthuyenngoaixa/blob/master/LICENSE)
[![Documentation Status](https://readthedocs.org/projects/chiecthuyenngoaixa/badge/?version=latest)](https://chiecthuyenngoaixa.readthedocs.io/en/latest/?badge=latest)
![PyPI](https://img.shields.io/pypi/v/chiecthuyenngoaixa)
![PyPI - Downloads](https://img.shields.io/pypi/dm/chiecthuyenngoaixa)

[English](README.md "English version")

**chiecthuyenngoaixa** là một thư viện Python cung cấp các hàm và lớp để thực hiện các công việc _xử lí văn bản tiếng Việt_, chẳng hạn như loại bỏ dấu thanh, chuyển số thành chữ, sắp xếp câu, kiểm tra tính hợp lệ, v.v..

Thư viện được viết hoàn toàn bằng Python, không có phần phụ thuộc bên ngoài. Hỗ trợ Python 3.8 trở lên.

## Cài đặt

Chiecthuyenngoaixa có mặt trên
[PyPI](https://pypi.org/project/chiecthuyenngoaixa/). Mở dòng lệnh (terminal) hoặc
_Command Prompt_ (trên Windows) và chạy lệnh sau:

``` console
pip install chiecthuyenngoaixa
```

Nếu bạn đang sử dụng [Poetry](https://python-poetry.org/), hãy dùng lệnh này:

``` console
poetry add chiecthuyenngoaixa
```

Hoặc nếu bạn đang sử dụng [uv](https://docs.astral.sh/uv/):

``` console
uv add chiecthuyenngoaixa
```

## Cách dùng cơ bản

Thư viện giờ đây sẽ có thể dùng được dưới dạng mô đun `ctnx` (viết tắt của _chiecthuyenngoaixa_).

Một số hàm và lớp thường dùng có thể được nhập trực tiếp. Ví dụ:

- Để chuyển văn bản tiếng Việt thành văn bản chỉ gồm mã ASCII (bỏ hết dấu):

```python
>>> from ctnx import remove_diacritics
>>> remove_diacritics("Đàn ong thấy cái lon thì bu vào.")
'Dan ong thay cai lon thi bu vao.'
```

- Để chuyển số thành văn bản tiếng Việt:

```python
>>> from ctnx import num_to_words
>>> num_to_words(123456789021003.45)
'một trăm hai mươi ba nghìn bốn trăm năm mươi sáu tỉ bảy trăm tám mươi chín triệu không trăm hai mươi mốt nghìn không trăm linh ba phẩy bốn mươi lăm'
```

- Để sắp xếp các văn bản tiếng Việt:

```python
>>> from ctnx import vi_sort_key
>>> lines = ['Hà Nam', 'Hải Dương', 'Hà Nội', 'Hà Tĩnh', 'Hải Phòng', 'Hậu Giang', 'Hoà Bình', 'Hưng Yên', 'Hạ Long', 'Hà Giang', 'Điện Biên']
>>> sorted(lines, key=vi_sort_key)
['Điện Biên', 'Hà Giang', 'Hà Nam', 'Hà Nội', 'Hà Tĩnh', 'Hải Dương', 'Hải Phòng', 'Hạ Long', 'Hậu Giang', 'Hoà Bình', 'Hưng Yên']
```

Các hàm và lớp khác nằm ở các mô đun phụ khác nhau. Một số mô đun sẽ được giới thiệu qua ở dưới.

### Sắp xếp xâu tiếng Việt

Thứ tự sắp xếp dấu mặc định là _ngang, sắc, huyền, hỏi, ngã, nặng_. Nếu bạn
muốn một thứ tự khác, Hãy sử dụng lớp `ctnx.sort.ViCollator`
thay vì `ctnx.vi_sort_key`.

```python
>>> from ctnx.sort import ViCollator, vi_sort_key
>>> ds = ['mạn', 'mạ', 'màn', 'mà', 'man', 'ma', 'má', 'mán']
>>> sorted(ds, key=vi_sort_key)
['ma', 'man', 'má', 'mán', 'mà', 'màn', 'mạ', 'mạn']
>>> sorter = ViCollator(["\\", "?", "~", "/", "."])
>>> sorted(ds, key=sorter.key)
['mà', 'màn', 'má', 'mán', 'mạ', 'mạn', 'ma', 'man']
```

### Chuẩn hoá văn bản

Thư viện cung cấp hàm `ctnx.normalize_text` để thực hiện dọn dẹp và chuẩn hoá văn bản cơ bản.

```python
>>> from ctnx import normalize_text
>>> normalize_text("------- “Họa sĩ :𝕋𝕠̂ ℕ𝕘𝕠̣𝕔 𝕍𝕒̂𝕟 ”", strip_punctuation=True, do_normalize_confusables=True)
'Hoạ sĩ Tô Ngọc Vân'
```

Các hàm chuẩn hoá khác nằm trong mô đun `ctnx.misc`.

- Để chuyển một đoạn văn bản dễ gây nhầm lẫn (khó đọc) sang dạng bình thường:

```python
>>> from ctnx.misc import normalize_confusables
>>> normalize_confusables("𝕮𝖍𝖎ế𝖈 𝖙𝖍𝖚𝖞ề𝖓 𝖓𝖌𝖔à𝖎 𝖝𝖆")
'Chiếc thuyền ngoài xa'
```

- Để chuẩn hoá vị trí đặt dấu thanh về kiểu "mới" (_oà, oẻ, uý_) hoặc kiểu "cũ" (_òa, ỏe, úy_):

```python
>>> from ctnx.misc import normalize_tone_placement_new_style, normalize_tone_placement_old_style
>>> text = "mũi thuyền in một nét lòe nhoè vào bầu sương mù"
>>> normalize_tone_placement_new_style(text)
'mũi thuyền in một nét loè nhoè vào bầu sương mù'
>>> normalize_tone_placement_old_style(text)
'mũi thuyền in một nét lòe nhòe vào bầu sương mù'
```

- Để chuẩn hoá các ký tự i/y trong các từ tố như "hi, ki, li, mi, quy, si, ty, vi":

```python
>>> from ctnx.misc import IYNormalizer
>>> normer = IYNormalizer.from_preset_style("sinoviet_hklmqt_y")
>>> normer("Con lạy quí toà...")
'Con lạy quý toà...'
>>> IYNormalizer.from_preset_style("unified_i").replace("cái thằng trẻ con lạ kỳ nhất trần đời.")
'cái thằng trẻ con lạ kì nhất trần đời.'
```

### Kiểm tra hợp lệ (Validation)

- Để trích xuất thông tin từ mã số Căn cước công dân (CCCD) Việt Nam:

```python
>>> from ctnx import validation
>>> validation.is_valid_cccd("024192123456")
True
>>> validation.parse_cccd("024192123456")
CccdResult(id='123456', is_male=False, birth_year=1992, birth_country='vn', birth_province='Bắc Giang')
```

### Thao tác với âm tiết

_chiecthuyenngoaixa_ cung cấp lớp `syllable.Syllable` để làm việc với các âm tiết tiếng Việt.

- Để thao tác với các âm tiết tiếng Việt:

```python
>>> from ctnx.syllable import Syllable
>>> text = "ba ngày một trận nhẹ năm ngày một trận nặng"
>>> a = [Syllable.from_string(x) for x in text.split(' ')]
>>> a
[Syllable(b, a, ), Syllable(ng, ay, , \), Syllable(m, ô, t, .), Syllable(tr, â, n, .), Syllable(nh, e, , .), Syllable(n, ă, m), Syllable(ng, ay, , \), Syllable(m, ô, t, .), Syllable(tr, â, n, .), Syllable(n, ă, ng, .)]
>>> for syll in a:
...     syll.onset = 'nh'
...
>>> a
[Syllable(nh, a, ), Syllable(nh, ay, , \), Syllable(nh, ô, t, .), Syllable(nh, â, n, .), Syllable(nh, e, , .), Syllable(nh, ă, m), Syllable(nh, ay, , \), Syllable(nh, ô, t, .), Syllable(nh, â, n, .), Syllable(nh, ă, ng, .)]
>>> ' '.join(str(x) for x in a)
'nha nhày nhột nhận nhẹ nhăm nhày nhột nhận nhặng'
```

### Khác

- Để trích xuất thanh điệu từ một âm tiết hoặc văn bản tiếng Việt:

```python
>>> from ctnx.misc import separate_tone
>>> separate_tone("Đẩu")
('Đâu', '?')
>>> toneNames = {'': 'thanh', '/': 'sắc', '\\': 'huyền', '?': 'hỏi', '~': 'ngã', '.': 'nặng'}
>>> ' '.join(toneNames[separate_tone(syll)[1]] for syll in "Tôi thầm cảm ơn Đẩu đã giữ mình ở nán lại".split(' '))
'thanh huyền hỏi thanh hỏi ngã ngã huyền hỏi sắc nặng'
```

Để biết thêm cách sử dụng, hãy xem tài liệu (tiếng Anh) nằm ở [chiecthuyenngoaixa.readthedocs.io](https://chiecthuyenngoaixa.readthedocs.io/en/latest/).
