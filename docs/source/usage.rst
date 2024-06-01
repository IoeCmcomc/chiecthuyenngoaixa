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

* To extract tones from a Vietnamese syllable or text:

    .. doctest::
        :pyversion: >= 3.8

        >>> from ctnx.misc import separate_tone
        >>> separate_tone("Đẩu")
        ('Đâu', '?')
        >>> toneNames = {'': 'thanh', '/': 'sắc', '\\': 'huyền', '?': 'hỏi', '~': 'ngã', '.': 'nặng'}
        >>> ' '.join(toneNames[separate_tone(syll)[1]] for syll in "Tôi thầm cảm ơn Đẩu đã giữ mình ở nán lại".split(' '))
        'thanh huyền hỏi thanh hỏi ngã ngã huyền hỏi sắc nặng'

* To manipulate Vietnamese syllables:

    .. doctest::
        :pyversion: >= 3.8

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

See :doc:`generated/api` section for full references.