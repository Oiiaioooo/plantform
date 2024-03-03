from fastapi import APIRouter, Response
import datetime
from utils.exp.dm3058 import dm3058
from pydantic import BaseModel

dm3058_addr = "USB0::0x1AB1::0x0588::DM3H134900675::INSTR"
router = APIRouter()


class dm3058_Item(BaseModel):
    mode1: str
    mode2: str


@router.post('/dm3058/data/', status_code=200)
async def get_dm3058_data(item: dm3058_Item, response: Response):
    try:
        with dm3058() as dev:
            dev.connect(dm3058_addr, reset=False)
            data = dev.measure(item.mode1, item.mode2)
    except Exception as e:
        print(e)
        response.status_code = 500
        return {'code': 500, 'message': "仪器出错了" + str(e)}
    else:
        return {
            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "mode1": item.mode1,
            "mode2": item.mode2,
            "value": data,
            "unit": "V" if item.mode1 == "voltage" else "A"
        }
