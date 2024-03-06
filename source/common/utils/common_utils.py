import uuid


def parse_valid_uuid(value):
    try:
        uuid.UUID(value)
        return value
    except (ValueError, AttributeError):
        return None