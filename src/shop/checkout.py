"""Order checkout.

The rules live in `src/shop/specs/checkout.md` - read it first.
Both functions below are stubs: their signature is final, the bodies are yours.
Do not change the constants: the tests rely on them.
"""

from shop.money import percent_of

PROMO_CODES = {"WELCOME10": 10, "SUMMER15": 15, "VIP35": 35}
SUPPORTED_CITIES = ("msk", "spb")
MAX_DISCOUNT_PERCENT = 30
VAT_PERCENT = 20
SHIPPING_KOPEKS = 49_000
FREE_DELIVERY_FROM_KOPEKS = 500_000
TIER_DISCOUNTS = ((10, 5), (25, 10), (50, 15))
REQUIRED_LINE_KEYS = ("sku", "qty", "unit_price_kopecks")


def _is_int_text(value: str) -> bool:
    """Check whether `int()` would parse the value, without catching exceptions."""
    text = value.strip()
    if text[:1] in ("+", "-"):
        text = text[1:]
    return text != "" and all(part.isascii() and part.isdigit() for part in text.split("_"))


def validate_order(
    lines: list[dict[str, str]],
    promo_code: str = "",
    shipping_city: str = "",
) -> str | None:
    """Return a human readable reason why the order is invalid, or None if it is fine."""
    # Only the happy path exists yet: rejection rules arrive one by one with later tests.
    if not lines:
        return "empty order"
    for index, raw in enumerate(lines, start=1):
        for key in REQUIRED_LINE_KEYS:
            if key not in raw:
                return f"missing key in line {index}"
        if not raw["sku"]:
            return "empty sku"
        if not _is_int_text(raw["qty"]):
            return "invalid qty"
    return None


def calculate_order_total(
    lines: list[dict[str, str]],
    promo_code: str = "",
    shipping_city: str = "",
) -> int | None:
    """Return the order total in kopecks, or None if the order is invalid."""
    # Only the smoke case exists yet: subtotal plus VAT, no discounts or delivery.
    if validate_order(lines, promo_code, shipping_city) is not None:
        return None
    subtotal = 0
    for raw in lines:
        subtotal += int(raw["qty"]) * int(raw["unit_price_kopecks"])
    return subtotal + percent_of(subtotal, VAT_PERCENT)
