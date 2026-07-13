# chiecthuyenngoaixa

[![GitHub issues](https://img.shields.io/github/issues/IoeCmcomc/chiecthuyenngoaixa)](https://github.com/IoeCmcomc/chiecthuyenngoaixa/issues)
[![GitHub license](https://img.shields.io/github/license/IoeCmcomc/chiecthuyenngoaixa)](https://github.com/IoeCmcomc/chiecthuyenngoaixa/blob/master/LICENSE)
[![Documentation Status](https://readthedocs.org/projects/chiecthuyenngoaixa/badge/?version=latest)](https://chiecthuyenngoaixa.readthedocs.io/en/latest/?badge=latest)
![PyPI](https://img.shields.io/pypi/v/chiecthuyenngoaixa)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/chiecthuyenngoaixa?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/chiecthuyenngoaixa)

[Tiếng Việt](README-vi.md "Vietnamese version")

**chiecthuyenngoaixa** is a Python library which provides functions and
classes for various tasks in _processing Vietnamese texts_, such as
removing diacritics, converting numbers to words, sorting strings,
validations and more.

This library is written on pure Python with no dependencies. Python 3.8
and above is supported.

## Installation

Chiecthuyenngoaixa is available on
[PyPI](https://pypi.org/project/chiecthuyenngoaixa/). Open a terminal or
_Command Prompt_ (on Windows) and run the following command:

``` console
pip install chiecthuyenngoaixa
```

If you are using [Poetry](https://python-poetry.org/), use this instead:

``` console
poetry add chiecthuyenngoaixa
```

Or if you are using [uv](https://docs.astral.sh/uv/):

``` console
uv add chiecthuyenngoaixa
```

## Basic usage

The library will now be available as `ctnx` module (abbreviation of
_chiecthuyenngoaixa_).

Some commonly used functions and classes can be imported directly. For
example:

- To convert Vietnamese text to ASCII-only text:

```python
>>> from ctnx import remove_diacritics
>>> remove_diacritics("Đàn ong thấy cái lon thì bu vào.")
'Dan ong thay cai lon thi bu vao.'
```

- To convert a number to Vietnamese text:

```python
>>> from ctnx import num_to_words
>>> num_to_words(123456789021003.45)
'một trăm hai mươi ba nghìn bốn trăm năm mươi sáu tỉ bảy trăm tám mươi chín triệu không trăm hai mươi mốt nghìn không trăm linh ba phẩy bốn mươi lăm'
```

- To sort Vietnamese texts:

```python
>>> from ctnx import vi_sort_key
>>> lines = ['Hà Nam', 'Hải Dương', 'Hà Nội', 'Hà Tĩnh', 'Hải Phòng', 'Hậu Giang', 'Hoà Bình', 'Hưng Yên', 'Hạ Long', 'Hà Giang', 'Điện Biên']
>>> sorted(lines, key=vi_sort_key)
['Điện Biên', 'Hà Giang', 'Hà Nam', 'Hà Nội', 'Hà Tĩnh', 'Hải Dương', 'Hải Phòng', 'Hạ Long', 'Hậu Giang', 'Hoà Bình', 'Hưng Yên']
```

Other functions and classes are put into separate sub-modules. Some modules are introduced more below.

### Sorting Vietnamese strings

The default tone-sorting order is _ngang, sắc, huyền, hỏi, ngã, nặng_. If you
prefers a different order, you should use `ctnx.sort.ViCollator`
instead of `ctnx.vi_sort_key`.

```python
>>> from ctnx.sort import ViCollator, vi_sort_key
>>> ds = ['mạn', 'mạ', 'màn', 'mà', 'man', 'ma', 'má', 'mán']
>>> sorted(ds, key=vi_sort_key)
['ma', 'man', 'má', 'mán', 'mà', 'màn', 'mạ', 'mạn']
>>> sorter = ViCollator(["\\", "?", "~", "/", "."])
>>> sorted(ds, key=sorter.key)
['mà', 'màn', 'má', 'mán', 'mạ', 'mạn', 'ma', 'man']
```

### Normalizing text

The library provides `ctnx.normalize_text` to do basic text cleaning and normalization.

```python
>>> from ctnx import normalize_text
>>> normalize_text("------- “Họa sĩ :𝕋𝕠̂ ℕ𝕘𝕠̣𝕔 𝕍𝕒̂𝕟 ”", strip_punctuation=True, do_normalize_confusables=True)
'Hoạ sĩ Tô Ngọc Vân'
```

Other normalization functions live in the `ctnx.misc` module.

- To convert a likely confusing text of Vietnamese to the normal text:

```python
>>> from ctnx.misc import normalize_confusables
>>> normalize_confusables("𝕮𝖍𝖎ế𝖈 𝖙𝖍𝖚𝖞ề𝖓 𝖓𝖌𝖔à𝖎 𝖝𝖆")
'Chiếc thuyền ngoài xa'
```

- To normalize tone characters to either the "new" style (_oà, oẻ, uý_) or the "old" style (_òa, ỏe, úy_):

```python
>>> from ctnx.misc import normalize_tone_placement_new_style, normalize_tone_placement_old_style
>>> text = "mũi thuyền in một nét lòe nhoè vào bầu sương mù"
>>> normalize_tone_placement_new_style(text)
'mũi thuyền in một nét loè nhoè vào bầu sương mù'
>>> normalize_tone_placement_old_style(text)
'mũi thuyền in một nét lòe nhòe vào bầu sương mù'
```

- To normalize i/y characters in tokens like "hi, ki, li, mi, quy, si, ty, vi":

```python
>>> from ctnx.misc import IYNormalizer
>>> normer = IYNormalizer.from_preset_style("sinoviet_hklmqt_y")
>>> normer("Con lạy quí toà...")
'Con lạy quý toà...'
>>> IYNormalizer.from_preset_style("unified_i").replace("cái thằng trẻ con lạ kỳ nhất trần đời.")
'cái thằng trẻ con lạ kì nhất trần đời.'
```

### Validation

- To extract information from a Vietnamese National Citizen ID (_Căn cước công dân_) number:

```python
>>> from ctnx import validation
>>> validation.is_valid_cccd("024192123456")
True
>>> validation.parse_cccd("024192123456")
CccdResult(id='123456', is_male=False, birth_year=1992, birth_country='vn', birth_province='Bắc Giang')
```

### Manipulating syllable

_chiecthuyenngoaixa_ provides the `syllable.Syllable` class to deal with
Vietnamese syllables.

- To manipulate Vietnamese syllables:

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

### Other

- To extract tones from a Vietnamese syllable or text:

```python
>>> from ctnx.misc import separate_tone
>>> separate_tone("Đẩu")
('Đâu', '?')
>>> toneNames = {'': 'thanh', '/': 'sắc', '\\': 'huyền', '?': 'hỏi', '~': 'ngã', '.': 'nặng'}
>>> ' '.join(toneNames[separate_tone(syll)[1]] for syll in "Tôi thầm cảm ơn Đẩu đã giữ mình ở nán lại".split(' '))
'thanh huyền hỏi thanh hỏi ngã ngã huyền hỏi sắc nặng'
```

For further usages, see the documentation, which is hosted on [chiecthuyenngoaixa.readthedocs.io](https://chiecthuyenngoaixa.readthedocs.io/en/latest/).
