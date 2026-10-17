"""Orders: orchestrates placing an order across the other modules.

Depends on auth (who is ordering), inventory (is it in stock), payments (take the
money) and notifications (confirm to the user).
"""
import itertools
from dataclasses import dataclass
from typing import Optional

from shoplite import auth, inventory, notifications, payments

TAX_RATE = 0.08

_orders = {}  # order_id -> OrderResult
_ids = itertools.count(1)


@dataclass
class OrderResult:
    """The outcome of placing an order."""

    status: str
    order_id: Optional[str] = None
    user: Optional[str] = None
    sku: Optional[str] = None
    quantity: int = 0
    total_cents: int = 0
    payment_id: Optional[str] = None
    reason: Optional[str] = None


def place_order(token, sku, quantity, unit_price_cents):
    """Place an order and return an OrderResult.

    The status is "rejected" if stock is insufficient. Otherwise it is "confirmed" when
    the payment was captured, or "pending_capture" when it was only authorized.
    """
    username = auth.verify_token(token)
    if username is None:
        raise PermissionError("invalid or expired token")
    try:
        inventory.reserve(sku, quantity)
    except inventory.OutOfStock:
        return OrderResult(status="rejected", reason="out of stock")
    subtotal = unit_price_cents * quantity
    total = round(subtotal * (1 + TAX_RATE))
    payment = payments.charge(token, total)
    status = "confirmed" if payment["status"] == "captured" else "pending_capture"
    order_id = "ord_%d" % next(_ids)
    order = OrderResult(
        status=status,
        order_id=order_id,
        user=username,
        sku=sku,
        quantity=quantity,
        total_cents=total,
        payment_id=payment["payment_id"],
    )
    _orders[order_id] = order
    notifications.send_order_confirmation(username, order_id)
    return order


def get_order(order_id):
    """Return an order by id, or None."""
    return _orders.get(order_id)


def list_orders():
    """Return all orders placed so far."""
    return list(_orders.values())
