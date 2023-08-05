from dataclasses import dataclass
from typing import Union
from .. import modbus_function_code
from .config import MaxReadSize, ReadMask, MaxWriteSize
from .modbus_value import RegisterValue, CoilValue


@dataclass
class FunctionCode:
    read: Union[int, hex]
    write: Union[int, hex] = None
    multi_write: Union[int, hex] = None

@dataclass
class TargetRangeInt:
    low: int
    high: int


@dataclass
class TargetRangeBool:
    value : bool
    

class ModbusObject:
    """Modbus object basic class"""

    def __init__(
            self, modbus_number: int,
            value_to_write: int | bool = None,
            target_range: TargetRangeInt | TargetRangeBool = None
        ):
        self.number = modbus_number
        self.value_to_write = self.VALUE_CLS(value_to_write)
        self.value = self.VALUE_CLS()
        self.target_range = target_range

    def __repr__(self):
        return str(self.number)

    @property
    def address(self):
        "Method to obtain address from modbus object number"
        first_modbus_number = self.MOBUS_NUMBER_RANGE[0]
        return self.number - first_modbus_number


class Coil(ModbusObject):
    """Coil modbus object """
    MAX_READ_SIZE = MaxReadSize.COIL
    READ_MASK = ReadMask.COIL
    MAX_WRITE_SIZE = MaxWriteSize.COIL
    MOBUS_NUMBER_RANGE = range(1,65537)
    NUMBER_RANGE = MOBUS_NUMBER_RANGE
    NUMBER_RANGE_FAST = set(MOBUS_NUMBER_RANGE)
    FUNCTION_CODE = FunctionCode(
        modbus_function_code.READ_COILS,
        modbus_function_code.WRITE_SINGLE_COIL,
        modbus_function_code.WRITE_MULTIPLE_COILS
    )
    VALUE_CLS = CoilValue


class DiscreteInput(ModbusObject):
    """Discrete Input modbus object """
    MAX_READ_SIZE = MaxReadSize.DISCRETE_INPUT
    READ_MASK = ReadMask.DISCRETE_INPUT
    MAX_READ_SIZE = 2000
    MOBUS_NUMBER_RANGE = range(100001,165537)
    NUMBER_RANGE = MOBUS_NUMBER_RANGE
    NUMBER_RANGE_FAST = set(MOBUS_NUMBER_RANGE)
    FUNCTION_CODE = FunctionCode(
        modbus_function_code.READ_DISCRETE_INPUTS,
    )
    VALUE_CLS = CoilValue


class InputRegister(ModbusObject):
    """Input Register modbus object """
    MAX_READ_SIZE = MaxReadSize.INPUT_REGISTER
    READ_MASK = ReadMask.INPUT_REGISTER
    MOBUS_NUMBER_RANGE = range(300001,365537)
    NUMBER_RANGE = MOBUS_NUMBER_RANGE
    NUMBER_RANGE_FAST = set(MOBUS_NUMBER_RANGE)
    FUNCTION_CODE = FunctionCode(
        modbus_function_code.READ_INPUT_REGISTERS,
    )
    VALUE_CLS = RegisterValue


class HoldingRegister(ModbusObject):
    """Holding Register modbus object """
    MAX_READ_SIZE = MaxReadSize.HOLDING_REGISTER
    READ_MASK = ReadMask.HOLDING_REGISTER
    MAX_WRITE_SIZE = MaxWriteSize.HOLDING_REGISTER
    MOBUS_NUMBER_RANGE = range(400001,465537)
    NUMBER_RANGE = MOBUS_NUMBER_RANGE
    NUMBER_RANGE_FAST = set(MOBUS_NUMBER_RANGE)
    FUNCTION_CODE = FunctionCode(
        modbus_function_code.READ_HOLDING_REGISTERS,
        modbus_function_code.WRITE_SINGLE_HOLDING_REGISTER,
        modbus_function_code.WRITE_MULTIPLE_HOLDING_REGISTERS,
    )
    VALUE_CLS = RegisterValue





