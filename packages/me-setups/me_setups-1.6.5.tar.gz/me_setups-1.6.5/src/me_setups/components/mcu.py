from __future__ import annotations

import select
import socket
import threading
import time
from enum import Enum
from typing import Any

from me_setups.components.comp import Component
from me_setups.components.eqs import EyeQ5


class McuType(Enum):
    MEAVES = "meaves"
    ADAM = "adam"
    ASR = "asr"


class Mcu(Component):
    _ip: str | None

    def __init__(
        self,
        pbc: str,
        port: str,
        mcu_type: McuType,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self.pbc = pbc
        super().__init__(pbc, port, *args, **kwargs)
        self.mcu_type = mcu_type
        self._ip = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.settimeout(5.0)

        self.lock = threading.Lock()

    @property
    def name(self) -> str:
        return f"MCUE_PBC_{self._pbcm}"

    @property
    def prompt(self) -> bytes:
        if self.mcu_type == McuType.MEAVES:
            return b"Shell>"
        elif self.mcu_type == McuType.ADAM:
            return b">>"
        elif self.mcu_type == McuType.ASR:
            return b">"
        else:
            raise NotImplementedError

    @property
    def ip(self) -> str:
        if self._ip is not None:
            return self._ip
        elif self.mcu_type == McuType.ADAM:
            return "192.168.19.16"
        elif self.mcu_type == McuType.MEAVES:
            return "192.168.19.20"
        else:
            raise NotImplementedError

    @ip.setter
    def ip(self, ip: str) -> None:
        self._ip = ip

    @property
    def port(self) -> int:
        if self.mcu_type == McuType.MEAVES:
            return 9995
        elif self.mcu_type == McuType.ADAM:
            return 4200
        else:
            raise NotImplementedError

    @property
    def address(self) -> tuple[str, int]:
        return self.ip, self.port

    @staticmethod
    def get_eq_name(which_eq: EyeQ5 | str) -> str:
        if isinstance(which_eq, str):
            return which_eq
        return f"EQ{which_eq.chip + 1}.{which_eq.mid}"

    def set_eq_bootmode(self, eq: EyeQ5 | str, mode: str) -> bool:
        eq_name = self.get_eq_name(eq)
        if self.mcu_type == McuType.ADAM:
            cmd = f"set -e {eq_name} -b {mode}"
        elif self.mcu_type in (McuType.MEAVES, McuType.ASR):
            cmd = f"set {eq_name} bootmode {mode}"
        else:
            raise NotImplementedError
        self.run_serial_cmd(cmd)
        return True

    def reset_eq(self, eq: EyeQ5 | str) -> bool:
        eq_name = self.get_eq_name(eq)
        if self.mcu_type == McuType.ADAM:
            cmd = f"reset -e {eq_name}"
        elif self.mcu_type in (McuType.MEAVES, McuType.ASR):
            cmd = f"reset {eq_name}"
        else:
            raise NotImplementedError
        self.run_serial_cmd(cmd)
        return True

    def set_eq_uboot(self, eq: EyeQ5 | str, status: str) -> bool:
        eq_name = self.get_eq_name(eq)
        if self.mcu_type == McuType.ADAM:
            cmd = f"set -e {eq_name} -u {status}"
        elif self.mcu_type == McuType.MEAVES:
            cmd = f"set {eq_name} uboot {status}"
        else:
            raise NotImplementedError
        self.run_serial_cmd(cmd)
        return True

    def run_socket_cmd(self, cmd: str) -> bytes:
        self.logger.debug(f"[socket] running cmd = {cmd!r}")
        cmd_b = cmd.encode()
        cmd_b += b"\n"
        with self.lock:
            assert self.socket.sendto(cmd_b, self.address) == len(cmd_b)
            time.sleep(0.1)
            response = self._get_response()
        return response

    def _get_response(self) -> bytes:
        result = b""
        while True:
            r, _, _ = select.select([self.socket], [], [], 0.1)
            if self.socket in r:
                feedback = self.socket.recv(1024)
                result += feedback
                time.sleep(0.01)
            else:
                break
        return result
