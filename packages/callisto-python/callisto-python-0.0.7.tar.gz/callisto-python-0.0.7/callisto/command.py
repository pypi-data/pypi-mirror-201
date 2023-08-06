from enum import Enum

D1_COMMAND_DELIMITER = "___callisto_d1_command___"


class D1CommandType(str, Enum):
    NOTIFY = "notify"
