"""Optional access token for the REST API.

Set the API_TOKEN environment variable to require it on every /api/ request, as
``Authorization: Bearer <token>`` or ``x-api-key: <token>``. Without API_TOKEN the
API stays open (default behaviour). Generated videos under /tasks/ stay readable
by URL so they can be opened in a browser.
"""

import hmac


def is_authorized(path: str, method: str, headers: dict, token: str) -> bool:
    if not token or method == "OPTIONS" or not path.startswith("/api/"):
        return True
    auth = headers.get("authorization", "")
    supplied = auth[7:] if auth.lower().startswith("bearer ") else headers.get("x-api-key", "")
    return hmac.compare_digest(supplied.encode(), token.encode())
