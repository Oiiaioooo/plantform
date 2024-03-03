"""Rigol DP3058 series digital multimeter control library.

The full instrument manual, including the programming guide, can be found at
https://www.rigolna.com/products/digital-multimeters/dm3000/.
"""
import pyvisa


rm = pyvisa.ResourceManager()


class dm3058:
    """Rigol DM3058 series multimeter instrument.

    Use the `connect()` method to open a connection to the instrument and instantiate
    the VISA resource attribute `instr` for an dm3058 instance. This attribute can be
    used to access all of the PyVISA attributes and methods for the resource.
    """

    def __enter__(self):
        """Enter the runtime context related to this object."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the runtime context related to this object.

        Make sure everything gets cleaned up properly.
        """
        # disconnect all devices
        self.disconnect()

    def connect(
        self, resource_name, reset=True, **resource_kwargs,
    ):
        """Conntect to the instrument and set remote mode.

        Parameters
        ----------
        resource_name : str
            Full VISA resource name, e.g. "ASRL2::INSTR", "GPIB0::14::INSTR" etc. See
            https://pyvisa.readthedocs.io/en/latest/introduction/names.html for more
            info on correct formatting for resource names.
        reset : bool, optional
            Reset the instrument to the built-in default configuration.
        resource_kwargs : dict
            Keyword arguments to be used to change instrument attributes after
            construction.
        """
        self.instr = rm.open_resource(resource_name, **resource_kwargs)

        if reset is True:
            self.reset()

    def disconnect(self):
        """Disconnect the instrument after returning to local mode."""
        self.instr.close()

    # --- IEEE488.2 common commands ---

    def get_id(self):
        """Get instrument identity string.

        Returns
        -------
        id : str
            Identification string.
        """
        return self.instr.query("*IDN?").strip("\n")

    def reset(self):
        """Reset the instrument to the factory default configuration."""
        self.instr.write("*RST")

    # --- FUNCtion commands---

    def get_function(self):
        """Query the current measurement function.

        Returns
        -------
        function : str
            Current measurment function.
        """
        return self.instr.query(":FUNC?").strip("\n")

    def set_function(self, function, mode=None):
        """Set the current measurement function.

        Parameters
        ----------
        function : str
            Measurement function: voltage, current, resistance, frequency, period,
            continuity, diode, or capacitance.
        mode : str or None
            Mode of the measurement function. The valid modes for each function that
            has multiple modes are:
                voltage: dc (defualt), ac
                current: dc (defualt), ac
                resistance: 2-wire (defualt), 4-wire

            If `None`, the default mode is selected.
        """
        cmd = ":FUNC"

        if function == "voltage":
            cmd += ":VOLT"
            if (mode is None) or (mode == "dc"):
                cmd += ":DC"
            elif mode == "ac":
                cmd += ":AC"
            else:
                raise ValueError(f"Invalid voltage mode: {mode}. Must be 'ac' or 'dc'.")
        elif function == "current":
            cmd += ":CURR"
            if (mode is None) or (mode == "dc"):
                cmd += ":DC"
            elif mode == "ac":
                cmd += ":AC"
            else:
                raise ValueError(f"Invalid current mode: {mode}. Must be 'ac' or 'dc'.")
        elif function == "resistance":
            if (mode is None) or (mode == "2-wire"):
                cmd += ":RES"
            elif mode == "4-wire":
                cmd += ":FRES"
            else:
                raise ValueError(
                    f"Invalid resistance mode: {mode}. Must be '2-wire' or '4-wire'."
                )
        elif function == "frequency":
            cmd += ":FREQ"
        elif function == "period":
            cmd += ":PER"
        elif function == "continuity":
            cmd += ":CONT"
        elif function == "diode":
            cmd += ":DIOD"
        elif function == "capacitance":
            cmd += ":CAP"
        else:
            raise ValueError(
                f"Invalid function: {function}. Must be 'voltage', 'current', "
                + "'resistance', 'frequency', 'period', 'continuity', 'diode', or "
                + "'capacitance'."
            )

        self.instr.write(cmd)

    # --- MEASure commands---

    @property
    def new_data_acquired(self):
        """Query if new data has been acquired.

        Returns
        -------
        new_data_acquired : bool
            Flag indicating whether new data has been acquired.
        """
        ret = self.instr.query(":MEAS?").strip("\n")

        if ret == "TRUE":
            return True
        elif ret == "FALSE":
            return False
        else:
            raise ValueError(f"Unexpected response: {ret}. Expected 'TRUE' or 'FALSE'.")

    def enable_autorange(self, enable=True):
        """Enable measurement autoranging.

        Parameters
        ----------
        enable : boolean
            If `True`, measurement autoranging is enabled. If `False` a manual
            range setting can be used.
        """
        cmd = ":MEAS"

        if enable is False:
            cmd += " MANU"
        elif enable is True:
            cmd += " AUTO"
        else:
            raise ValueError(
                f"Invalid autorange enable setting: {enable}. Must be 'True' or "
                + "'False'."
            )

        self.instr.write(cmd)

    def set_measurement_range(self, function, mrange, mode=None):
        """Set the range for a measurement function.

        Parameters
        ----------
        function : str
            Measurement function: voltage, current, resistance, frequency, period,
            continuity, or capacitance.
        mode : str or None
            Mode of the measurement function. The valid modes for each function that
            has multiple modes are:
                voltage: dc (defualt), ac
                current: dc (defualt), ac
                resistance: 2-wire (defualt), 4-wire

            If `None`, the default mode is selected.
        mrange : int
            Integer corresponding to a range depending on the selected measurement
            function. See manual for valid values.
        """
        cmd = ":MEAS"

        if function == "voltage":
            cmd += ":VOLT"
            if (mode is None) or (mode == "dc"):
                cmd += ":DC"
            elif mode == "ac":
                cmd += ":AC"
            else:
                raise ValueError(f"Invalid voltage mode: {mode}. Must be 'ac' or 'dc'.")
        elif function == "current":
            cmd += ":CURR"
            if (mode is None) or (mode == "dc"):
                cmd += ":DC"
            elif mode == "ac":
                cmd += ":AC"
            else:
                raise ValueError(f"Invalid current mode: {mode}. Must be 'ac' or 'dc'.")
        elif function == "resistance":
            if (mode is None) or (mode == "2-wire"):
                cmd += ":RES"
            elif mode == "4-wire":
                cmd += ":FRES"
            else:
                raise ValueError(
                    f"Invalid resistance mode: {mode}. Must be '2-wire' or '4-wire'."
                )
        elif function == "frequency":
            cmd += ":FREQ"
        elif function == "period":
            cmd += ":PER"
        elif function == "continuity":
            cmd += ":CONT"
        elif function == "capacitance":
            cmd += ":CAP"
        else:
            raise ValueError(
                f"Invalid function: {function}. Must be 'voltage', 'current', "
                + "'resistance', 'frequency', 'period', 'continuity', or 'capacitance'."
            )

        cmd += f" {mrange}"

        self.instr.write(cmd)

    def get_measurement_range(self, function, mode=None):
        """Query the range for a measurement function.

        Parameters
        ----------
        function : str
            Measurement function: voltage, current, resistance, frequency, period,
            or capacitance.
        mode : str or None
            Mode of the measurement function. The valid modes for each function that
            has multiple modes are:
                voltage: dc (defualt), ac
                current: dc (defualt), ac
                resistance: 2-wire (defualt), 4-wire

            If `None`, the default mode is selected.
        """
        cmd = ":MEAS"

        if function == "voltage":
            cmd += ":VOLT"
            if (mode is None) or (mode == "dc"):
                cmd += ":DC"
            elif mode == "ac":
                cmd += ":AC"
            else:
                raise ValueError(f"Invalid voltage mode: {mode}. Must be 'ac' or 'dc'.")
        elif function == "current":
            cmd += ":CURR"
            if (mode is None) or (mode == "dc"):
                cmd += ":DC"
            elif mode == "ac":
                cmd += ":AC"
            else:
                raise ValueError(f"Invalid current mode: {mode}. Must be 'ac' or 'dc'.")
        elif function == "resistance":
            if (mode is None) or (mode == "2-wire"):
                cmd += ":RES"
            elif mode == "4-wire":
                cmd += ":FRES"
            else:
                raise ValueError(
                    f"Invalid resistance mode: {mode}. Must be '2-wire' or '4-wire'."
                )
        elif function == "frequency":
            cmd += ":FREQ"
        elif function == "period":
            cmd += ":PER"
        elif function == "capacitance":
            cmd += ":CAP"
        else:
            raise ValueError(
                f"Invalid function: {function}. Must be 'voltage', 'current', "
                + "'resistance', 'frequency', 'period', or 'capacitance'."
            )

        cmd += ":RANG?"

        return int(self.instr.query(cmd).strip("\n"))

    def set_dc_voltage_measurement_impedance(self, impedance="10M"):
        """Set the input impedance for DC voltage measurements.

        Parameters
        ----------
        impedance : str
            Input impedance:
                "10M" : 10 MOhms
                "10G" : > 10 GOhms
        """
        if impedance not in ["10M", "10G"]:
            raise ValueError(
                f"Invalid impedance setting: {impedance}. Must be '10M' or '10G'."
            )

        self.instr.write(f":MEAS:VOLT:DC:IMPE {impedance}")

    def get_dc_voltage_measurement_impedance(self):
        """Query the input impedance for DC voltage measurements.

        Returns
        -------
        impedance : str
            Input impedance:
                "10M" : 10 MOhms
                "10G" : > 10 GOhms
        """
        return self.instr.query(":MEAS:VOLT:DC:IMPE?").strip("\n")

    def set_ac_filter_state(self, function, state):
        """Set the AC filter state for DC voltage or current measurements.

        Parameters
        ----------
        function : str
            Measurement function: voltage or current.
        state : int
            AC filter state: 1 (on) or 0 (off).
        """
        cmd = ":MEAS"

        if function == "voltage":
            cmd += ":VOLT"
        elif function == "current":
            cmd += ":CURR"
        else:
            raise ValueError(
                f"Invalid function: {function}. Must be 'voltage' or 'current'"
            )

        if state not in [0, 1]:
            raise ValueError(
                f"Invalid filter state: {state}. Must be '1' (on) or '0' (off)."
            )

        cmd += f":DC:FILT {state}"

        self.instr.write(cmd)

    def get_ac_filter_state(self, function):
        """Get the AC filter state for DC voltage or current measurements.

        Parameters
        ----------
        function : str
            Measurement function: voltage or current.

        Returns
        -------
        state : int
            AC filter state: 1 (on) or 0 (off).
        """
        cmd = ":MEAS"

        if function == "voltage":
            cmd += ":VOLT"
        elif function == "current":
            cmd += ":CURR"
        else:
            raise ValueError(
                f"Invalid function: {function}. Must be 'voltage', or 'current'."
            )

        cmd += f":DC:FILT?"

        return int(self.instr.query(cmd).strip("\n"))

    def measure(self, function, mode):
        """Perform a measurement using the selected function.

        Parameters
        ----------
        function : str
            Measurement function: voltage, current, resistance, frequency, period,
            continuity, diode, or capacitance.
        mode : str or None
            Mode of the measurement function. The valid modes for each function that
            has multiple modes are:
                voltage: dc (defualt), ac
                current: dc (defualt), ac
                resistance: 2-wire (defualt), 4-wire

            If `None`, the default mode is selected.
        """
        cmd = ":MEAS"

        if function == "voltage":
            cmd += ":VOLT"
            if (mode is None) or (mode == "dc"):
                cmd += ":DC?"
            elif mode == "ac":
                cmd += ":AC?"
            else:
                raise ValueError(f"Invalid voltage mode: {mode}. Must be 'ac' or 'dc'.")
        elif function == "current":
            cmd += ":CURR"
            if (mode is None) or (mode == "dc"):
                cmd += ":DC?"
            elif mode == "ac":
                cmd += ":AC?"
            else:
                raise ValueError(f"Invalid current mode: {mode}. Must be 'ac' or 'dc'.")
        elif function == "resistance":
            if (mode is None) or (mode == "2-wire"):
                cmd += ":RES?"
            elif mode == "4-wire":
                cmd += ":FRES?"
            else:
                raise ValueError(
                    f"Invalid resistance mode: {mode}. Must be '2-wire' or '4-wire'."
                )
        elif function == "frequency":
            cmd += ":FREQ?"
        elif function == "period":
            cmd += ":PER?"
        elif function == "continuity":
            cmd += ":CONT?"
        elif function == "diode":
            cmd += ":DIOD?"
        elif function == "capacitance":
            cmd += ":CAP?"
        else:
            raise ValueError(
                f"Invalid function: {function}. Must be 'voltage', 'current', "
                + "'resistance', 'frequency', 'period', 'continuity', 'diode', or "
                + "'capacitance'."
            )

        return float(self.instr.query(cmd).strip("\n"))

    # --- RATE commands ----

    def set_reading_rate(self, function, mode=None, rate="S"):
        """Set the reading rate for a given measurement function.

        Parameters
        ----------
        function : str
            Measurement function: voltage, current, or resistance.
        mode : str or None
            Mode of the measurement function. The valid modes for each function that
            has multiple modes are:
                voltage: dc (defualt), ac
                current: dc (defualt), ac
                resistance: 2-wire (defualt), 4-wire

            If `None`, the default mode is selected.
        rate : str
            Reading rate: "S", "M", or "F" corresponding to slow, medium, or fast
            rates, respectively. The reading rate impacts the reading resolution, i.e.
            slower rates have higher resolution.
        """
        cmd = ":RATE"

        if function == "voltage":
            cmd += ":VOLT"
            if (mode is None) or (mode == "dc"):
                cmd += ":DC"
            elif mode == "ac":
                cmd += ":AC"
            else:
                raise ValueError(f"Invalid voltage mode: {mode}. Must be 'ac' or 'dc'.")
        elif function == "current":
            cmd += ":CURR"
            if (mode is None) or (mode == "dc"):
                cmd += ":DC"
            elif mode == "ac":
                cmd += ":AC"
            else:
                raise ValueError(f"Invalid current mode: {mode}. Must be 'ac' or 'dc'.")
        elif function == "resistance":
            if (mode is None) or (mode == "2-wire"):
                cmd += ":RES"
            elif mode == "4-wire":
                cmd += ":FRES"
            else:
                raise ValueError(
                    f"Invalid resistance mode: {mode}. Must be '2-wire' or '4-wire'."
                )
        else:
            raise ValueError(
                f"Invalid function: {function}. Must be 'voltage', 'current', "
                + "or 'resistance'."
            )

        if rate not in ["S", "M", "F"]:
            raise ValueError(f"Invalid rate: {rate}. Must be 'S', 'M', or 'F'.")

        cmd += f" {rate}"

        self.instr.write(cmd)

    def get_reading_rate(self, function, mode=None):
        """Query the reading rate for a given measurement function.

        This command is only valid if the queried function is the same as the currently
        selected measurement function.

        Parameters
        ----------
        function : str
            Measurement function: voltage, current, or resistance.
        mode : str or None
            Mode of the measurement function. The valid modes for each function that
            has multiple modes are:
                voltage: dc (defualt), ac
                current: dc (defualt), ac
                resistance: 2-wire (defualt), 4-wire

            If `None`, the default mode is selected.

        Returns
        -------
        rate : str
            Reading rate: "S", "M", or "F" corresponding to slow, medium, or fast
            rates, respectively. The reading rate impacts the reading resolution, i.e.
            slower rates have higher resolution.
        """
        cmd = ":RATE"

        if function == "voltage":
            cmd += ":VOLT"
            if (mode is None) or (mode == "dc"):
                cmd += ":DC?"
            elif mode == "ac":
                cmd += ":AC?"
            else:
                raise ValueError(f"Invalid voltage mode: {mode}. Must be 'ac' or 'dc'.")
        elif function == "current":
            cmd += ":CURR"
            if (mode is None) or (mode == "dc"):
                cmd += ":DC?"
            elif mode == "ac":
                cmd += ":AC?"
            else:
                raise ValueError(f"Invalid current mode: {mode}. Must be 'ac' or 'dc'.")
        elif function == "resistance":
            if (mode is None) or (mode == "2-wire"):
                cmd += ":RES?"
            elif mode == "4-wire":
                cmd += ":FRES?"
            else:
                raise ValueError(
                    f"Invalid resistance mode: {mode}. Must be '2-wire' or '4-wire'."
                )
        else:
            raise ValueError(
                f"Invalid function: {function}. Must be 'voltage', 'current', "
                + "or 'resistance'."
            )

        return self.instr.query(cmd).strip("\n")
