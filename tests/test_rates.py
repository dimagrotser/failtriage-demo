from shop.rates import convert


def test_convert_to_euro():
    assert convert(1000, "EUR") == 900


def test_convert_to_pound():
    assert convert(1000, "GBP") == 800
