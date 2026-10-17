"""Dispatcher: decides which channels a notification goes to and sends it.

Depends on auth (the recipient must exist) and on the email and SMS channel modules.
"""
from shoplite import auth
from shoplite.notifications import email_channel, sms_channel

ORDER_TEMPLATE = "Thanks for your order, {user}! We have received {order_id} and will keep you posted."

CHANNELS = {"email": email_channel, "sms": sms_channel}
DEFAULT_CHANNELS = ("email",)

_preferences = {}  # username -> tuple of channel names


def set_preference(username, channels):
    """Choose which channels a user is notified on."""
    for name in channels:
        if name not in CHANNELS:
            raise ValueError("unknown channel: %s" % name)
    _preferences[username] = tuple(channels)


def send_order_confirmation(username, order_id):
    """Send an order confirmation on the user's channels. Returns the message text."""
    if not auth.user_exists(username):
        raise KeyError("unknown user")
    message = ORDER_TEMPLATE.format(user=username, order_id=order_id)
    for name in _preferences.get(username, DEFAULT_CHANNELS):
        CHANNELS[name].deliver(username, message)
    return message


def get_outbox(channel=None):
    """Return messages sent so far, optionally for a single channel."""
    if channel is not None:
        return CHANNELS[channel].sent()
    return [m for ch in CHANNELS.values() for m in ch.sent()]
