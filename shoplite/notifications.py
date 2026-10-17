"""Notifications: user-facing messages.

Depends on auth to check that a recipient exists.
"""
from shoplite import auth

ORDER_TEMPLATE = "Thanks for your order, {user}! We have received {order_id} and will keep you posted."

_outbox = []  # messages "sent" so far


def send_order_confirmation(username, order_id):
    """Send an order confirmation to a registered user. Returns the message text."""
    if not auth.user_exists(username):
        raise KeyError("unknown user")
    message = ORDER_TEMPLATE.format(user=username, order_id=order_id)
    _outbox.append({"to": username, "body": message})
    return message


def get_outbox():
    """Return a copy of all messages sent so far."""
    return list(_outbox)
