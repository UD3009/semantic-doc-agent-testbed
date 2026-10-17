"""Email channel: delivers full-length messages by email (simulated)."""

_sent = []


def deliver(username, text):
    """Record an email to the user."""
    _sent.append({"to": username, "channel": "email", "body": text})


def sent():
    """Return a copy of the emails delivered so far."""
    return list(_sent)
