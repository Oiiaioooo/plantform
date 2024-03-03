"""Perform a voltage measurement using the Rigol DM3058."""

import dm3058


address = "USB0::0x1AB1::0x0588::DM3H134900658::INSTR"

# address = "ASRL2::INSTR"
# baud = 19200
# flow_control = 1
# term_char = "\n"

with dm3058.dm3058() as dmm:
    # dmm.connect(
    #     address,
    #     reset=True,
    #     baud_rate=baud,
    #     flow_control=flow_control,
    #     write_termination=term_char,
    #     read_termination=term_char,
    # )

    dmm.connect(address, reset=False)

    print(f"Connected to {dmm.get_id()}!\n")

    # # setup the dmm for dc voltage measurement
    # dmm.set_function("voltage", "dc")
    # dmm.enable_autorange(True)
    # dmm.set_dc_voltage_measurement_impedance("10G")
    # dmm.set_reading_rate("voltage", "dc", "S")
    #
    # input(
    #     "Connect a DC voltage source to the input of the DMM. Press Enter when "
    #     + "ready...\n"
    # )

    # perform the measurement
    voltage = dmm.measure("voltage", "dc")

    print(f"Measured voltage: {voltage} V")
