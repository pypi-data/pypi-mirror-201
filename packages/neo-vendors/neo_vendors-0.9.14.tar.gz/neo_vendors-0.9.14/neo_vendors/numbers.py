import decimal


def get_fractional_part_len(value: decimal.Decimal) -> int:
    return abs(int(value.as_tuple().exponent))
