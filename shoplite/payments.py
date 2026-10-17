"""Payments: charges and refunds for authenticated users.

Depends on auth to identify the caller.
"""
import itertools
import time

from shoplite import auth

CAPTURE_MODE = "auto"
REFUND_WINDOW_DAYS = 30

_payments = {}  # payment_id -> record
_ids = itertools.count(1)


def charge(token, amount_cents):
    """Charge the user behind the token. Returns a payment record (dict).

    In "auto" capture mode the payment is captured immediately (status "captured").
    Otherwise it is only authorized (status "authorized").
    """
    username = auth.verify_token(token)
    if username is None:
        raise PermissionError("invalid or expired token")
    if amount_cents <= 0:
        raise ValueError("amount must be positive")
    payment_id = "pay_%d" % next(_ids)
    status = "captured" if CAPTURE_MODE == "auto" else "authorized"
    record = {
        "payment_id": payment_id,
        "user": username,
        "amount_cents": amount_cents,
        "status": status,
        "created_at": time.time(),
    }
    _payments[payment_id] = record
    return record


def refund(token, payment_id):
    """Refund a payment owned by the caller, if it is inside the refund window."""
    username = auth.verify_token(token)
    if username is None:
        raise PermissionError("invalid or expired token")
    record = _payments.get(payment_id)
    if record is None or record["user"] != username:
        raise KeyError("payment not found")
    age_days = (time.time() - record["created_at"]) / 86400
    if age_days > REFUND_WINDOW_DAYS:
        raise ValueError("refund window has passed")
    record["status"] = "refunded"
    return record
