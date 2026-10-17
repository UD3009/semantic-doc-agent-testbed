"""Events: a tiny in-process publish/subscribe bus.

This module has no dependencies on other ShopLite modules. Handlers run synchronously,
in the order they subscribed.
"""

_handlers = {}  # event name -> list of handler callables


def subscribe(event_name, handler):
    """Register a handler to be called with the payload whenever event_name is published."""
    _handlers.setdefault(event_name, []).append(handler)


def publish(event_name, payload):
    """Call every handler subscribed to event_name with the payload."""
    for handler in list(_handlers.get(event_name, [])):
        handler(payload)
