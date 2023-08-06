from __future__ import annotations

import contextlib
import logging
import pathlib
import sys
import threading
from datetime import datetime
from io import TextIOWrapper
from time import sleep
from types import TracebackType
from typing import Any
from typing import Generator

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

from serial import Serial
from serial import SerialException
from serial.threaded import LineReader

from me_setups.utils import filter_ansi_escape

logger = logging.getLogger(__name__)


def add_line_timestamp(line: str) -> str:
    """adds timestamp to a given line

    Args:
        line (str): line to add timestamp to

    Returns:
        str: the line with timestamp prefix - e.g. "[12:24:33.168423] <line>"
    """

    def timestamp() -> str:
        return datetime.now().strftime("[%H:%M:%S.%f]")

    return f"{timestamp()} {line}"


class Sniffer(LineReader):
    TERMINATOR = b"\n"
    log_file: TextIOWrapper | None

    def __init__(
        self,
        clean_line: bool = True,
        add_timestamp: bool = True,
    ) -> None:
        """Sniffer class for handling lines from serial

        Args:
            clean_line (bool, optional): remove escape characters . Defaults to True.
            add_timestamp (bool, optional): add time stamp to lines. Defaults to True.
        """
        super().__init__()
        self.clean_line = clean_line
        self.add_timestamp = add_timestamp
        self.log_file = None

    def handle_line(self, data: str) -> None:
        """handle line and write it to the log file if it is not None

        Args:
            data (str): line recived
        """
        if self.log_file is not None:
            if self.clean_line:
                data = filter_ansi_escape(data)
            if self.add_timestamp:
                data = add_line_timestamp(data)
            self.log_file.write(f"{data}\n")


class ReaderThread(threading.Thread):
    def __init__(self, serial: Serial, *args: Any, **kwargs: Any) -> None:
        """create a sniffing thread that allways reads the given serial

        Args:
            serial (Serial): serial port to read.
        """
        super().__init__(*args, **kwargs)
        self.daemon = True
        self.serial = serial

    def stop(self) -> None:
        """\
            Stop sniffing
        """
        self.alive = False
        self.join(5)

    def run(self) -> None:
        self.alive = True
        while self.alive and self.serial.is_open:
            try:
                self.serial.read(self.serial.in_waiting or 1)
            except SerialException:
                break
        self.alive = False

    def __enter__(self) -> ReaderThread:
        self.start()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None:
        self.stop()
        if exc_type or exc or traceback:
            return False
        else:
            return None


class SerialSniffer(Serial):
    sniff_thread: ReaderThread
    timeout: float

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """\
            Serial port with built in Sniffer.
        """
        super().__init__(*args, **kwargs)
        self.protocol = Sniffer()
        self._sniffing = False

    def read(self, size: int = 1) -> bytes:
        """read from serial and call the Sniffer protocol.

        Args:
            size (int, optional): size to read. Defaults to 1.

        Returns:
            bytes: data read from serail.
        """
        data = super().read(size)
        self.protocol.data_received(data)
        return data

    @contextlib.contextmanager
    def change_timeout_ctx(
        self,
        timeout: float,
    ) -> Generator[None, None, None]:
        """contextmanager for temporary change the serial timeout

        Args:
            timeout (float): the new timeout for the serial
        """
        orig_timeout = self.timeout
        try:
            self.timeout = timeout
            yield
        finally:
            self.timeout = orig_timeout

    def start_sniffing(self) -> ReaderThread:
        """start the sniffing thread

        Returns:
            ReaderThread: The sniffing thread
        """
        self.sniff_thread = ReaderThread(self)
        self.sniff_thread.start()
        self._sniffing = True
        return self.sniff_thread

    def stop_sniffing(self) -> None:
        """\
            Stops the Sniffing thread
        """
        if not self._sniffing:
            return None

        self.sniff_thread.stop()
        self._sniffing = False

    def config_sniffer(
        self,
        *,
        clean_line: bool = True,
        add_timestamp: bool = True,
    ) -> None:
        self.protocol.clean_line = clean_line
        self.protocol.add_timestamp = add_timestamp


class Component:
    def __init__(self, pbcm: str, port: str) -> None:
        """Base Component containing SerialSniffer by default

        Args:
            pbcm (str): pbcm for the Component
            port (str): path to the serial port.
        """
        self._pbcm = pbcm
        self.serial = SerialSniffer(port=port, baudrate=115200, timeout=5)
        self.logger = logging.getLogger(self.name)

    @property
    def prompt(self) -> bytes:
        raise NotImplementedError

    @property
    def name(self) -> str:
        return self._pbcm

    @contextlib.contextmanager
    def sniff(
        self,
        log_file: pathlib.Path | str,
        mode: Literal["w", "a"] = "a",
    ) -> Generator[None, None, None]:
        """contextmanager for sniffing the serial

        Args:
            log_file (pathlib.Path | str): path to log file.
            mode (Literal['w', 'a'], optional): like open(). Defaults to 'a'.
        """
        self.config_serial_log_file(log_file, mode)
        try:
            self.serial.start_sniffing()
            self.serial._sniffing = True
            yield
        finally:
            if self.serial._sniffing:
                self.serial.stop_sniffing()
            self.serial._sniffing = False

    def run_serial_cmd(self, cmd: str) -> None:
        """run command on the serial port. adds '\\n' at the end.

        Args:
            cmd (str): the command to run
        """
        self.logger.debug(f"[serial] running cmd: {cmd!r}")
        cmd_b = cmd.encode()
        cmd_b += b"\n"
        for b in cmd_b:
            self.serial.write(bytes([b]))
            sleep(0.01)
        sleep(0.4)

    def config_serial_log_file(
        self,
        log_file: pathlib.Path | str,
        mode: Literal["w", "a"] = "a",
    ) -> None:
        """config log file for the sniffer.

        Args:
            log_file (pathlib.Path | str): path for the log file.
            mode (Literal['w', 'a'], optional): like open(). Defaults to 'a'.
        """
        if self.serial._sniffing:
            self.serial.stop_sniffing()
            assert self.serial.protocol.log_file
            self.serial.protocol.log_file.close()

        self.logger.debug(f"configuring log file for serial - {str(log_file)!r}")
        log_file = pathlib.Path(log_file)
        log_file.parent.mkdir(parents=True, exist_ok=True)
        self.serial.protocol.log_file = log_file.open(mode, buffering=1)

    def wait_for_msg(self, msg: bytes, timeout: float) -> bytes:
        """waiting for serial msg, if sniffing in progress, it will stop it and restart
        when msg recived or timeout expired.

        Args:
            msg (bytes): msg to wait for.
            timeout (float): waiting timeout.

        Returns:
            bytes: all data that been read while waiting for the msg.
        """
        self.logger.debug(f"waiting for msg {msg.decode()!r}")

        restart_sniffing = False
        if self.serial._sniffing:
            restart_sniffing = True
            self.serial.stop_sniffing()

        with self.serial.change_timeout_ctx(timeout):
            if not self.serial.is_open:
                self.serial.open()
            res = self.serial.read_until(msg)

        if restart_sniffing:
            self.serial.start_sniffing()

        return res

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name})"
