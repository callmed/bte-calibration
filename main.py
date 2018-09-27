from canlib import canlib, Frame
from canlib.canlib import ChannelData


def setUpChannel(channel=0,
                 openFlags=canlib.canOPEN_ACCEPT_VIRTUAL,
                 bitrate=canlib.canBITRATE_500K,
                 bitrateFlags=canlib.canDRIVER_NORMAL):
    ch = canlib.openChannel(channel, openFlags)
    print("Using channel: %s, EAN: %s" % (ChannelData(channel).device_name,
                                          ChannelData(channel).card_upc_no)
                                              )
    ch.setBusOutputControl(bitrateFlags)
    ch.setBusParams(bitrate)
    ch.busOn()
    return ch


def tearDownChannel(ch):
    ch.busOff()
    ch.close()


print("canlib version:", canlib.dllversion())

ch0 = setUpChannel(channel=0)
ch1 = setUpChannel(channel=1)

frame = Frame(id_=100, data=[1, 2, 3, 4], flags=canlib.canMSG_EXT)
ch1.write(frame)

while True:
    try:
        frame = ch0.read()
        print(frame)
        break
    except (canlib.canNoMsg) as ex:
        pass
    except (canlib.canError) as ex:
        print(ex)

tearDownChannel(ch0)
tearDownChannel(ch1)
