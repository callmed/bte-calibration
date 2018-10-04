
import can

CAN_INTERFACE = "kvaser"
CAN_CHANNEL = 1, 2
CAN_BITRATE = 1000000


if CAN_INTERFACE not NULL:
    can.util.load_environment_config()

bus = can.interface.Bus()


def convertIEEE754Hex(value):
"""Converts a float value into a IEEE754 hex representative value."""
    hex_value = None
    int_value = None
    int_value = np.float32(float(value)).view(np.int32).item()
    hex_value = hex(int_value)
    return hex_value


def loadDataToMessage(payload):
"""Re-orders data to fit the INTEL byte-order rule (little-endian)."""
    # Least significant byte at least significat message byte
    return payload


def swapPayload(payload):
    """Reverse a string as string pairs of two."""
    payload_reverse = []
    len_pair = 2
    pair_lst = [payload[i:i+len_pair] for i in range(0, len(payload), len_pair)]
    for p in reversed(pair_lst):
        payload_reverse.append(p)
    return payload_reverse
