# import dp832
# dp832 = dp832.DP832(dev_name="USB0::0x1AB1::0x0E11::DP8C175105606::INSTR")
# print(dp832.identify())
# dp832.set_channel_settings(1, 4, 1)
# dp832.set_output_state(1,False)
from pyvisa import ResourceManager
rm=ResourceManager()
print(rm.list_resources())