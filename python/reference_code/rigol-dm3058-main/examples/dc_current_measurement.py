"""Perform a voltage measurement using the Rigol DM3058."""

import pathlib
import sys

sys.path.insert(1, str(pathlib.Path.cwd().parent.joinpath("src")))
from multimeter import dm3058 as dm3058

address = "USB0::0x1AB1::0x0588::DM3R160300073::INSTR"

# address = "ASRL2::INSTR"
# baud = 19200
# flow_control = 1
# term_char = "\n"

with dm3058() as dmm:
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

    # setup the dmm for dc voltage measurement
    dmm.set_function("current", "dc")
    dmm.enable_autorange(True)
    dmm.set_reading_rate("current", "dc", "S")

    input(
        "Connect a DC current source to the input of the DMM. Press Enter when "
        + "ready...\n"
    )

    # perform the measurement
    current = dmm.measure("current", "dc")

    print(f"Measured current: {current} A")
