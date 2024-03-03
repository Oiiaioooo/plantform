import serial
import time


mySerial = serial.Serial("COM3", 115200, timeout=5)
time.sleep(1)
# 02发送指令让继电器动，10指的是后面的字节数，接下来两个字节一组，00指的是0号上继电器，每个板上8个继电器，
# 00 00 代表0号板清零
clr = bytes.fromhex('02 10 00 00 01 00 02 00 03 00 04 00 05 00 06 00 07 00')

# # 对应boost，00 28 指0号继电器上开第四个和第六个
# dat1 = bytes.fromhex('02 08 00 28 01 00 02 06 03 04');
# # buck
# dat2 = bytes.fromhex('02 08 00 01 01 84 02 40 03 02');
# # buck-boost
# dat3 = bytes.fromhex('02 08 00 01 01 01 02 21 03 02');

mySerial.write(clr)
time.sleep(1)
# mySerial.write(data)

mySerial.close()
