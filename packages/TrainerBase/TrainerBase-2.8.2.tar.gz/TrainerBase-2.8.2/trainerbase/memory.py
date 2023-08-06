import typing
import pymem
import config


for process_name in config.PROCESS_NAMES:
    try:
        pm = pymem.Pymem(process_name)
    except pymem.exception.ProcessNotFound:
        continue
    break
else:
    raise pymem.exception.ProcessNotFound(f"not any: {config.PROCESS_NAMES}")


ARCH = 32 if pm.is_WoW64 else 64
POINTER_SIZE = 4 if pm.is_WoW64 else 8

read_pointer = pm.read_uint if pm.is_WoW64 else pm.read_longlong


class Address:
    def __init__(self, address: int, offsets: list[int] = None, add: int = 0):
        self.address = address
        self.offsets = [] if offsets is None else offsets
        self.add = add

    def inherit(self, *, extra_offsets: list = None, new_add: int = None) -> typing.Self:
        new_address = Address(self.address, self.offsets.copy(), self.add)

        if extra_offsets is not None:
            new_address.offsets.extend(extra_offsets)

        if new_add is not None:
            new_address.add = new_add

        return new_address

    def resolve(self):
        pointer = self.address
        for offset in self.offsets:
            pointer = read_pointer(pointer) + offset

        return pointer + self.add


def make_address(address: typing.Union[Address, int]):
    if isinstance(address, Address):
        return address
    else:
        return Address(address)
