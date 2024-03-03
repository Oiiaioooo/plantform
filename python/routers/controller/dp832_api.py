from fastapi import APIRouter, Response
from utils.exp.dp832 import DP832
from pydantic import BaseModel, Field
from typing import List

# 因为要防止循环导入，所以全部改为使用APIRouter
router = APIRouter()


# 注意使用pydantic的时候，每一个定义都不能重名，否则可能会引发错误
class dp832_config(BaseModel):
    channels: List[int] = Field(default=[1, 2, 3], title="电源的通道", description="例如:[1,2,3]")
    voltages: List[float] = Field(default=[0, 0, 0], title="各个通道的电压", description="例如:[1,0,0]")
    currents: List[float] = Field(default=[0, 0, 0], title="各个通道的电流", description="例如[1,0,0]")
    output_states: List[bool] = Field(default=[0, 0, 0], title="通道的输出状态", description="例如[True,False,False]")


dp832_addr = "USB0::0x1AB1::0x0E11::DP8C175105663::INSTR"
# dp832_addr = "USB0::0x1AB1::0x0E11::DP8C175105606::INSTR"


@router.post("/dp832/", status_code=200)
async def set_dp832(dp832_config: dp832_config, response: Response):
    print('call set_dp832')
    try:
        dp832 = DP832(dev_name=dp832_addr)
        for ch, voltage, current, output_state in zip(dp832_config.channels, dp832_config.voltages,
                                                      dp832_config.currents,
                                                      dp832_config.output_states):
            dp832.set_channel_settings(ch, voltage, current)
            dp832.set_output_state(ch, output_state)
        # print(config_after, dp832_config.dict())
    except Exception as e:
        print(e)
        response.status_code = 500
        return {'code': 500, 'message': "仪器出错了" + str(e)}
    else:
        return {'code': 200, 'message': "设置成功"}


@router.get("/dp832/config/", status_code=200)
async def get_dp832_config(response: Response):
    try:
        dp832 = DP832(dev_name=dp832_addr)
        chs = [1, 2, 3]
        vols = []
        curs = []
        states = []
        for ch in chs:
            states.append(dp832.get_output_state(ch))
            output = dp832.get_channel_settings(ch)
            vols.append(output['voltage'])
            curs.append(output['current'])
    except Exception as e:
        print(e)
        response.status_code = 500
        return {'message': "仪器出错了" + str(e)}
    else:
        return {'channels': chs, 'voltages': vols, 'currents': curs, 'output_states': states}


@router.get("/dp832/data/", status_code=200)
async def get_dp832_data(response: Response):
    try:
        dp832 = DP832(dev_name=dp832_addr)
        chs = [1, 2, 3]
        l = []
        for ch in chs:
            data = dp832.measure_all(ch)
            data.update({'channel': ch})
            l.append(data)
        # print(l)
    except Exception as e:
        print(e)
        response.status_code = 500
        return {'code': 500, 'message': "仪器出错了" + str(e)}
    else:
        return l
