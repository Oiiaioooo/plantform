import time

from fastapi import APIRouter, Response
from pydantic import BaseModel, Field
import json
from munch import DefaultMunch
import numpy as np
import traceback
import asyncio
import serial
import pandas as pd

from routers.controller.node_json_config_api import get_init_circuit_collection

router = APIRouter()


class INPUT(BaseModel):
    data: str

# 继电器板子的编号
relay_number = ['00', '01', '02', '03', '04', '05', '06','07', '08', '09', '0A', '0B', '0C', '0D','0E', '0F',
                '10', '11', '12', '13', '14', '15', '16','17', '18', '19', '1A', '1B', '1C', '1D','1E', '1F']

# 节点之间使用的继电器，按照顺序进行编号，使用了31个继电器，这里描述的是，哪些节点之间可以连接(不为0的数字)
# ，这里理论上有9个节点，因此，需要使用1+...+8=36个继电器，但是这里只使用了31个，是因为限制了一些节点之间的链接(防止短路之类的)。
# 按照李老师的说法，在之后的设计中，我们不对节点之间的连接进行约束，因此这里直接变成一个按照顺序编号的下三角或上三角矩阵即可，不需要将一些元素设置为0
circuit_nodes = 23

def generate_matrix(n):
    matrix = np.zeros((n, n),dtype=int)
    count = 1
    for i in range(n):
        for j in range(i+1, n):
            matrix[i][j] = count
            matrix[j][i] = count
            count += 1

    return matrix
connectMatrix = generate_matrix(circuit_nodes)#circuit_node is the real node in the relay matrix
which=pd.read_excel("../../cnode_to_relay1.xlsx")
which=which.drop(which.columns[[0]],axis=1)
connectMatrix=np.array(which)


