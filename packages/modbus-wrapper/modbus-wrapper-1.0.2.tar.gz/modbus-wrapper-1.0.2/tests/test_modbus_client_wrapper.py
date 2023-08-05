import unittest
from  modbus_wrapper.function_argument import FunctionArgument
from modbus_wrapper.object_factory import get_modbus_object


class TestCalculateReadSize(unittest.TestCase):
    modbus_objects =  [
        get_modbus_object(1),
        get_modbus_object(10),
        get_modbus_object(2),
        get_modbus_object(3),
        get_modbus_object(4),
        get_modbus_object(5),
        get_modbus_object(6),
        get_modbus_object(11),
        get_modbus_object(12),
        get_modbus_object(13),
    ]


    def test_max_read_size(self):
        modbus_objects = self.modbus_objects
        result = FunctionArgument._calculate_read_size(modbus_objects, max_read_size=5)
        breakpoint()
        assert result == [
            ModbusFunctionArgument(0,5), 
            ModbusFunctionArgument(5,1), 
            ModbusFunctionArgument(9,4), 
            ]

        result = FunctionArgument._calculate_read_size(modbus_objects, max_read_size=1)
        assert result == [
            ModbusFunctionArgument(0,1), 
            ModbusFunctionArgument(1,1), 
            ModbusFunctionArgument(2,1), 
            ModbusFunctionArgument(3,1), 
            ModbusFunctionArgument(4,1), 
            ModbusFunctionArgument(5,1), 
            ModbusFunctionArgument(9,1), 
            ModbusFunctionArgument(10,1), 
            ModbusFunctionArgument(11,1), 
            ModbusFunctionArgument(12,1), 
            ]

    # def test_mask(self):
    #     addresses = self.addresses
    #     result = ModbusClientWrapper._get_modbus_function_args(addresses, max_read_size=15, read_mask=1)
    #     assert result == [[1,6], [10,4]]

    #     result = ModbusClientWrapper._get_modbus_function_args(addresses, max_read_size=15, read_mask=3)
    #     assert result == [[1,6], [10,4]]

    #     result = ModbusClientWrapper._get_modbus_function_args(addresses, max_read_size=15, read_mask=4)
    #     assert result == [[1,13]]



if __name__ == '__main__':
    unittest.main()