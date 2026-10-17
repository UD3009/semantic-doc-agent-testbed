"""Analytics: revenue reporting.

Depends on orders. Reads order data directly by calling orders.list_orders().
"""
from shoplite import orders


def order_count():
    """Return the number of orders placed (rejected orders are not stored)."""
    return len(orders.list_orders())


def total_revenue_cents():
    """Return revenue from confirmed orders only, in cents."""
    return sum(o.total_cents for o in orders.list_orders() if o.status == "confirmed")


def average_order_value_cents():
    """Return the average value of confirmed orders in cents (0 if there are none)."""
    confirmed = [o for o in orders.list_orders() if o.status == "confirmed"]
    if not confirmed:
        return 0
    return sum(o.total_cents for o in confirmed) // len(confirmed)


def revenue_summary():
    """Return order count, confirmed revenue, and average confirmed order value."""
    return {
        "orders": order_count(),
        "revenue_cents": total_revenue_cents(),
        "average_order_value_cents": average_order_value_cents(),
    }
