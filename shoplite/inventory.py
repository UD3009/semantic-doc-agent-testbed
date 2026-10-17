"""Inventory: stock levels per SKU and stock reservation.

Depends on auth: adding stock requires the inventory:write permission.
"""
from shoplite import auth

LOW_STOCK_THRESHOLD = 5

_stock = {}  # sku -> quantity on hand


class OutOfStock(Exception):
    """Raised when a reservation asks for more units than are on hand."""


def add_stock(token, sku, quantity):
    """Add units of a SKU to stock. The caller needs the inventory:write permission."""
    if not auth.has_permission(token, "inventory:write"):
        raise PermissionError("not allowed to change stock")
    if quantity <= 0:
        raise ValueError("quantity must be positive")
    _stock[sku] = _stock.get(sku, 0) + quantity


def get_stock(sku):
    """Return units on hand for a SKU (0 if unknown)."""
    return _stock.get(sku, 0)


def reserve(sku, quantity):
    """Reserve stock for an order. Raises OutOfStock if there is not enough."""
    if _stock.get(sku, 0) < quantity:
        raise OutOfStock(sku)
    _stock[sku] -= quantity


def is_low_stock(sku):
    """Return True if stock is at or below the low-stock threshold."""
    return get_stock(sku) <= LOW_STOCK_THRESHOLD
