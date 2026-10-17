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


def revenue_summary():
    """Return a small summary dict of order count and confirmed revenue."""
    return {"orders": order_count(), "revenue_cents": total_revenue_cents()}
