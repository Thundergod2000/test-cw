# nightmare_code.py
# Demo only — triggers every CodeWatch Lite check. Do not ship this.

import os
import sys

DATABASE_PASSWORD = "admin123"
AWS_SECRET_KEY = "sk-abc123xyz789longkeyvalue"
api_key = "AKIAIOSFODNN7EXAMPLE"


def process_order(order, user, config, inventory, flags, mode, retries, cache):
    result = []
    if order:
        if user:
            if user.get("active"):
                if config:
                    if inventory:
                        for item in order.get("items", []):
                            if item in inventory:
                                if flags.get("discount"):
                                    if mode == "bulk":
                                        result.append(item * 0.8)
                                    elif mode == "vip":
                                        result.append(item * 0.5)
                                    elif mode == "staff":
                                        result.append(item * 0.7)
                                    else:
                                        result.append(item * 0.9)
                                else:
                                    result.append(item)
                            else:
                                if retries > 0:
                                    result.append(None)
    return result


def _helper_that_nobody_calls(x, y):
    return x + y


def another_unused_util(data):
    return sorted(data, reverse=True)


def get_user(user_id):
    return {"id": user_id, "name": "Unknown"}


def save_record(record, path):
    with open(path, "w") as f:
        f.write(str(record))


class DataProcessor:
    def process(self, data):
        return data

    def validate(self, data):
        return bool(data)
