import logging
from pyModbusTCP.client import ModbusClient
from typing import List
from . import modbus_function_code 
from .object_factory import ModbusObject, get_modbus_object, get_modbus_object_from_range
from .function_argument import ReadFunctionArgument, WriteFunctionArgument

LOG = logging.getLogger(__name__)

class FunctionUnknow(Exception):
    pass

class ObjectNonWriteable(Exception):
    pass


class ModbusClientWrapper(ModbusClient):

    def __init__(self, host='localhost', port=502, unit_id=1, timeout=30.0,
                 debug=False, auto_open=True, auto_close=False):
        super().__init__(host, port, unit_id, timeout,
                 debug, auto_open, auto_close)
        
        self.function_map = {
            modbus_function_code.READ_COILS: self.read_coils,
            modbus_function_code.READ_HOLDING_REGISTERS: self.read_holding_registers,
            modbus_function_code.READ_DISCRETE_INPUTS: self.read_discrete_inputs,
            modbus_function_code.READ_INPUT_REGISTERS: self.read_input_registers,
            modbus_function_code.WRITE_SINGLE_COIL: self.write_single_coil,
            modbus_function_code.WRITE_SINGLE_HOLDING_REGISTER: self.write_single_register,
            modbus_function_code.WRITE_MULTIPLE_COILS: self.write_multiple_coils,
            modbus_function_code.WRITE_MULTIPLE_HOLDING_REGISTERS: self.write_multiple_registers
         }
        
    def read(self, modbus_numbers: List[int | str], *args, **kwargs) -> dict:
        modbus_objects = []

        for n in modbus_numbers:
            try: 
               range_entry =  "-" in n
            except TypeError:
                range_entry = False

            if range_entry:
                modbus_objects = modbus_objects + get_modbus_object_from_range(n)
            else:
                modbus_objects.append(get_modbus_object(n))

        self.read_modbus_objects(modbus_objects, *args, **kwargs)

        result = {obj.__repr__():obj.value.__repr__() for obj in modbus_objects}

        return result
    
    def read_modbus_objects(
            self, 
            modbus_objects: List[ModbusObject],  
            max_read_size: int = None, 
            read_mask: int = None,
            ) -> None:
        
        arguments = ReadFunctionArgument.get_arguments(
            modbus_objects,
            max_read_size=max_read_size, 
            read_mask=read_mask
            )

        self.open()

        for arg in arguments: self._read(arg)

        self.close()

    def write(self, modbus_numbers_with_values: dict) -> dict:
        modbus_objects = [get_modbus_object(n,v) for n,v in modbus_numbers_with_values.items()]

        self.write_modbus_objects(modbus_objects)

        result = {obj.__repr__():obj.value.__repr__() for obj in modbus_objects}

        return result

    def write_modbus_objects(self, modbus_objects: List[ModbusObject]):
        arguments = WriteFunctionArgument.get_arguments(
                                        modbus_objects,
                                        )

        self.open()

        for arg in arguments: 
            self._write(arg)

        self.close()
            
    def _write(self, write_argument: WriteFunctionArgument):
        write_function = self._get_function(write_argument.write_function_code)
        starting_address = write_argument.starting_address
        values_to_write = write_argument.values_to_write
        function_string = write_function.__doc__.splitlines()[0]
        LOG.debug (f'executing function: "{function_string}" for argument: "{write_argument}"')

        write_ok = write_function(starting_address, values_to_write)
        objects = write_argument.object_list.objects
        if write_ok:
            [obj.value.update(obj.value_to_write.value) for obj in objects]
        else:
            LOG.error(f'failed to write "{function_string}" for argument: "{write_argument}"')

        return write_ok
        
    def _get_function(self, code:[hex, int]):
        """Get modbus function by code"""
        try:
            function = self.function_map[code]
        except KeyError:
            raise FunctionUnknow(f"code {code} not valid")
        
        return function

    def _filter_modbus_type(self, object_type: ModbusObject, modbus_objects: List[ModbusObject]) -> List[ModbusObject]:
        is_type = lambda obj: type(obj)==object_type
        objects_to_read = filter(is_type, modbus_objects)

        return list(objects_to_read)

    def _get_read_size(self, modbus_class):
        try: 
            return next(
                value for cls, value in self.MAX_READ_SIZE.items() 
                if issubclass(modbus_class, cls)
                )
        except StopIteration:
            return None
    
    def _read(self, modbus_function_argument: ReadFunctionArgument) -> None:

        argument = modbus_function_argument

        collected_values = {}
        
        starting_address = argument.starting_address
        read_function_code = argument.object_list.type.FUNCTION_CODE.read
        read_function = self._get_function(read_function_code)
        function_string = read_function.__doc__.splitlines()[0]

        LOG.debug(f'executing function: "{function_string}" for argument "{argument}"')
        collected_values.update(
            {
            starting_address: read_function(starting_address, argument.size)
            }
        )
        LOG.debug(f'results: "{collected_values[starting_address]}"')

        if not collected_values[starting_address]: # None means no reply from modbus target
            LOG.error(f'{function_string} failed to read {argument}')
            collected_values[starting_address] = [None for i in range(0, argument.size)] # Fill all results with None, when no reply from Modbus target

        increment = 0
        for value in collected_values[starting_address]:
            collected_values[starting_address+increment] = value
            increment+=1

        for object in argument.object_list.objects:
            object.value.update(
                collected_values[object.address]
                )



    