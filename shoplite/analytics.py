"""Analytics: revenue reporting.

Depends on events. It keeps running totals from OrderPlaced and OrderConfirmed events and
no longer reads order data from the orders module.
"""
from shoplite import events

_placed = 0
_confirmed = 0
_revenue_cents = 0


def _on_order_placed(payload):
    global _placed
    _placed += 1


def _on_order_confirmed(payload):
    global _confirmed, _revenue_cents
    _confirmed += 1
    _revenue_cents += payload["total_cents"]


events.subscribe("OrderPlaced", _on_order_placed)
events.subscribe("OrderConfirmed", _on_order_confirmed)


def order_count():
    """Return the number of orders placed (rejected orders are not counted)."""
    return _placed


def total_revenue_cents():
    """Return revenue from confirmed orders only, in cents."""
    return _revenue_cents


def average_order_value_cents():
    """Return the average value of confirmed orders in cents (0 if there are none)."""
    if _confirmed == 0:
        return 0
    return _revenue_cents // _confirmed


def revenue_summary():
    """Return order count, confirmed revenue, and average confirmed order value."""
    return {
        "orders": order_count(),
        "revenue_cents": total_revenue_cents(),
        "average_order_value_cents": average_order_value_cents(),
    }
