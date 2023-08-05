from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Tuple
import wasmer # type: ignore

try:
    from typing import Protocol
except ImportError:
    class Protocol: # type: ignore
        pass


def _load(make_view: Callable[[], Any], mem: wasmer.Memory, base: int, offset: int) -> Any:
    ptr = (base & 0xffffffff) + offset
    view = make_view()
    if ptr + view.bytes_per_element > mem.data_size:
        raise IndexError('out-of-bounds load')
    view_ptr = ptr // view.bytes_per_element
    return view[view_ptr]

def _decode_utf8(mem: wasmer.Memory, ptr: int, len: int) -> str:
    ptr = ptr & 0xffffffff
    len = len & 0xffffffff
    if ptr + len > mem.data_size:
        raise IndexError('string out of bounds')
    view = mem.uint8_view()
    bytes = bytearray(view[ptr:ptr+len])
    x = bytes.decode('utf8')
    return x

def _encode_utf8(val: str, realloc: wasmer.Function, mem: wasmer.Memory) -> Tuple[int, int]:
    bytes = val.encode('utf8')
    ptr = realloc(0, 0, 1, len(bytes))
    assert(isinstance(ptr, int))
    ptr = ptr & 0xffffffff
    if ptr + len(bytes) > mem.data_size:
        raise IndexError('string out of bounds')
    view = mem.uint8_view()
    view[ptr:ptr+len(bytes)] = bytes
    return (ptr, len(bytes))
@dataclass
class Output:
    is_valid: bool
    error_message: str

class Polyvalid:
    instance: wasmer.Instance
    _canonical_abi_free: wasmer.Function
    _canonical_abi_realloc: wasmer.Function
    _is_app_name_valid: wasmer.Function
    _memory: wasmer.Memory
    def __init__(self, store: wasmer.Store, imports: dict[str, dict[str, Any]], module: wasmer.Module):
        self.instance = wasmer.Instance(module, imports)
        
        canonical_abi_free = self.instance.exports.__getattribute__('canonical_abi_free')
        assert(isinstance(canonical_abi_free, wasmer.Function))
        self._canonical_abi_free = canonical_abi_free
        
        canonical_abi_realloc = self.instance.exports.__getattribute__('canonical_abi_realloc')
        assert(isinstance(canonical_abi_realloc, wasmer.Function))
        self._canonical_abi_realloc = canonical_abi_realloc
        
        is_app_name_valid = self.instance.exports.__getattribute__('is-app-name-valid')
        assert(isinstance(is_app_name_valid, wasmer.Function))
        self._is_app_name_valid = is_app_name_valid
        
        memory = self.instance.exports.__getattribute__('memory')
        assert(isinstance(memory, wasmer.Memory))
        self._memory = memory
    def is_app_name_valid(self, name: str) -> 'Output':
        memory = self._memory;
        realloc = self._canonical_abi_realloc
        free = self._canonical_abi_free
        ptr, len0 = _encode_utf8(name, realloc, memory)
        ret = self._is_app_name_valid(ptr, len0)
        assert(isinstance(ret, int))
        load = _load(memory.uint8_view, memory, ret, 0)
        
        operand = load
        if operand == 0:
            boolean = False
        elif operand == 1:
            boolean = True
        else:
            raise TypeError("invalid variant discriminant for bool")
        load1 = _load(memory.int32_view, memory, ret, 4)
        load2 = _load(memory.int32_view, memory, ret, 8)
        ptr3 = load1
        len4 = load2
        list = _decode_utf8(memory, ptr3, len4)
        free(ptr3, len4, 1)
        return Output(boolean, list)
