"""Bootstrap: imports the modules that register event handlers when they are loaded.

Import this module once at application start. Without it, handlers such as the payments
handler for OrderPlaced are never registered.
"""
from shoplite import orders, payments  # noqa: F401  (imported for side effects)
