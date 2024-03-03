import pyvisa as visa
from enum import Enum
from pydantic import BaseModel
from main import app,Response




class FUNCTION(str, Enum):
    sin = "sinusoid"
    square = "square"
    ramp = "ramp"
    pulse = "pulse"


class FREQUENCY(str, Enum):
    mahz = "MAHz"
    khz = "kHz"
    hz = "Hz"
    mhz = "mHz"
    uhz = "uHz"


class PERIOD(str, Enum):
    ks = "ks"
    s = "s"
    ms = "ms"
    us = "us"
    ns = "ns"


# 幅度
class VOLTAGE(str, Enum):
    Vrms = 'Vrms'
    mVrms = 'mVrms'
    Vpp = 'Vpp'
    mVpp = "mVpp"


# 偏移
class OFFESET(str, Enum):
    V = "V"
    mv = "mV"


# 高电平电压
class HIGH(str, Enum):
    V = "V"
    mv = "mV"


# 低电平电压
class LOW(str, Enum):
    V = "V"
    mv = "mV"


# 设置波形相位
class PHASE(str, Enum):
    deg = "deg"


# SQUare:DCYCle方波占空比 25%

# 波形
class INPUT(BaseModel):
    output:bool
    function_type: FUNCTION
    voltage: float
    voltage_unit: VOLTAGE
    frequency_or_period:bool
    frequency: float
    frequency_unit: FREQUENCY
    period: float
    period_unit: PERIOD
    offset: float
    offset_unit: OFFESET
    phase: float
    dcycle: float


# 目前只有单通道
@app.post("/tfg6930a/")
def set_signal_generator(input:INPUT,response:Response):
    try:
        rm = visa.ResourceManager()
        dev = rm.open_resource("USB0::0x0451::0x3352::usbtmc.000::INSTR")
        dev.timeout = 10000
        print(dev.query('*idn?'))
        # 根据function type来进行操作
        # 首先设置波形
        dev.write("source1:function {}".format(input.function_type))
        # 使用频率还是周期
        if input.frequency_or_period:
            dev.write("source1:frequency {}{}".format(input.frequency,input.frequency_unit))
        else:
            dev.write("source1:period {}{}".format(input.period,input.period_unit))
        # 设置幅值
        dev.write("source1:voltage {}{}".format(input.voltage,input.voltage_unit))
        # 设置便宜
        dev.write("source1:offset {}{}".format(input.offset,input.offset_unit))
        # 设置相位
        dev.write("source1:phase {}deg".format(input.phase))
        # 如果等于方波才使用占空比
        if input.function_type == FUNCTION.square:
            dev.write("source1:function:square:dcycle {}%".format(input.dcycle))
        # 是否输出波形
        if input.output:
            print("output on")
            dev.write("output1 1")
        else:
            print("output off")
            dev.write("output1 0")
        # dev.query('*opc?')
    except Exception as e:
        print(e)
        response.status_code = 500
        return {'code': 500, 'message': "仪器出错了" + str(e)}
    else:
        return {'code': 200, 'message': "设置成功"}

