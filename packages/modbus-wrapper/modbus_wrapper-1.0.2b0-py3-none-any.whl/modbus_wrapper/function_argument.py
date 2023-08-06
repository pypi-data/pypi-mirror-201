from dataclasses import dataclass
from typing import List, Type
from .objects import ModbusObject

class ModbusObjectListUniqueException(Exception):
    pass

class ModbusWriteValueException(Exception):
    pass

@dataclass
class ModbusObjectList:
    type: Type
    objects: List[ModbusObject]

    def __post_init__(self):
        for obj in self.objects:
            if type(obj) != self.type:
                raise ModbusObjectListUniqueException(f'Modbus object {obj} is not type of {self.objects_type}')


    @classmethod
    def get_single_type_objects(cls, modbus_objects: List[ModbusObject]) -> list:
        modbus_object_types = list({type(i) for i in modbus_objects})
        list_to_return = []
        for object_type in modbus_object_types:
            is_type = lambda obj: type(obj) == object_type
            single_type_modbus_objects = list(filter(is_type, modbus_objects))
            list_to_return.append(
                cls(object_type, single_type_modbus_objects)
            )
        return list_to_return

class FunctionArgument:
    def _calculate_read_size(addresses, max_read_size: int = 1, read_mask: int = 1) -> List[dict]:
        results = []
        done_list = set()
        addresses  = sorted(addresses)

        for i in range(len(addresses)):
            if addresses[i] not in done_list:

                result_addresses = []
                read_size = 1
                starting_address = addresses[i]
                result_addresses.append(starting_address)
                remain_addresses = addresses[i+1:]
                _read_mask = read_mask
                for remain_address in remain_addresses:
                    prev_elemet_diff = remain_address - starting_address
                    if (
                        prev_elemet_diff <= _read_mask 
                        and prev_elemet_diff + 1 <= max_read_size
                    ):
                            read_size = prev_elemet_diff + 1
                            done_list.add(remain_address)
                            result_addresses.append(remain_address)
                    _read_mask +=1
                
                results.append({"starting_address" : starting_address,
                                "size" : read_size,
                                "addresses": result_addresses
                                }
                               )
        return results


@dataclass
class ReadFunctionArgument(FunctionArgument):
    starting_address: int
    size: int
    object_list: ModbusObjectList

    @classmethod
    def get_arguments(
            cls,
            modbus_objects: List[ModbusObject], 
            max_read_size: int = None, 
            read_mask: int = None
    ) -> list:
        """Function to get read arguments for modbus function from Modbus Objects"""

        single_type_obj_list = ModbusObjectList.get_single_type_objects(modbus_objects)
        arguments = []
        for single_type in single_type_obj_list:
            addresses = [obj.address for obj in single_type.objects]
            _max_read_size = max_read_size if max_read_size else single_type.type.MAX_READ_SIZE
            _read_mask = read_mask if read_mask else single_type.type.READ_MASK
            calculated_read_sizes = cls._calculate_read_size(
                addresses, 
                max_read_size=_max_read_size, 
                read_mask=_read_mask
                )

            for result in calculated_read_sizes:
                staring_address = result["starting_address"]
                size = result["size"]
                addresses = result["addresses"]
                object_list = ModbusObjectList(
                    single_type.type,
                    [obj for obj in single_type.objects if obj.address in addresses]
                )
                argument = cls(staring_address, size, object_list)
                arguments.append(argument)

        return arguments

@dataclass
class WriteFunctionArgument(FunctionArgument):
    starting_address: int
    values_to_write: List[int | bool] | int | bool
    write_function_code: int
    object_list: ModbusObjectList


    @classmethod
    def get_arguments(cls, modbus_objects: List[ModbusObject], max_write_size: int = None):
        """Function to get read arguments for modbus function from Modbus Objects"""

        arguments = []
        single_type_obj_list = ModbusObjectList.get_single_type_objects(modbus_objects)

        for single_type in single_type_obj_list:
            addresses = [obj.address for obj in single_type.objects]
            max_write_size = max_write_size if max_write_size else single_type.type.MAX_READ_SIZE
            read_mask = 1
            calculated_write_sizes = cls._calculate_read_size(
                addresses, 
                max_read_size=max_write_size, 
                read_mask=read_mask
                )

            for write in calculated_write_sizes:
                number_of_values_to_write = write['size']
                starting_address = write['starting_address'] 
                ending_address = starting_address + number_of_values_to_write
                get_write_value_for_address = lambda address: next(
                        obj.write.value
                        for obj in single_type.objects 
                        if obj.address == address
                        )
                get_objets_for_address = lambda address: next(obj for obj in single_type.objects if obj.address == address)
                addresses_range = range(starting_address, ending_address)

                values_to_write = list(
                    map(get_write_value_for_address, addresses_range)
                    )

                single_value_to_write = len(values_to_write) == 1
                if single_value_to_write:
                    values_to_write=values_to_write[0]
                    write_function_code=single_type.type.FUNCTION_CODE.write
                else:
                    write_function_code=single_type.type.FUNCTION_CODE.multi_write

                object_list = ModbusObjectList(
                    single_type.type,
                    list(map(get_objets_for_address, addresses_range))
                )

                arguments.append(WriteFunctionArgument(
                    starting_address,
                    object_list=object_list,
                    write_function_code=write_function_code,
                    values_to_write=values_to_write
                    )
                )

        return arguments

        
        