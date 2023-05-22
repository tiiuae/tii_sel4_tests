import attr

from labgrid.factory import target_factory
from labgrid.driver import Driver, SerialDriver
from labgrid.driver.consoleexpectmixin import ConsoleExpectMixin
from labgrid.protocol import ConsoleProtocol
import logging

@target_factory.reg_driver
@attr.s(eq=False)
class MySerialDriver(SerialDriver):
    __double_n = False

    def set_double_n(self, state):
        """
        WAR for rpi4_vm_multi tests.
        Buildroot image need to be forced to send echo and
        last line promt.
        """
        self.__double_n = True if state else False

    def _write(self, data: bytes):
        """
        Writes 'data' to the serialport

        Arguments:
        data -- data to write, must be bytes
        """
        if self.__double_n:
            from time import sleep
            out = super()._write(data)
            sleep(1)
            out2 = super()._write(str.encode('\n'))
            sleep(1)
            return out + out2
        return super()._write(data)
