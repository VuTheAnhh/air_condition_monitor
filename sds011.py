from __future__ import print_function
from serial import Serial, EIGHTBITS, STOPBITS_ONE, PARITY_NONE
import time, struct

port = "com12"  # Port
baudrate = 9600

ser = Serial(port, baudrate=baudrate, bytesize=EIGHTBITS, parity=PARITY_NONE, stopbits=STOPBITS_ONE)
ser.flushInput()

HEADER_BYTE = b"\xAA"
COMMANDER_BYTE = b"\xC0"
TAIL_BYTE = b"\xAB"

byte, previousbyte = b"\x00", b"\x00"

while True:
    previousbyte = byte
    byte = ser.read(size=1)

    if previousbyte == HEADER_BYTE and byte == COMMANDER_BYTE:
        packet = ser.read(size=8)
        readings = struct.unpack('<HHcccc', packet)

        pm_25 = readings[0] / 10.0
        pm_10 = readings[1] / 10.0

        id = packet[4:6]

        checksum = readings[4][0]
        calculated_checksum = sum(packet[:6]) & 0xFF
        checksum_verified = (calculated_checksum == checksum)

        tail = readings[5]

        if tail == TAIL_BYTE and checksum_verified:
            # print("PM 2.5:", pm_25, "μg/m^3  PM 10:", pm_10, "μg/m^3")
            print("PM 2.5:", pm_25, "µg/m³  PM 10:", pm_10, "µg/m³  ID:", bytes(id).hex())