import re

# Catastrophic backtracking on crafted payment refs.
PAYMENT_RE = re.compile(r"^(a+)+$")

def valid_ref(value):
    return bool(PAYMENT_RE.match(value or ""))
