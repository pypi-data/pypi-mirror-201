from abc import ABC, abstractmethod
from pathlib import Path
from subprocess import run as run_executable, DEVNULL
from tempfile import TemporaryDirectory
from uuid import uuid4

from trainerbase.memory import ARCH, Address, pm, make_address


FASM_EXECUTABLE_PATH = Path(__file__).resolve().parent.parent / "fasm" / "FASM.EXE"


Code = bytes | str


class AbstractCodeInjection(ABC):
    DPG_TAG_PREFIX = "injection__"

    @abstractmethod
    def __init__(
        self,
        address: Address | int,
        code_to_inject: Code,
    ):
        self.address = make_address(address)
        self.code_to_inject = compile_asm(code_to_inject)
        self.dpg_tag = f"{self.DPG_TAG_PREFIX}{uuid4()}"

    @abstractmethod
    def inject(self):
        pass

    @abstractmethod
    def eject(self):
        pass


class CodeInjection(AbstractCodeInjection):
    def __init__(
        self,
        address: Address | int,
        code_to_inject: Code,
    ):
        super().__init__(address, code_to_inject)
        self.original_code: bytes = b""

    def inject(self):
        self.original_code = pm.read_bytes(self.address.resolve(), len(self.code_to_inject))
        pm.write_bytes(self.address.resolve(), self.code_to_inject, len(self.code_to_inject))

    def eject(self):
        pm.write_bytes(self.address.resolve(), self.original_code, len(self.original_code))


class AllocatingCodeInjection(AbstractCodeInjection):
    def __init__(
        self,
        address: Address | int,
        code_to_inject: Code,
        original_code_length: int = 0,
        new_memory_size: int = 1024,
    ):
        super().__init__(address, code_to_inject)
        self.original_code_length = original_code_length
        self.new_memory_size = new_memory_size
        self.original_code: bytes = b""
        self.new_memory_address: int = 0

    def __del__(self):
        if self.new_memory_address:
            self.eject()

    def inject(self):
        self.original_code = pm.read_bytes(self.address.resolve(), self.original_code_length)
        self.new_memory_address = pm.allocate(self.new_memory_size)

        jump_back = compile_asm(goto(self.address.resolve() + self.original_code_length))
        code_to_inject = self.code_to_inject + jump_back

        jump_to_new_mem = compile_asm(goto(self.new_memory_address))
        if len(jump_to_new_mem) < self.original_code_length:
            jump_to_new_mem += b"\x90" * (self.original_code_length - len(jump_to_new_mem))

        pm.write_bytes(self.new_memory_address, code_to_inject, len(code_to_inject))
        pm.write_bytes(self.address.resolve(), jump_to_new_mem, len(jump_to_new_mem))

    def eject(self):
        pm.write_bytes(self.address.resolve(), self.original_code, self.original_code_length)
        pm.free(self.new_memory_address)
        self.new_memory_address = 0


def compile_asm(code: Code) -> bytes:
    if isinstance(code, str):
        fasm_mode = f"use{ARCH}"
        with TemporaryDirectory() as tmp_dir:
            asm_file = Path(tmp_dir) / "injection.asm"

            asm_file.write_text(f"{fasm_mode}\n{code}", encoding="utf-8")

            run_executable([FASM_EXECUTABLE_PATH, asm_file], stdout=DEVNULL)
            code = asm_file.with_suffix(".bin").read_bytes()

    if not isinstance(code, bytes):
        raise TypeError("code must be bytes | str")

    return code


def goto(address: int) -> str:
    return f"""
            push {address}
            ret
        """
