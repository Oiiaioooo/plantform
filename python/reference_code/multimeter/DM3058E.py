#author:lailai
import time
import pyvisa as visa
inst_wyb = visa.ResourceManager().open_resource('USB0::0x1AB1::0x0588::DM3H134900658::INSTR')
inst_wyb.write(":FUNCtion:VOLTage:DC")

def write_to_file():
    file_name = str(time.strftime("%Y-%m-%d %H-%M-%S", time.localtime()))
    result = open("%s.txt"% file_name, 'w')
    result.write('CURRENT_TIME\tVOLTAGE\n')
    result.close()
    while(True):
        result = open("%s.txt" % file_name, 'a')
        time_now = str(time.strftime("%Y%m-%d %H-%M-%S", time.localtime()))
        voltage = inst_wyb.query(":MEASure:VOLTage:DC?")
        result.write('%s\t' % time_now)
        result.write('%s' % voltage)
        result.close()
        time.sleep(0.5)

def print_value():
    voltage = inst_wyb.query(":MEASure:VOLTage:DC?")
    time_now = str(time.strftime("%Y%m-%d %H-%M-%S", time.localtime()))
    print(time_now,voltage)
while(True):
    print_value()