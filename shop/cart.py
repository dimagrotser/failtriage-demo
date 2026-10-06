def total(prices_cents: list[int], discount_percent: int = 0) -> int:
    """Price of a cart in cents after a percentage discount, rounded down."""
    subtotal = sum(prices_cents)
    return subtotal - subtotal * discount_percent // 100
