import serial
import time
import numpy as np
mySerial = serial.Serial("COM3", 115200, timeout = 5)
time.sleep(1)
# 02发送指令让继电器动，10指的是后面的字节数，接下来两个字节一组，00指的是0号上继电器，每个板上8个继电器，
# 00 00 代表0号板清零
clr = bytes.fromhex('02 10 00 00 01 00 02 00 03 00 04 00 05 00 06 00 07 00')
# 对应boost，00 28 指0号继电器上开第四个和第六个
dat1 = bytes.fromhex('02 08 00 28 01 00 02 06 03 04')
# buck
dat2 = bytes.fromhex('02 08 00 01 01 84 02 40 03 02')
# buck-boost
dat3 = bytes.fromhex('02 08 00 01 01 01 02 21 03 02')

# 一个继电器
# dat4 = bytes.fromhex('02 08 00 01 01 00 02 00 03 00')
# 控制一个电路板上的一个继电器
# dat5 = bytes.fromhex('02 08 04 01 05 00 06 00 07 00')
# mySerial.write(clr)
time.sleep(2)
mySerial.write(bytes.fromhex('02 0E 0F 00 0E 00 0D 00 0C 00 0B 00 0A 00 09 00'))

mySerial.close()

# circuit_nodes = 11
#
# def generate_matrix(n):
#     matrix = np.zeros((n, n),dtype=int)
#     count = 1
#     for i in range(n):
#         for j in range(i+1, n):
#             matrix[i][j] = count
#             matrix[j][i] = count
#             count += 1
#
#     return matrix


# 第一行和第一列代表的是第一个电路节点，第二行和第二列代表的是第二个电路节点，以此类推
# 因此，如果我们要连接第1个电路节点和第3个电路节点，则使用第一行第三列对应的继电器，即2号继电器
# connectionMatrix = generate_matrix(circuit_nodes)
# print(connectionMatrix+connectionMatrix.T)
#
# # 使用的继电器板子编号，每个板子上有8个继电器，因此继电器1-8对应的是'0F'板子，9-16对应的是'0E'板子，以此类推
# relay_number = ['0F', '0E', '0D', '0C', '0B', '0A', '09']
#
# #
# SetConnect = np.zeros((circuit_nodes,circuit_nodes), dtype=int)
#
# i=1
# j=10
# SetConnect[i][j] = connectionMatrix[i][j]
#
# command = "02 0E"
# N = len(relay_number)
# for n in range(N):
#     # 矩阵中1-8，对应00号继电器板
#     connect_list = SetConnect[np.where((SetConnect <= (n + 1) * 8) & (SetConnect > n * 8))]
#     # print(connect_list)
#     # 定义一个长度为8的零向量
#     trans_array = np.zeros(8, dtype=int)
#     for j in connect_list:
#         # 除8取余
#         trans_array[j % 8 - 1] = 1
#     # 反向，上面的赋值操作是0代表最左，而实际算法中0应该是最右
#     trans_array = trans_array[::-1]
#
#
#     # print(trans_array)
#
#     def array_bin_to_dec(arr):
#         reverse = arr[::-1]
#         temp = 0
#         for i in range(len(reverse)):
#             temp += reverse[i] * 2 ** i
#         return temp
#
#
#     value_left = array_bin_to_dec(trans_array[:4])
#     value_right = array_bin_to_dec(trans_array[4:])
#     command += " " + relay_number[n] + " " + str(value_left) + str(value_right)
# print(command)
#
#
# mySerial = serial.Serial("COM3", 115200, timeout = 5)
# time.sleep(2)
# # clr = bytes.fromhex('02 0E 0F 00 0E 00 0D 00 0C 00 0B 00 0A 00 09 00 ')
# # mySerial.write(clr)
# time.sleep(1)
# mySerial.write(bytes.fromhex(command))
# time.sleep(1)
# mySerial.close()