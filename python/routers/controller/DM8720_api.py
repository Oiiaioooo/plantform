from fastapi import APIRouter, Response
import datetime

from pydantic import BaseModel
import serial

router = APIRouter()

@router.get('/dm8720/data/', status_code=200)
async def get_dm3058_data(response: Response):
    try:
        # 打开串口
        ser = serial.Serial('COM6', 9600, timeout=0.5)

        # 发送读取命令
        cmd = bytes.fromhex('01 03 01 00 00 06 C4 34')
        ser.write(cmd)

        # 读取返回数据
        data = ser.read(17)
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

    except Exception as e:
        print(e)
        response.status_code = 500
        return {'code': 500, 'message': "仪器出错了" + str(e)}
    else:
        return {'Voltage': voltage,'Current': current,'Power': power}


@router.get('/dm8720/data/test', status_code=200)
async def get_dm3058_data(response: Response):
    try:
       pass
    except Exception as e:
        print(e)
        response.status_code = 500
        return {'code': 500, 'message': "仪器出错了" + str(e)}
    else:
        return {'Voltage': 1.1, 'Current': 1.1, 'Power': 1.21}
