import smbus

bus = smbus.SMBus(1)
device = 0x19

ACC_RANGE = 0x41
ACC_CONF = 0x40

accel_conf = {
    "odr": 0x0c, # 400Hz
    "range": 0x00, # 2g
    "bandwidth": 0x04, # 2 ^ 5 = 32
    "perf_mode": 0x00, # average
}

def set_accel_config(accel_conf):
    rslt = 0
    accel_config_data = [0, 0]

    # Check whether the bandwidth , odr and perf_mode combinations are valid
    accel_config_data[0] = accel_conf["odr"] & 0x1F
    accel_config_data[0] |= (accel_conf["bandwidth"] << 5)
    accel_config_data[0] |= (accel_conf["perf_mode"] << 7)
    accel_config_data[1] = accel_conf["range"] & 0x03

    bus.write_byte_data(device, ACC_CONF, accel_config_data[0])
    
    rslt = bus.write_byte_data(device, ACC_RANGE, accel_config_data[1])

set_accel_config(accel_conf)

# enable accel
bus.write_byte_data(device, 0x7d, 4)