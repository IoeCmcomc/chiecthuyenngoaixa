Usage
=====

.. _installation:

Installation
------------

Chiecthuyenngoaixa is available on `PyPI <https://pypi.org/project/chiecthuyenngoaixa/>`_.
Open a terminal or *Command Prompt* (on Windows) and run the following command:

.. code-block:: console

    pip install chiecthuyenngoaixa

If you are using `Poetry <https://python-poetry.org/>`_, use this instead:

.. code-block:: console

    poetry add chiecthuyenngoaixa

Basic usage
-----------

The library will now be available as :py:mod:`ctnx` module (abbreviation of *chiecthuyenngoaixa*).

Some commonly used functions and classes can be imported directly. For example:

* To convert Vietnamese text to ASCII-only text:

    .. doctest::
        :pyversion: >= 3.8

        >>> from ctnx import remove_diacritics
        >>> remove_diacritics("Đàn ong thấy cái lon thì bu vào.")
        'Dan ong thay cai lon thi bu vao.'

* To convert a number to Vietnamese text:

    .. doctest::
        :pyversion: >= 3.8

        >>> from ctnx import num_to_words
        >>> num_to_words(123456789021003.45)
        'một trăm hai mươi ba nghìn bốn trăm năm mươi sáu tỉ bảy trăm tám mươi chín triệu không trăm hai mươi mốt nghìn không trăm linh ba phẩy bốn mươi lăm'

* To sort Vietnamese texts:

    .. doctest::
        :pyversion: >= 3.8

        >>> from ctnx import ViSortKey
        >>> lines = ['Hà Nam', 'Hải Dương', 'Hà Nội', 'Hà Tĩnh', 'Hải Phòng', 'Hậu Giang', 'Hoà Bình', 'Hưng Yên', 'Hạ Long', 'Hà Giang', 'Điện Biên']
        >>> sorted(lines, key=ViSortKey)
        ['Điện Biên', 'Hà Giang', 'Hà Nam', 'Hà Nội', 'Hà Tĩnh', 'Hải Dương', 'Hải Phòng', 'Hạ Long', 'Hậu Giang', 'Hoà Bình', 'Hưng Yên']

Other functions and classes are put into separate sub-modules. For example:

* To convert a likely confusing text of Vietnamese to the normal text:

    .. doctest::
        :pyversion: >= 3.8

        >>> from ctnx.misc import normalize_confusables
        >>> normalize_confusables("𝕮𝖍𝖎ế𝖈 𝖙𝖍𝖚𝖞ề𝖓 𝖓𝖌𝖔à𝖎 𝖝𝖆")
        'Chiếc thuyền ngoài xa'

* To extract information from a Vietnamese National Citizen ID (*Căn cước công dân*) number:

    .. doctest::
        :pyversion: >= 3.8

        >>> from ctnx import validation
        >>> validation.is_valid_cccd("024192123456")
        True
        >>> validation.parse_cccd("024192123456")
        CccdResult(id='123456', is_male=False, birth_year=1992, birth_country='vn', birth_province='Bắc Giang')

See :doc:`generated/api` section for full references.