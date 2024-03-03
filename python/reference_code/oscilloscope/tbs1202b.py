# tbs simple plot
# python v3.x, pyvisa v1.8
# should work with TDS2k, TPS2k, and TBS1k series

# replaced 'wfmoutpre' with 'wfmpre' (see mdo simple plot)
# https://github.com/caldarolamartin/hyperion/blob/19d6d2041f5029cd33da86c095d76e19ce89fcac/hyperion/controller/tektronix/simple_TBS1202B.py
import time # std module
import pyvisa as visa # http://github.com/hgrecco/pyvisa
import pylab as pl # http://matplotlib.org/
import numpy as np # http://www.numpy.org/


class tbs1202b():
    def __init__(self,visa_address):
        self.rm = visa.ResourceManager()
        self.scope = self.rm.open_resource(visa_address)
    
    def get_curve(self,ch):
        self.scope.timeout = 10000 # ms
        self.scope.encoding = 'latin_1'
        self.scope.read_termination = '\n'
        self.scope.write_termination = None
        # clear ESR(event status register 0b00000000)
        self.scope.write('*cls')
        # Returns the oscilloscope identification code in IEEE 488.2 notation.
        print(self.scope.query('*idn?'))
        
        # input("""
        # ACTION:
        # Connect probe to oscilloscope Channel 1 and the probe compensation signal.
        #
        # Press Enter to continue...
        # """)
        # reset
        self.scope.write('*rst')
        t1 = time.perf_counter()
        # opc命令可以使得示波器的操作与程序同步，即当所有待定命令完成时，将opc(operation complete message)写入ESR
        r = self.scope.query('*opc?')
        t2 = time.perf_counter()
        print('reset time: {} s'.format(t2 - t1))

        # autoset,如果两个通道相差太多，则显示会受影响
        self.scope.write('autoset EXECUTE')
        t3 = time.perf_counter()
        r = self.scope.query('*opc?') # sync
        t4 = time.perf_counter()
        print('autoset time: {} s'.format(t4 - t3))

        # autorange
        # t3 = time.perf_counter()
        # self.scope.write('autorange:setting both')
        # self.scope.write('autorange:state on')
        # self.scope.query('*opc?')
        # self.scope.write('autorange:state off')
        # t4 = time.perf_counter()
        # print('autorange time: {} s'.format(t4 - t3))


        # io config
        # 设置和查询Response Header Enable State（响应标头启用状态），该状态会导致示波器在查询响应中包含或忽略标头
        # ON or <NR1> ≠ 0 sets the Response Header Enable State to true. This causes the oscilloscope to include headers on applicable query responses. You can then use the query response as a command.
        # OFF or <NR1> = 0 sets the Response Header Enable State to false. This causes the oscilloscope to omit headers on query responses so that only the argument is returned.
        self.scope.write('header 0')
        # 设置或查询波形数据的格式。此命令相当于设置WFMPre:ENCdg、WFMPre：BN_Fmt和WFMPref:BYT_Or。（见表2-35。）设置DATa:ENCdg值会导致相应的WFMPre值更新。设置WFMPre值会导致相应的DATa:ENCdg值更新。
        # RIBinary specifies signed integer data-point representation with the most
        # significant byte transferred first. This format results in the fastest data transfer rate
        # when DATa:WIDth is set to 2.
        self.scope.write('data:encdg RIBINARY')
        # channel
        self.scope.write('data:source {}'.format(ch))
        # first sample
        # Sets or queries the starting data point for waveform data transfers. This command
        # lets you transfer partial waveforms to and from the oscilloscope.
        self.scope.write('data:start 1')
        # Query the number of points in the curve transfer,因为start是1，默认一次transfer2500点，但是不同目标下的不一样，比如fft可能是1024
        record = int(self.scope.query('wfmpre:nr_pt?'))
        # last sample
        self.scope.write('data:stop {}'.format(record))
        # 1 byte per sample
        # Set or query the preamble byte width of waveform points
        # Sets or queries the data width for the waveform to be transferred. This command
        # is equivalent to DATa:WIDth. Changing WFMPre:BYT_Nr also changes
        # WFMPre:BIT_Nr and DATa:WIDth.
        # <NR1> is an integer in the range of 1 to 2 that sets the number of bytes per point.
        self.scope.write('wfmpre:byt_nr 1')
        
        # acq config
        # Starts or stops oscilloscope acquisitions. This command is the equivalent of
        # pressing the front-panel RUN/STOP button. If ACQuire:STOPAfter is set to
        # SEQuence, other signal events may also stop acquisition.
        # NOTE. The best way to determine when a single sequence acquisition is complete
        # is to use *OPC rather than ACQuire:STATE.
        self.scope.write('acquire:state 0') # stop
        # If ACQuire:STOPAfter is set to
        # SEQuence, other signal events may also stop acquisition.
        self.scope.write('acquire:stopafter SEQUENCE') # single
        self.scope.write('acquire:state 1') # run
        t5 = time.perf_counter()
        r = self.scope.query('*opc?') # sync
        t6 = time.perf_counter()
        print('acquire time: {} s'.format(t6 - t5))
        
        # data query
        t7 = time.perf_counter()
        # 以二进制或ASCII格式将示波器波形数据传输到示波器或从示波器传输。传输的每个波形都有一个相关的波形前导码，其中包含数据格式和比例等信息。有关波形前导码的信息，请参阅WFMPre？。数据格式由data:ENCdg和data:WIDth命令指定。
        #
        # 曲线？query将数据从示波器发送到外部设备。数据源由data:source命令指定。传输的第一个和最后一个数据点由data:STARt和data:STOP命令指定。
        bin_wave = self.scope.query_binary_values('curve?', datatype='b', container=np.array, chunk_size = 1024**2)
        t8 = time.perf_counter()
        print('transfer time: {} s'.format(t8 - t7))
        
        # retrieve scaling factors
        # 此命令的设置形式指定DATa:DESTination命令指定的参考波形样本之间的间隔（非FFT为每点秒，FFT为每个点赫兹）。当显示参考波形时，示波器使用此值计算状态栏中显示的秒/分度或赫兹/分度单位以及光标读数。如果DATa:SOUrce命令指定的波形样本处于活动状态或显示状态，则查询表单返回该波形样本之间的间隔。如果该波形未激活或未显示，则查询失败，示波器生成执行错误，事件代码为2244（请求的波形未激活）。
        # <NR3> is the interval between points in the waveform record, in the units specified
        # by WFMPre:XUNit. Note that at some fast sweeps, some points in the waveform
        # record are produced by interpolation.
        # 采样点之间的时间间隔
        tscale = float(self.scope.query('wfmpre:xincr?'))
        # The set form of this command specifies the position, in XUNits, of the first sample of the reference_code waveform specified by the DATa:DESTination command, relative to the trigger.
        # The query form returns the position of the first sample of the waveform specified by the DATa:SOUrce command, if that waveform is active or displayed.
        # If that waveform is not active or displayed, the query fails and the oscilloscope generates an execution error with event code 2244 (waveform requested is not active).
        # The oscilloscope sets WFMPre:XZEro to zero when:
        # The display mode is set to XY.
        # The DATa:SOUrce is set to MATH FFT when the waveform is acquired.
        # <NR3> is the position, in XUNits, of the first waveform sample.
        # 第一个样本的参考时间
        tstart = float(self.scope.query('wfmpre:xzero?'))
        # YMUlt is a value, expressed in YUNits per digitizer level, used to convert
        # waveform record values to YUNit values using the following formula (where
        # dl is digitizer levels):
        # <NR3> is the vertical scale factor, in YUNits (usually volts) per sample value.
        vscale = float(self.scope.query('wfmpre:ymult?')) # volts / level
        # <NR3> is a value, expressed in YUNits.
        voff = float(self.scope.query('wfmpre:yzero?')) # reference_code voltage
        print('voff',voff)
        # YOFf是一个以数字化仪电平表示的值，用于使用以下公式将波形记录值转换为YUNit值（其中dl是数字化仪电平）：
        vpos = float(self.scope.query('wfmpre:yoff?')) # reference_code position (level)
        
        # error checking
        r = int(self.scope.query('*esr?'))
        print('event status register: 0b{:08b}'.format(r))
        # 使示波器返回所有事件及其消息，并从事件队列中删除返回的事件。消息之间用逗号分隔。
        #
        # 使用*ESR？查询以启用要返回的事件。有关如何使用这些寄存器的完整描述，请参阅状态和事件部分。此命令类似于重复发送*EVMsg？对示波器的查询
        r = self.scope.query('allev?').strip()
        print('all event messages: {}'.format(r))
        

        
        # create scaled vectors
        # horizontal (time)
        # 样本点之间的间隔时间*样本点数量
        total_time = tscale * record
        
        tstop = tstart + total_time
        scaled_time = np.linspace(tstart, tstop, num=record, endpoint=False)
        # vertical (voltage)
        unscaled_wave = np.array(bin_wave, dtype='double') # data type conversion
        print(unscaled_wave[3])
        # 实际波形=(实际参考值-零电压参考值)*电压比例+零电压点，一个计算公式
        scaled_wave = (unscaled_wave - vpos) * vscale + voff
        self.scope.write('acquire:stopafter runstop')
        self.scope.write('acquire:state RUN')
        self.scope.query('*opc?')
        return {'time':scaled_time.tolist(),'wave':scaled_wave.tolist()}
    
    def close(self):
        self.scope.close()
        self.rm.close()