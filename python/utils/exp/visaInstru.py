import pyvisa as visa
rm = visa.ResourceManager()
print(rm.list_resources())