# chiecthuyenngoaixa

[![GitHub issues](https://img.shields.io/github/issues/IoeCmcomc/chiecthuyenngoaixa)](https://github.com/IoeCmcomc/chiecthuyenngoaixa/issues)
[![GitHub license](https://img.shields.io/github/license/IoeCmcomc/chiecthuyenngoaixa)](https://github.com/IoeCmcomc/chiecthuyenngoaixa/blob/master/LICENSE)
[![Documentation Status](https://readthedocs.org/projects/chiecthuyenngoaixa/badge/?version=latest)](https://chiecthuyenngoaixa.readthedocs.io/en/latest/?badge=latest)
![PyPI](https://img.shields.io/pypi/v/chiecthuyenngoaixa)
![PyPI - Downloads](https://img.shields.io/pypi/dm/chiecthuyenngoaixa)

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

## Cách dùng cơ bản

Thư viện giờ đây sẽ có thể dùng được bằng mô-đun `ctnx` (viết tắt của _chiecthuyenngoaixa_).

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
>>> from ctnx import ViSortKey
>>> lines = ['Hà Nam', 'Hải Dương', 'Hà Nội', 'Hà Tĩnh', 'Hải Phòng', 'Hậu Giang', 'Hoà Bình', 'Hưng Yên', 'Hạ Long', 'Hà Giang', 'Điện Biên'\]
>>> sorted(lines, key=ViSortKey)
['Điện Biên', 'Hà Giang', 'Hà Nam', 'Hà Nội', 'Hà Tĩnh', 'Hải Dương', 'Hải Phòng', 'Hạ Long', 'Hậu Giang', 'Hoà Bình', 'Hưng Yên']
```

Để biết thêm cách sử dụng, hãy xem tài liệu (tiếng Anh) nằm ở [chiecthuyenngoaixa.readthedocs.io](https://chiecthuyenngoaixa.readthedocs.io/en/latest/).