# try:
#
#     clr = bytes.fromhex('02 0E 0F 00 0E 00 0D 00 0C 00 0B 00 0A 00 09 00')
#     # mySerial.write(clr)
# except Exception as e:
#     print(e)
# 由于目前不能控制单个继电器，因此只能一次性控制所有，所以接受到的是整个graphData
@router.post('/relayMatrix/', status_code=200)
async def set_relay(item: INPUT, response: Response):#item comes from client side
    try:
        # 从数据库中检索cnode_anchor
        init_circuit_collection = get_init_circuit_collection()
        init_circuit = init_circuit_collection.find_one({"name": "exp1"})
        if init_circuit and "cnode_anchor" in init_circuit:
            circuitNodeAnchorType = init_circuit["cnode_anchor"]


        SetConnect = np.zeros(connectMatrix.shape, dtype=int)
        edgesData = json.loads(item.data)#item.data is a string, json.loads transform string into json
        print(edgesData)
        # 从所有的edgeData里，判断连线。
        for edge in edgesData:
            edge = DefaultMunch.fromDict(edge)
            sourceAnchorId = edge.sourceAnchorId
            sourceAnchorTypeIndex = -1
            targetAnchorId = edge.targetAnchorId
            targetAnchorTypeIndex = -1
            # 获得source anchor的节点类型
            for i, (type, anchors) in enumerate(circuitNodeAnchorType.items()):
                
                if sourceAnchorId in anchors:
                    sourceAnchorTypeIndex = type
                    break
            # 获得target anchor的节点类型
            for i, (type, anchors) in enumerate(circuitNodeAnchorType.items()):
                if targetAnchorId in anchors:
                    targetAnchorTypeIndex = type#targetAnchorTypeIndex is the real matrix node
                    break

            sourceAnchorTypeIndex=int(sourceAnchorTypeIndex.strip("C"))-1
            targetAnchorTypeIndex=int(targetAnchorTypeIndex.strip("C"))-1

            value=connectMatrix[sourceAnchorTypeIndex][targetAnchorTypeIndex]
            SetConnect[sourceAnchorTypeIndex][targetAnchorTypeIndex]=value
            SetConnect[targetAnchorTypeIndex][sourceAnchorTypeIndex]=value
            # source和target都是定义的类节点，则为矩阵设置数，代表连接
            # print(circuitNodeAnchorType)
            # print(sourceAnchorTypeIndex)
            # print(targetAnchorTypeIndex)

        # 在这里需要加入短路回路检测，如果有短路回路，则返回错误,这一方法尚不成熟。
        def has_simple_cycle(matrix):
            def dfs(node, parent, depth):
                if visited[node]:
                    return depth >= 2  # 确保路径长度至少为3（包括起点和终点）

                visited[node] = True
                for neighbor in range(len(matrix)):
                    if matrix[node][neighbor] > 0 and neighbor != parent:
                        if dfs(neighbor, node, depth + 1):
                            return True

                visited[node] = False  # 撤销访问状态，以便其他路径可以使用这个节点
                return False

            n = len(matrix)
            visited = [False] * n
            for i in range(n):
                if dfs(i, -1, 0):
                    return True
            return False

        # try:
        #     if has_simple_cycle(SetConnect+SetConnect.T):
        #         raise Exception("短路回路检测失败")
        # except Exception as e:
        #     return {'code': 500, 'message': "短路回路检测失败" + str(e)}

        # 同时也需要加入电源检测，如果电源没有关闭，则返回错误，拒绝执行连线操作

        # 同时还需要加入电源短路检测，如果电源短路，则返回错误，拒绝执行连线操作

        print(SetConnect)

        # 根据指令的矩阵生成命令
        # 四块继电器板，08代表后面跟8个字节，00代表第一块继电器板子
        command = "02 40"
        # 继电器板子的数量
        N = len(relay_number)

        # 这里的逻辑是，获得每一块板子对应的继电器编号，1-8对应的就是第一块板子，所以通过np.where获得对应n的所有需要开通的继电器，SetConnect里的值对应的就是需要开通的继电器。
        # 然后将需要开通的继电器，转换为对应的编码，再通过循环，遍历所有的继电器板子，逐个加入command中
        for n in range(N):
            # 矩阵中1-8，对应00号继电器板
            connect_list = SetConnect[np.where((SetConnect <= (n + 1) * 8) & (SetConnect > n * 8))]
            # print(connect_list)
            # 定义一个长度为8的零向量
            trans_array = np.zeros(8, dtype=int)
            for j in connect_list:
                # 除8取余
                trans_array[j % 8 - 1] = 1
            # 反向，上面的赋值操作是0代表最左，而实际算法中0应该是最右
            trans_array = trans_array[::-1]

            # print(trans_array)

            def array_bin_to_hex(arr):
                reverse = arr[::-1]
                temp = 0
                for i in range(len(reverse)):
                    temp += reverse[i] * 2 ** i
                if(temp<10):
                    return str(temp)
                match temp:
                    case 10:
                        return 'A'
                    case 11:
                        return 'B'
                    case 12:
                        return 'C'
                    case 13:
                        return 'D'
                    case 14:
                        return 'E'
                    case 15:
                        return 'F'
            if(n>15):
                value_left = array_bin_to_hex(np.flipud(trans_array[4:]))
                value_right = array_bin_to_hex(np.flipud(trans_array[:4]))
            else:
                value_left = array_bin_to_hex(trans_array[:4])
                value_right = array_bin_to_hex(trans_array[4:])
            command += " " + relay_number[n] + " " + value_left + value_right
        print(command)

        mySerial = serial.Serial("COM13", 115200, timeout=2)
        commanda=command.split(" ")
        command1="02 20 "+" ".join(commanda[2:34])
        command2="02 20 "+" ".join(commanda[34:])
        print(command1)
        clr1=bytes.fromhex(command1)
        clr2=bytes.fromhex(command2)
        mySerial.write(clr1)
        time.sleep(0.5)
        mySerial.close()
        mySerial = serial.Serial("COM13", 115200, timeout=2)
        mySerial.write(clr2)
        print(mySerial.read_all())
        # #print(mySerial.read(2))
        # #for i11 in range(16):
        # #    print(mySerial.read(1))
        mySerial.close()




        # time.sleep(1)
        # # 这里是先清0，然后再设置相应的值，实际上，应该直接设置也行，但是好像是因为继电器控制有bug，所以只能先清0，实际上是不是这样得研究一下才知道。
        # clr = bytes.fromhex('02 0E 0F 00 0E 00 0D 00 0C 00 0B 00 0A 00 09 00')
        # mySerial.write(clr)
        # # 这里使用异步似乎存在问题
        # # await asyncio.sleep(1)
        # time.sleep(2)
        # mySerial.write(bytes.fromhex(command))
        # mySerial.close()

    except Exception as e:
        # traceback.print_exc()
        # response.status_code = 500
        print(e)
        return {'code': 500, 'message': "继电器出错了" + str(e)}
    else:
        return {'code': 200, 'message': "设置成功"}
