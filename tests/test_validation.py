from ctnx.validation import CccdResult, parse_cccd, is_valid_cccd


def test_parse_cccd():
    assert parse_cccd("011167000556") == \
        CccdResult(id='000556', is_male=False, birth_year=1967, birth_country='vn', birth_province='Điện Biên')
    assert parse_cccd("015204001166") == \
        CccdResult(id='001166', is_male=True, birth_year=2004, birth_country='vn', birth_province='Yên Bái')

def test_is_valid_cccd():
    assert is_valid_cccd("123456789") == False
    assert is_valid_cccd("321654987321") == False
    assert is_valid_cccd("001199000000") == False