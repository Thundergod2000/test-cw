"""Order processing module — handles order validation and pricing."""
import os


DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")
API_KEY = os.environ.get("API_KEY")


def process_order(order: dict, user: dict, inventory: list) -> list:
    """Process an order and return priced items."""
    if not order or not user or not user.get("active"):
        return []

    items = order.get("items", [])
    available = [item for item in items if item in inventory]
    return _apply_pricing(available, user)


def _apply_pricing(items: list, user: dict) -> list:
    """Apply pricing rules to a list of available items."""
    discount = _get_discount(user)
    return [item * discount for item in items]


def _get_discount(user: dict) -> float:
    """Return the discount multiplier for a given user type."""
    user_type = user.get("type", "standard")
    discounts = {"bulk": 0.8, "vip": 0.5, "standard": 1.0}
    return discounts.get(user_type, 1.0)


def get_user(user_id: str) -> dict:
    """Fetch a user record by ID. Returns a dict with id and name."""
    return {"id": user_id, "name": "Unknown"}


def save_record(record: dict, path: str) -> None:
    """Write a record to disk at the given path."""
    with open(path, "w") as f:
        f.write(str(record))


class DataProcessor:
    """Handles validation and processing of incoming data payloads."""

    def process(self, data: list) -> list:
        """Run processing pipeline on data and return results."""
        return data

    def validate(self, data: list) -> bool:
        """Return True if data is non-empty and valid."""
        return bool(data)
