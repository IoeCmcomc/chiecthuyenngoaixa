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
        'một trăm hai mươi ba nghìn tỉ bốn trăm năm mươi sáu tỉ bảy trăm tám mươi chín triệu không trăm hai mươi mốt nghìn không trăm linh ba phẩy bốn năm'

* To sort Vietnamese texts:

    .. doctest::
        :pyversion: >= 3.8

        >>> from ctnx import ViSortKey
        >>> lines = ['Hà Nam', 'Hải Dương', 'Hà Nội', 'Hà Tĩnh', 'Hải Phòng', 'Hậu Giang', 'Hoà Bình', 'Hưng Yên', 'Hạ Long', 'Hà Giang', 'Điện Biên']
        >>> sorted(lines, key=ViSortKey)
        ['Điện Biên', 'Hà Giang', 'Hà Nam', 'Hà Nội', 'Hà Tĩnh', 'Hải Dương', 'Hải Phòng', 'Hạ Long', 'Hậu Giang', 'Hoà Bình', 'Hưng Yên']

Other functions and classes are put into separate sub-modules. See :doc:`generated/api` section for full references.