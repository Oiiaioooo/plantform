from utils.exp.tbs1202b import tbs1202b
from fastapi import APIRouter, Response

router = APIRouter()
tbs1202b_addr = 'USB0::0x0699::0x0368::C010936::INSTR'


@router.get('/tbs1202b/data/', status_code=200)
async def get_tbs1202b_data(response:Response):
    try:
        tbs1202 = tbs1202b(visa_address=tbs1202b_addr)
        data = tbs1202.get_curve("CH1")
        print(data)
    except Exception as e:
        print(e)
        response.status_code = 500
        return {'code': 500, 'message': "仪器出错了" + str(e)}
    else:
        return {
            'ch1': {'time': data['time'], 'wave': data['wave']},
            'ch2': {'time': [], 'wave': []}
        }
    #
    # data1 = tbs1202.get_curve("CH1")
    # data2 = tbs1202.get_curve("CH2")
    # # print(data)
    # return {
    #     'ch1': {'time': data1['time'], 'wave': data1['wave']},
    #     'ch2': {'time': data2['time'], 'wave': data2['wave']}
    # }
