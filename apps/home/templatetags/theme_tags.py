from django import template

register = template.Library()

_ROMAN = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
    (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
]


def _to_roman(n):
    out = ""
    for value, symbol in _ROMAN:
        while n >= value:
            out += symbol
            n -= value
    return out


@register.filter
def roman(value):
    """4 -> IV. Anything that isn't a positive integer is returned unchanged."""
    try:
        n = int(value)
    except (TypeError, ValueError):
        return value
    return _to_roman(n) if n > 0 else value


@register.filter
def threat(card_count):
    """Threat level I to V: one level per 8 cards."""
    try:
        n = int(card_count)
    except (TypeError, ValueError):
        return "I"
    return _to_roman(min(5, max(1, (n + 7) // 8)))


@register.filter
def bounty(card_count):
    """Max XP for clearing a dungeon (matches the 15 XP per card in the run view)."""
    try:
        return int(card_count) * 15
    except (TypeError, ValueError):
        return 0