from shop.cart import total


def test_total_without_discount():
    assert total([1000, 500]) == 1500


def test_total_with_discount():
    assert total([1000, 500], discount_percent=10) == 1350


def test_total_of_an_empty_cart():
    assert total([]) == 0
