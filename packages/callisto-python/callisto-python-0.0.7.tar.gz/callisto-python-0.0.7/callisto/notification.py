import json
import sys

from .command import D1_COMMAND_DELIMITER, D1CommandType


def create_notification_payload(title: str, message: str) -> str:
    command = {"command_type": D1CommandType.NOTIFY, "title": title, "message": message}
    command_str = json.dumps(command, separators=(",", ":"))
    return f"{D1_COMMAND_DELIMITER}{command_str}{D1_COMMAND_DELIMITER}"


def send_notification(title: str, message: str) -> None:
    payload = create_notification_payload(title, message)
    sys.stdout.write(payload)
