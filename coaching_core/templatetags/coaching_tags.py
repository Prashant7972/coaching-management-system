from django import template
from decimal import Decimal

register = template.Library()


@register.filter(name='inr')
def inr_format(value):
    """
    Formats a numeric value into the Indian numbering system with Rupee symbol:
    e.g. 150000 -> ₹1,50,000.00
    12500000 -> ₹1,25,00,000.00
    """
    if value is None or value == '':
        return "₹0.00"

    try:
        val = Decimal(str(value))
    except Exception:
        return f"₹{value}"

    is_negative = val < 0
    val = abs(val)

    # Format to 2 decimal places
    s = f"{val:.2f}"
    int_part, dec_part = s.split('.')

    if len(int_part) <= 3:
        formatted_int = int_part
    else:
        last3 = int_part[-3:]
        remaining = int_part[:-3]
        groups = []
        while len(remaining) > 2:
            groups.insert(0, remaining[-2:])
            remaining = remaining[:-2]
        if remaining:
            groups.insert(0, remaining)
        formatted_int = ','.join(groups) + ',' + last3

    result = f"₹{formatted_int}.{dec_part}"
    return f"-{result}" if is_negative else result


@register.filter(name='inr_compact')
def inr_compact_format(value):
    """
    Formats large currency amounts into Indian economic denominations:
    Crores (Cr) and Lakhs (L).
    e.g. 1,25,00,000 -> ₹1.25 Cr
    1,50,000 -> ₹1.50 L
    45,000 -> ₹45,000
    """
    if value is None or value == '':
        return "₹0"

    try:
        val = float(value)
    except Exception:
        return f"₹{value}"

    is_neg = val < 0
    val = abs(val)

    prefix = "-" if is_neg else ""

    if val >= 10000000:
        cr = val / 10000000
        return f"{prefix}₹{cr:.2f} Cr"
    elif val >= 100000:
        lakh = val / 100000
        return f"{prefix}₹{lakh:.2f} Lakh"
    else:
        # Standard format
        return f"{prefix}{inr_format(val)}"


@register.filter(name='initials')
def get_initials(name):
    """
    Extracts 2-letter uppercase initials from full name for avatar badges.
    e.g. 'Priya Sharma' -> 'PS', 'Amit' -> 'AM'
    """
    if not name:
        return "--"
    parts = str(name).strip().split()
    if len(parts) >= 2:
        return f"{parts[0][0]}{parts[-1][0]}".upper()
    elif len(parts) == 1 and len(parts[0]) >= 2:
        return parts[0][:2].upper()
    elif len(parts) == 1 and len(parts[0]) == 1:
        return parts[0][0].upper()
    return "--"
