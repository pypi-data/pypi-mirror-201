"""
There are some other fun things on the boards/ASICs that are useful to control

This controls those things

Ben Rotter
"""
import logging
import time

from naludaq.communication import readI2cResponse, sendI2cCommand
from naludaq.controllers.controller import Controller

logger = logging.getLogger("naludaq.peripherals")


class PeripheralsController(Controller):
    """The peripherals controller handles all the telemetry devices on the boards.

    Telemetry found on the boards is temperature, current, voltages, it also measures certain
    voltage rails.

    The specific telemetry available is highly board dependent.
    """

    def __init__(self, board):
        super().__init__(board)
        self._reader_functions = {
            "temp": self.read_temp_of_chip,
            "current": self.read_current_of_chip,
            "vadjn": self.read_vadjn,
            "vadjp": self.read_vadjp,
        }

    def read_temp_of_chip(self):
        """Reads out the AT30TS00 temp sensor and converts it to Celcius.

        Requires configuration, done in board_controller.init_board()

        Returns:
            Temperature of the chip in Celcius.
        """
        temp = 0
        response = self._request_temperature_readout()
        if response:
            temp = self._convert_response_to_temperature(response)

        logger.debug("Temperature: %s C", temp)

        return temp

    def _request_temperature_readout(self):
        """Reads the temperature register on the AT30TS00.

        Returns:
            A list of binary strings (including ACK bit).
        """
        board = self.board
        sendI2cCommand(self.board, "30", ["05"])
        sendI2cCommand(board, "31", ["FF", "FF"])
        return readI2cResponse(board)

    def _convert_response_to_temperature(self, response) -> float:
        """Converts the AT30TS00 temperature register response
        into a temperature in Celsius

        Args:
            response (list): I2C response registers.

        Returns:
            Temperature in Celsius.
        """
        reg_bits = response[1][:-1] + response[2][:-1]
        temp_bits = reg_bits[3:-1]
        sign_bit = temp_bits[0]

        # Negative temperatures are represented in 2's complement
        temp = int(temp_bits, 2)
        if sign_bit == "1":
            temp -= 1 << len(temp_bits)

        return temp / 8

    def read_current_of_chip(self):
        """Reads out the MCP3426 monitoring the current and converts to Ampere.

        Reads out the MCP3426 monitoring the current sense resistor, and converts
        it to a current in A.

        Returns:
            Current in Ampere.

        Raises:
            NotImplementedError if this functionality is not available for the current model.
        """
        voltage = self._request_readout("current")
        current = self._convert_voltage_to_current(voltage)
        logger.debug("Current Sense: %sA / %smV", current, voltage)
        return current

    def read_vadjn(self):
        """Read the vadjn voltage

        Raises:
            NotImplementedError if this functionality is not available for the current model.
        """
        voltage = self._request_readout("vadjn")
        logger.debug("VadjN: %smV", voltage)
        return voltage

    def read_vadjp(self):
        """Read the vadjp voltage

        Raises:
            NotImplementedError if this functionality is not available for the current model.
        """
        voltage = self._request_readout("vadjp")
        logger.debug("VadjP: %smV", voltage)
        return voltage

    def _request_readout(self, param):
        params = self._get_peripheral_params(param)
        return self._read_MCP3426_ADC(**params)

    def _get_peripheral_params(self, name: str) -> dict:
        """Gets the peripherals parameters for a given type of measurement.

        Args:
            param (str): the measurement name
        """
        try:
            params = self._board.params["peripherals"][name]
        except KeyError:
            raise NotImplementedError(
                f"{name} readout functionality has not been implemented for {self.board.model}"
            )
        return params

    def _read_MCP3426_ADC(self, chan, addr, bits=16, gain=1):
        """
        MCP3426/7/8, two on board (addr D0 and D8)

        command bits: RCCOSSGG
        R = "Ready Bit," initiates new conversion in one-shot mode
                         resets to 1 when new conversion is settled
        CC = Channel Selection
        O = Conversion Mode (1=continuous, 0=one-shot)
        SS = "Sample Rate" - b'00' 240sps (12bit)
                             b'01' 60sps  (14bit)
                             b'10' 15sps  (16bit)
        GG = "Gain Select" - b'00' 1x, b'01' 2x,
                             b'10' 4x, b'11' 8x
        """
        board = self.board

        bitmap = {
            16: "10",
            14: "01",
            12: "00",
        }.get(bits, None)
        if bitmap is None:
            raise ValueError("bits needs to be 16, 14, or 12, not %s", bits)

        gainmap = {
            1: "00",
            2: "01",
            4: "10",
            8: "11",
        }.get(gain, None)
        if gainmap is None:
            raise ValueError("gain needs to be 1, 2, 4, or 8, not %s", gain)

        command = "1" + "{0:b}".format(chan).zfill(2) + "1" + bitmap + gainmap
        sendI2cCommand(board, addr, [command])
        time.sleep(0.1)
        readaddr = "{0:X}".format(addr + 1)
        sendI2cCommand(board, readaddr, ["FF", "FF"])
        time.sleep(0.1)
        response = readI2cResponse(board)

        logger.info("response=%s", response)

        return self._convert_response_to_voltage(response, bits=bits, gain=gain)

    @staticmethod
    def _convert_response_to_voltage(response, bits, gain):
        """When the MCP3426 is operating in 16-bit mode, convert response to voltage.

        When in 16-bit mode LSB represents 62.5 uV. It is also using 8x gain.
        """
        step_size = 4096 / (2**bits)
        return (step_size / gain) * (
            int(response[1][:-1], 2) * (2**8) + int(response[2][:-1], 2)
        )

    def _convert_voltage_to_current(self, voltage):
        """Convert voltage to current by checking voltage drop over resistor.

        # Currently using a 50 mili-ohm resistor.
        # voltage is in mV, this should yield mA
        """

        resistance = self._get_v2a_resistance()
        return voltage / resistance

    def _get_v2a_resistance(self):
        """Default used to be 50mOhm"""
        return self.board.params.get("peripherals", {}).get("current_resistor", 50e-3)

    def read_all(self) -> dict:
        """Read all peripherals into a dict"""
        result = {}
        for name, func in self._reader_functions.items():
            try:
                value = func()
            except Exception:
                value = None
            result[name] = value
        return result
