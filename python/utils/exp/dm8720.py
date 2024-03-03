import serial
import struct

# 打开串口
ser = serial.Serial('COM6', 9600, timeout=0.5)

# 发送读取命令
cmd = bytes.fromhex('01 03 01 00 00 06 C4 34')
ser.write(cmd)

# 读取返回数据
data = ser.read(17)
print(data)
print(len(data))
# data: 01 03 0c 40 a0 5e 06 00 00 00 00 00 00 00 00 d9 59




# 1 3 0CH 43,66,CD,C8-40,82,DD,6E-44,6B,F8,45 6FH A2H
# 43,66,CD,C8-40,82,DD,6E-44,6B,F8,45为四字节浮点数据，高字节在前，分别代表电压、电流、功率
# 解析数据
# Your data
# data = "01 03 0c 40 a0 5e 06 00 00 00 00 00 00 00 00 d9 59"

# Extract the bytes for voltage, current, and power
voltage_bytes = data[3:7]
current_bytes = data[7:11]
power_bytes = data[11:15]

# Function to convert bytes to float
def bytes_to_float(bytes_value):
    return struct.unpack('!f', bytes_value)[0]
if len(data) == 17 and data[0] == 0x01 and data[1] == 0x03 and data[2] == 0x0C:
    # Convert each group of bytes to float
    voltage = bytes_to_float(voltage_bytes)
    current = bytes_to_float(current_bytes)
    power = bytes_to_float(power_bytes)

    # Print the float values
    print(f"Voltage: {voltage}")
    print(f"Current: {current}")
    print(f"Power: {power}")



# if len(data) == 9 and data[0] == 0x01 and data[1] == 0x03 and data[2] == 0x0C:
#     voltage = (data[3] << 8 | data[4]) / 100.0
#     current = (data[5] << 8 | data[6]) / 100.0
#     power = (data[7] << 8 | data[8]) / 100.0
#     print('Voltage: %.2f V' % voltage)
#     print('Current: %.2f A' % current)
#     print('Power: %.2f W' % power)

# 关闭串口
ser.close()

# import struct

# # 假设给出的四字节浮点数据为 data，高字节在前
# # 将 data 转换为浮点数
# value = struct.unpack('>f', bytes.fromhex('43 6E F8 00'))[0]
# print('转换后的十进制数为：', value)