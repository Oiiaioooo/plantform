"""
Rigol VISA Module

This module contains classes and functions for interfacing with Rigol Test
Equipment. Currently supported devices are:

- DP832 Programmable Power Supply
https://fixturfab.com/articles/controlling-rigol-dp832-using-pyvisa/
or https://github.com/kearneylackas/DP832-Python/blob/master/DP832.py
根据第二个链接，也许在每个操作指令后面都最好加上一个time.sleep(0.01)
"""

import logging
# from visa import ResourceManager
from pyvisa import ResourceManager

class DP(object):
    """
    Generic Rigol DPxxx Power Supply

    This class serves as the base for a controller of a Rigol DPxxx series
    programmable power supply. To create a controller class for a specific
    power supply, inherit from this class, and then implement the
    `channel_check` function to verify that the provided channel number is
    supported by the power supply.
    """
    def __init__(self, dev_name: str, backend: str = ""):
        """
        Initialize the Rigol Programmable Power Supply

        :param dev_name: Device name as shown in the USB device tree
        :type dev_name: str
        :param backend: VisaLibrary spec string
        :type backend: str
        """
        self.rm = ResourceManager(backend)
        self.instrument_list = self.rm.list_resources()
        logging.debug(f"instruments: {self.instrument_list}")
        self.address = None
        for elem in self.instrument_list:
            if elem.find(dev_name) != -1:
                self.address = elem

        # Check that a VISA device was found
        if self.address is None:
            raise IOError("No VISA devices found")
        # , read_termination="\n"删掉了括号里的这个东西，不知道为啥要删除，之前确实可以用，可能是visa版本的问题
        self.device = self.rm.open_resource(self.address)

    def channel_check(self, channel):
        """
        Implemented by each power supply model to verify that the channel 
        specified actually exists for the given model
        """
        assert NotImplementedError

    def close(self):
        """
        Close the opened DP832 device and the VISA resource manager
        """
        self.device.close()
        self.rm.close()

    def identify(self) -> dict:
        """
        Query the ID string of the instrument

        :return: Dictionary containing the manufacturer, instrument model,
                 serial number, and version number.
        :rtype: dict
        """
        id_str = self.device.query("*IDN?").strip().split(",")
        logging.debug(f"id_str: {id_str}")
        return {
            "manufacturer": id_str[0],
            "model": id_str[1],
            "serial_number": id_str[2],
            "version": id_str[3]
        }

    def get_output_mode(self, channel: int) -> str:
        """
        Query the current output mode of the specified channel

        DP800 series power supplies provide three output modes, including CV
        (constant voltage), CC (constant current), and UT (unregulated). In CV
        mode, the output voltage equals the voltage setting value and the
        output current is determined by the load. In CC mode, the output
        current equals the current setting value and the output voltage is
        determined by the load. UR mode is the critical mode between CC and CV
        modes.

        :param channel: Channel to get output state of, can be 1, 2, or 3.
        :type channel: int
        :return: Output mode string, CC, CV, or UR
        :rtype: str
        """
        self.channel_check(channel)
        return self.device.query(f":OUTP:MODE? CH{channel}").strip()

    def get_ocp_alarm(self, channel: int = "") -> bool:
        """
        Query whether OCP occurred on the specified channel.

        Overcurrent protection (OCP) refers to that the output turns off
        automatically when the actual output current of the channel exceeds the
        overcurrent protection value.

        The clear_ocp_alarm function can be used to clear this alarm on the
        specified channel.

        If the channel number is omitted, the OCP alarm state of the current
        channel is returned.

        :param channel: Channel to get OCP alarm start of, can be 1, 2, or 3
        :type channel: int
        :return: Alarm state, True or False
        :rtype: bool
        """
        self.channel_check(channel)

        if isinstance(channel, int):
            channel = f" CH{channel}"

        alarm_state = self.device.query(f":OUTP:OCP:ALAR?{channel}").strip()
        return alarm_state == "YES"

    def clear_ocp_alarm(self, channel: int = ""):
        """
        Clear the label of the overcurrent protection occurred on the specified
        channel.

        Before executing this command, make sure that the reason that causes
        the OCP on the specified channel is cleared (you can decrease the
        output current below the OCP value or increase the OCP value to be
        greater than the output current).

        If the channel number is omitted, the OCP alarm state of the current
        channel is returned.

        :param channel: Channel to OCP alarm of, can be 1, 2, or 3
        :type channel: int
        """
        self.channel_check(channel)

        if isinstance(channel, int):
            channel = f" CH{channel}"

        self.device.write(f":OUTP:OCP:CLEAR{channel}")

    def set_ocp_enabled(self, channel: int, state: bool):
        """
        Enable or disable overcurrent protection (OCP) of the specified channel

        When OCP is enabled, the output will turn off automatically when the
        output current exceeds the overcurrent protection value currently set.

        The overcurrent value can be set using the set_ocp_current function.

        If the channel number is omitted, the OCP enabled state of the current
        channel is set.

        :param channel: Channel to enable OCP on
        :type channel: int
        :param state: Enable/Disable OCP
        :type state: bool
        """
        self.channel_check(channel)

        if state:
            state = "ON"
        else:
            state = "OFF"

        self.device.write(f":OUTP:OCP CH{channel},{state}")

    def get_ocp_enabled(self, channel: int = "") -> bool:
        """
        Query the status of overcurrent protection (OCP) of the specified
        channel.

        If the channel number is omitted, the OCP enabled state of the current
        channel is returned.

        :param channel: Channel to get OCP state from
        :type channel: int
        :return: Enable/Disable state
        :rtype: bool
        """
        self.channel_check(channel)

        if isinstance(channel, int):
            channel = f" CH{channel}"

        state = self.device.query(f":OUTP:OCP?{channel}").strip()
        logging.debug(f"state: {state}")
        return state == "ON"

    def set_ocp_value(self, channel: int, setting: float):
        """
        Set the OCP value of the specified channel

        When OCP is enabled, the output will turn off automatically when the
        output current exceeds the overcurrent protection value currently set.

        :param channel: Channel to set OCP current of
        :type channel: int
        :param setting: Current setting in amps
        :type setting: float
        """
        self.channel_check(channel)
        self.device.write(f":OUTP:OCP:VAL CH{channel},{setting}")

    def get_ocp_value(self, channel: int) -> float:
        """
        Query the OCP value of the specified channel.

        If the channel number is omitted, the OCP current setting of the
        current channel is returned.

        :param channel: Channel to get OCP current setting from
        :type channel: int
        :return: Current settin in amps
        :rtype: float
        """
        self.channel_check(channel)

        if isinstance(channel, int):
            channel = f" CH{channel}"
        return float(self.device.query(f":OUTP:OCP:VAL?{channel}"))

    def get_ovp_alarm(self, channel: int = "") -> bool:
        """
        Query whether OVP occurred on the specified channel

        Overvoltage protection (OVP) refers to that the output turns off
        automatically when the actual output voltage of the channel exceeds the
        OVP value.

        If the channel number is omitted, the OVP alarm of the current channel
        is queried.

        :param channel: Channel to check OVP alarm on
        :type channel: int
        :return: True if the alarm is set, False if not
        :rtype: bool
        """
        self.channel_check(channel)

        if isinstance(channel, int):
            channel = f" CH{channel}"
        state = self.device.query(f":OUTP:OVP:ALAR?{channel}").strip()
        return state == "ON"

    def clear_ovp_alarm(self, channel: int = ""):
        """
        Clear the label of the overvoltage protection occurred on the specified
        channel.

        Before executing this command, make sure that the reason that causes
        the OCP on the specified channel is cleared (you can decrease the
        output voltage to below the OVP value or increase the OVP value to be
        greater than the output voltage).

        If the channel number is omitted, the OVP alarm of the current channel
        will be cleared.

        :param channel: Channel to clear OVP alarm on
        :type channel: int
        """
        self.channel_check(channel)

        if isinstance(channel, int):
            channel = f" CH{channel}"

        self.device.write(f":OUTP:OVP:CLEAR{channel}")

    def set_ovp_enabled(self, channel: int, state: bool):
        """
        Enable or disable OVP of the specified channel

        When OVP is enabled, the output will turn off automatically when the
        output voltage exceeds the OVP value that is currently set.

        :param channel: Channel to enable/disable OVP on
        :type channel: int
        :param state: Enable/Disable OVP
        :type state: bool
        """
        self.channel_check(channel)

        if state:
            state = "ON"
        else:
            state = "OFF"

        self.device.write(f":OUTP:OVP CH{channel},{state}")

    def get_ovp_enabled(self, channel: int = "") -> bool:
        """
        Query the status of OVP on the specified channel

        :param channel: Channel to check for overvoltage protection on.
        :type channel: int
        :return: True if OVP is enabled, False if not
        :rtype: bool
        """
        self.channel_check(channel)

        if isinstance(channel, int):
            channel = f" CH{channel}"

        state = self.device.query(f":OUTP:OVP?{channel}").strip()
        logging.debug(f"state: {state}")
        return state == "ON"

    def set_ovp_value(self, channel: int, setting: float):
        """
        Set the OVP value of the specified channel

        When OVP is enabled, the output will turn off automatically when the
        output voltage exceeds the overcurrent protection value currently set.

        :param channel: Channel to set OVP voltage of
        :type channel: int
        :param setting: Current setting in volts
        :type setting: float
        """
        self.channel_check(channel)

        self.device.write(f":OUTP:OVP:VAL CH{channel},{setting}")

    def get_ovp_value(self, channel: int) -> float:
        """
        Query the OVP value of the specified channel.

        If the channel number is omitted, the OVP voltage setting of the
        current channel is returned.

        :param channel: Channel to get OVP voltage setting from
        :type channel: int
        :return: Current setting in volts
        :rtype: float
        """
        self.channel_check(channel)

        if isinstance(channel, int):
            channel = f" CH{channel}"
        return float(self.device.query(f":OUTP:OVP:VAL?{channel}"))

    def set_output_state(self, channel: int, state: bool):
        """
        Enable or disable the output of the specified channel

        Make sure that the current settings will not affect the device
        connected to the power supply before enabling the channel output.

        :param channel: Channel to set enable state of
        :type channel: int
        :param state: True to enable, False to disable
        :type state: bool
        """
        if state:
            state = "ON"
        else:
            state = "OFF"
        self.device.write(f":OUTP:STAT CH{channel},{state}")

    def get_output_state(self, channel: int = "") -> bool:
        """
        Query the output status of the specified channel

        :param channel: channel to get enable state of
        :type channel: int
        :return: True if channel enabled, False if not
        :rtype: bool
        """
        self.channel_check(channel)

        if isinstance(channel, int):
            channel = f" CH{channel}"

        state = self.device.query(f":OUTP:STAT?{channel}").strip()
        return state == "ON"

    def set_channel_settings(self, channel, voltage, current):
        """
        Set voltage and current settings of the specified channel

        :param channel: channel to set settings of
        :type channel: int
        :param voltage: voltage to set (V)
        :type voltage: float
        :param current: current to set (A)
        :type current: float
        """
        self.channel_check(channel)
        self.device.write(f":APPL CH{channel},{voltage},{current}")

    def get_channel_settings(self, channel: int = "") -> dict:
        """
        Query the specified channels current settings

        Returns the voltage and current settings for the given channel.

        :param channel: Channel to return settings of
        :type channel: int
        :return: Dictionary containing the current and voltage settings
        :rtype: dict
        """
        self.channel_check(channel)

        if isinstance(channel, int):
            channel = f" CH{channel}"
        settings = self.device.query(f":APPL?{channel}").strip().split(",")
        return {
            "voltage": float(settings[-2]),
            "current": float(settings[-1])
        }

    def measure_current(self, channel):
        """
        Get the current measurement for the given channel

        :param channel: Channel to read current measurement from
        :type channel: int
        :return: Current measurement in A
        :rtype: float
        """
        self.channel_check(channel)

        meas = self.device.query(f":MEAS:CURR? CH{channel}").strip()
        return float(meas)

    def measure_voltage(self, channel):
        """
        Ger the voltage measurement for the given channel

        :param channel: Channel to read voltage measurement from
        :type channel: int
        :return: Current measurement in A
        :rtype: float
        """
        self.channel_check(channel)

        meas = self.device.query(f":MEAS? CH{channel}").strip()
        return float(meas)

    def measure_all(self, channel):
        """
        Get the voltage, current, and power measurements for the channel

        :param channel: Channel to read measurements from
        :type channel: int
        :return: dict
        """
        self.channel_check(channel)

        meas = self.device.query(f":MEAS:ALL? CH{channel}").strip().split(",")
        return {
            'voltage': float(meas[0]),
            'current': float(meas[1]),
            'power': float(meas[2])
        }


class DP712(DP):
    """
    Rigol DP712 Programmable Power Supply
    """
    def channel_check(self, channel):
        assert channel in [1, ""], f"Output channel {channel} not supported"


class DP821(DP):
    """
    Rigol DP821 Programmable Power Supply
    """
    def channel_check(self, channel):
        assert channel in [1, 2, ""], f"Output channel {channel} not supported"


class DP832(DP):
    """
    Rigol DP832 Programmable Power Supply
    """
    def channel_check(self, channel):
        assert channel in [1, 2, 3, ""], f"Output channel {channel} not supported"