"""Payments: charges and refunds for authenticated users.

Depends on auth to identify the caller and on events to react to new orders.
"""
import itertools
import time

from shoplite import auth, events

CAPTURE_MODE = "manual"
REFUND_WINDOW_DAYS = 14
SUPPORTED_CURRENCIES = {"USD", "EUR", "INR"}

_payments = {}  # payment_id -> record
_ids = itertools.count(1)


def charge(token, amount_cents, currency="USD"):
    """Charge the user behind the token. Returns a payment record (dict).

    In "auto" capture mode the payment is captured immediately (status "captured").
    Otherwise it is only authorized (status "authorized").
    """
    username = auth.verify_token(token)
    if username is None:
        raise PermissionError("invalid or expired token")
    return _record_charge(username, amount_cents, currency)


def _record_charge(username, amount_cents, currency):
    """Validate and store a charge for a user. Shared by charge() and the order handler."""
    if amount_cents <= 0:
        raise ValueError("amount must be positive")
    if currency not in SUPPORTED_CURRENCIES:
        raise ValueError("unsupported currency")
    payment_id = "pay_%d" % next(_ids)
    status = "captured" if CAPTURE_MODE == "auto" else "authorized"
    record = {
        "payment_id": payment_id,
        "user": username,
        "amount_cents": amount_cents,
        "currency": currency,
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


def _on_order_placed(payload):
    """React to an OrderPlaced event by charging the user and announcing the result."""
    record = _record_charge(
        payload["user"], payload["total_cents"], payload.get("currency", "USD")
    )
    events.publish(
        "PaymentProcessed",
        {
            "order_id": payload["order_id"],
            "payment_id": record["payment_id"],
            "status": record["status"],
        },
    )


events.subscribe("OrderPlaced", _on_order_placed)
