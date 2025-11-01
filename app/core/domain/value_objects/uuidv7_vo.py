import os
import time
from dataclasses import dataclass


@dataclass(frozen=True)
class UUIDv7:
    value: str | None

    def __post_init__(self):
        if self.value is None:
            final_uuidv7 = UUIDv7.__generate_uuidv7()
            object.__setattr__(self, 'value', final_uuidv7)

        elif isinstance(self.value, str):
            object.__setattr__(self, 'value', self.value)

        else:
            raise ValueError("Invalid UUID format")

    @staticmethod
    def __generate_uuidv7() -> str:
        # random bytes
        value = bytearray(os.urandom(16))

        # current timestamp in ms
        timestamp = int(time.time() * 1000)

        # timestamp
        value[0] = (timestamp >> 40) & 0xFF
        value[1] = (timestamp >> 32) & 0xFF
        value[2] = (timestamp >> 24) & 0xFF
        value[3] = (timestamp >> 16) & 0xFF
        value[4] = (timestamp >> 8) & 0xFF
        value[5] = timestamp & 0xFF

        # version and variant
        value[6] = (value[6] & 0x0F) | 0x70
        value[8] = (value[8] & 0x3F) | 0x80

        formated_uuid = '-'.join([
            ''.join(f'{byte:02x}' for byte in value[0:4]),
            ''.join(f'{byte:02x}' for byte in value[4:6]),
            ''.join(f'{byte:02x}' for byte in value[6:8]),
            ''.join(f'{byte:02x}' for byte in value[8:10]),
            ''.join(f'{byte:02x}' for byte in value[10:16])
        ])

        return formated_uuid
