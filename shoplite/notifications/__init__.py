"""Notifications: user-facing messages, sent through email and SMS channels.

The public interface is unchanged: send_order_confirmation() and get_outbox(), plus the new
set_preference(). Depends on auth (through the dispatcher).
"""
from shoplite.notifications.dispatcher import (  # noqa: F401
    get_outbox,
    send_order_confirmation,
    set_preference,
)
