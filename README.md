# chiecthuyenngoaixa

[![GitHub issues](https://img.shields.io/github/issues/IoeCmcomc/chiecthuyenngoaixa)](https://github.com/IoeCmcomc/chiecthuyenngoaixa/issues)
[![GitHub license](https://img.shields.io/github/license/IoeCmcomc/chiecthuyenngoaixa)](https://github.com/IoeCmcomc/chiecthuyenngoaixa/blob/master/LICENSE)
[![Documentation Status](https://readthedocs.org/projects/chiecthuyenngoaixa/badge/?version=latest)](https://chiecthuyenngoaixa.readthedocs.io/en/latest/?badge=latest)
![PyPI](https://img.shields.io/pypi/v/chiecthuyenngoaixa)
![PyPI - Downloads](https://img.shields.io/pypi/dm/chiecthuyenngoaixa)

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
'một trăm hai mươi ba nghìn tỉ bốn trăm năm mươi sáu tỉ bảy trăm tám mươi chín triệu không trăm hai mươi mốt nghìn không trăm linh ba phẩy bốn mươi lăm'
```

- To sort Vietnamese texts:

```python
>>> from ctnx import ViSortKey
>>> lines = ['Hà Nam', 'Hải Dương', 'Hà Nội', 'Hà Tĩnh', 'Hải Phòng', 'Hậu Giang', 'Hoà Bình', 'Hưng Yên', 'Hạ Long', 'Hà Giang', 'Điện Biên'\]
>>> sorted(lines, key=ViSortKey)
['Điện Biên', 'Hà Giang', 'Hà Nam', 'Hà Nội', 'Hà Tĩnh', 'Hải Dương', 'Hải Phòng', 'Hạ Long', 'Hậu Giang', 'Hoà Bình', 'Hưng Yên']
```

For further usages, see the documentation, which is hosted on [chiecthuyenngoaixa.readthedocs.io](https://chiecthuyenngoaixa.readthedocs.io/en/latest/).
