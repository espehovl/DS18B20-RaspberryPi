import os
import glob
import time

class DS18B20:
    # Number of sensors currently active
    _instance_count = 0 
    
    # Initialize the sensors for reading
    os.system("modprobe w1-gpio")
    os.system("modprobe w1-therm")

    # Find the devices
    _devices = glob.glob("/sys/bus/w1/devices/28*")

    def __init__(self) -> None:
        self._device_file = self._devices[DS18B20._instance_count] + "/w1_slave"
        
        DS18B20._instance_count += 1

    def __del__(self) -> None:
        """ Decrement the instance counter upon destruction """
        DS18B20._instance_count -= 1

    @classmethod
    def get_devices(cls) -> list:
        """ Get the file locations of the devices on the bus. """
        return cls._devices

    def _read_raw_value(self) -> str:
        with open(self._device_file, "r") as f:
            raw: list = f.readlines()
        return raw

    def read_temperature(self) -> float:
        """ Read the temperature in degrees Celsius. """
        raw = self._read_raw_value()
        
        while raw[0].strip()[-3:].upper() != "YES":
            # Device is not ready
            time.sleep(0.5)
            raw = self._read_raw_value()

        try:
            value = float(raw[1].strip().split("t=")[1])/1000.0
            return value

        except ValueError as e:
            print(f"Error when reading temperature: {e}")
            return None


if __name__ == "__main__":
    sensor = DS18B20()
    print(f"T = {sensor.read_temperature()}{chr(0xB0)}C")
