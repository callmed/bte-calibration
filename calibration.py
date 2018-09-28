
import can

CAN_INTERFACE = "kvaser"
CAN_CHANNEL = 1, 2
CAN_BITRATE = 1000000


if CAN_INTERFACE not NULL:
    can.util.load_environment_config()

bus = can.interface.Bus()
