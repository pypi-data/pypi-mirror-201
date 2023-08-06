import logging
import sys
from djitellopy import Tello


class TelloMain(Tello):
    """
    Klasa z ogólnymi funkcjami, które mogą się przydać w przyszłości
    """

    def __init__(self, info_all=False):
        if not info_all:
            Tello.LOGGER.setLevel(logging.CRITICAL)
        super().__init__()

    def query_hardware(self):
        """

        :return: "RMTT" if using the Controller on top of the RMTT, or "TELLO", if using a Tello or RMTT without
        the controller.
        :rtype:
        """
        try:
            hardware = self.send_read_command('hardware?')
            if hardware == 'unknown command: hardware?':
                hardware = "TelloEDU"
        except Exception as exc:
            hardware = "TelloEDU"

        return hardware

    def get_speed(self) -> int:
        """Query speed setting (cm/s)
        This method is in the DroneBlocksTello class because the Tello class
        uses a different command that no longer seems supported.
        Returns:
            int: 1-100
        """
        speed_value = self.send_read_command('speed?')
        try:
            speed_value = int(float(speed_value))
            self.last_speed_value = speed_value
        except:
            speed_value = self.last_speed_value

        return speed_value


class TelloEDU(TelloMain):
    """

    Klasa przeznaczona dla dronów Tello-EDU (czarny)
    W metodzie D.connect() sprawdza, czy to taki dron
    """
    hardware_type = "TelloEDU"

    def __init__(self, info_all=False):
        """

        :param info_all: Czy ysyłać wszystkie informacje na ekran, True lub False (default)
        """
        super().__init__(info_all=info_all)

    def connect(self, wait_for_state=True) -> bool:
        connection_success = False
        hardware_ok = False
        hardware_probe = "xxxx"

        try:
            super().connect(wait_for_state=wait_for_state)
            connection_success = True
        except Exception as e:
            print(f"Błąd przy wywołaniu CONNECT: {e}")
            return False

        hardware_probe = self.query_hardware()
        if self.hardware_type == hardware_probe:
            hardware_ok = True
            print(f"Połączono z dronem typu {self.hardware_type}")
        else:
            print(f"Otrzymano: {repr(hardware_probe)} -> nie pasuje do {self.hardware_type}")

        return connection_success and hardware_ok


class RyzenTT(TelloMain):
    """
    Klasa przeznaczona dla dronów Ryzen-TT (czerwony)
    W metodzie D.connect() sprawdza, czy to taki dron
    W przyszłości pojawią się definicje metod
    """
    hardware_type = "RyzenTT"
    pass
