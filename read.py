import time
import smbus
import socket

bus = smbus.SMBus(1)
device = 0x19

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

gravity = 9.80665

def lsb_to_ms2(val, g_range, bit_width):
    power = 2
    half_scale = (pow(power, bit_width) / 2.0)
    gs = val / half_scale
    scaled = (gs - gravity * 4) if (gs > gravity * 2) else gs
    return scaled

DATA_8_ADDR = 0x12
BMA4_ACCEL_DATA_LENGTH = 6

def read_accel_xyz():
    data = bus.read_i2c_block_data(device, DATA_8_ADDR, BMA4_ACCEL_DATA_LENGTH)
    msb = data[1]
    lsb = data[0]
    x = (msb << 8) | lsb
    msb = data[3]
    lsb = data[2]
    y = (msb << 8) | lsb
    msb = data[5]
    lsb = data[4]
    z = (msb << 8) | lsb
    return x, y, z

while True:
    x, y, z = read_accel_xyz()
    # read to 4 dp
    # print("x: {:.4f} y: {:.4f} z: {:.4f}".format(lsb_to_ms2(x, 2, 16), lsb_to_ms2(y, 2, 16), lsb_to_ms2(z, 2, 16)))
    UDPClientSocket.sendto(bytes("[{:.4f}, {:.4f}, {:.4f}]".format(lsb_to_ms2(x, 2, 16), lsb_to_ms2(y, 2, 16), lsb_to_ms2(z, 2, 16)), "utf-8"), ("192.168.1.67", 2222))
    # time.sleep(0.01)