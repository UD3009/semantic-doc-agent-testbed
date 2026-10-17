"""SMS channel: delivers messages shortened to 160 characters (simulated)."""

MAX_LENGTH = 160

_sent = []


def deliver(username, text):
    """Record an SMS to the user, truncated to MAX_LENGTH characters."""
    _sent.append({"to": username, "channel": "sms", "body": text[:MAX_LENGTH]})


def sent():
    """Return a copy of the SMS messages delivered so far."""
    return list(_sent)
