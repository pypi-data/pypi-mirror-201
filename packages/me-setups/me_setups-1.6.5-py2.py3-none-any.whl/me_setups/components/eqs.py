from __future__ import annotations

import pathlib
import re
import subprocess
import time
from enum import Enum
from subprocess import CompletedProcess
from typing import Any

from me_setups.components.comp import Component


class CoreType(Enum):
    PCD = "pcd"
    FCD = "fcd"


class OSType(Enum):
    VOIS = "VOiS"
    UBOOT = "U-Boot"
    LINUX = "Linux"


PCD_WRITE_COMPLETE = b"CAUTION P-COREDUMP TO  EMMC COMPLETE !!"
FCD_WRITE_COMPLETE = b"OK"
LINUX_BOOT_MSG = b"Welcome to EyeQ5"
NO_KEY_CHECK = ["-o", "StrictHostKeyChecking=no", "-o", "LogLevel=FATAL"]
PROMPTS = {
    OSType.LINUX: b"# ",
    OSType.VOIS: b"VOiS>>",
    OSType.UBOOT: b"EyeQ5 # ",
}


class EyeQ5(Component):
    crash_folder = pathlib.Path("/media/storage/crash")

    def __init__(
        self,
        pbcm: str,
        port: str,
        os_type: OSType = OSType.LINUX,
    ) -> None:
        """class for working with EyeQ5 instance.

        Args:
            pbcm (str): pbcm of EyeQ e.g. (0001)
            port (str): serial port path e.g. (/dev/ttyUSB2)
            os_type (OSType, optional): The OS type of the EQ. Defaults to LINUX.
        """
        super().__init__(pbcm, port)
        self.os_type = os_type

    @property
    def name(self) -> str:
        """name of the EQ in this format - 'EQ5_PBCM_<pbcm>'

        Returns:
            str: the name of the EQ
        """
        return f"EQ5_PBCM_{self._pbcm}"

    @property
    def chip(self) -> int:
        """the chip of the EQ

        Returns:
            int: the chip of the EQ
        """
        return int(self._pbcm[-2])

    @property
    def mid(self) -> int:
        """the mid of the EQ

        Returns:
            int: the mid of the EQ
        """
        return int(self._pbcm[-1])

    @property
    def prompt(self) -> bytes:
        """The prompt for the EQ

        Returns:
            bytes: prompt of the EQ e.g. b'# '
        """
        return PROMPTS[self.os_type]

    @property
    def ip(self) -> str | None:
        """the IP of the EQ

        Returns:
            str | None: the EQ IP for the current OS
        """
        if self.name == "EQ5_PBCM_0000":
            if self.os_type == OSType.VOIS:
                return "169.254.0.11"
            else:
                return "192.168.19.129"

        elif self.name == "EQ5_PBCM_0001":
            if self.os_type == OSType.VOIS:
                return "169.254.0.12"
            else:
                return "192.168.19.113"

        elif self.name == "EQ5_PBCM_0010":
            if self.os_type == OSType.VOIS:
                return "169.254.0.13"
            else:
                return "192.168.19.105"

        elif self.name == "EQ5_PBCM_0011":
            if self.os_type == OSType.VOIS:
                return "169.254.0.14"
            else:
                return "192.168.19.121"

        else:
            raise NotImplementedError(f"ip for {self.name} is not implemented")

    @property
    def _ssh_root(self) -> str:
        return f"root@{self.ip}"

    def copy_from(
        self,
        src: pathlib.Path | str,
        dst: pathlib.Path | str,
        timeout: float = 5,
        recurcive: bool = False,
        mkdir: bool = False,
        **kwargs: Any,
    ) -> CompletedProcess[str]:
        """Copy files from EQ to local host

        Args:
            src (pathlib.Path | str): EQ path to the files
            dst (pathlib.Path | str): local path to copy to
            timeout (float, optional): timeout for the copy. Defaults to 5.
            recurcive (bool, optional): recurcive copy includs dirs. Defaults to False.

        Returns:
            CompletedProcess[str]: the process
        """
        if mkdir:
            pathlib.Path(dst).mkdir(parents=True, exist_ok=True)
        return self._scp(
            f"{self._ssh_root}:{src}",
            str(dst),
            timeout,
            recurcive,
            **kwargs,
        )

    def copy_to(
        self,
        src: pathlib.Path | str,
        dst: pathlib.Path | str,
        timeout: float = 5,
        recurcive: bool = False,
        mkdir: bool = False,
        **kwargs: Any,
    ) -> CompletedProcess[str]:
        """Copy files from local host to EQ

        Args:
            src (pathlib.Path | str): local path to the files
            dst (pathlib.Path | str): EQ path to copy to
            timeout (float, optional): timeout for the copy. Defaults to 5.
            recurcive (bool, optional): recurcive copy includs dirs. Defaults to False.

        Returns:
            CompletedProcess[str]: the process
        """
        dst = pathlib.Path(dst)
        if mkdir:
            self.run_ssh_cmd(f"mkdir -p {dst.parent}")
        return self._scp(
            str(src),
            f"{self._ssh_root}:{dst}",
            timeout,
            recurcive,
            **kwargs,
        )

    def copy_cores(self, dst: pathlib.Path | str) -> CompletedProcess[str] | None:
        """Extract cores from EQ

        Args:
            dst (pathlib.Path | str): Path to folder to extract to

        Returns:
            CompletedProcess[str] | None: status of extracting process None if no cores
        """
        cores = self.ssh_cmd_stdout("find /media/storage/crash/ -type f").splitlines()
        if not cores:
            return None
        if not all(core.endswith(".zip") for core in cores):
            self.wait_for_core_write(core_type=CoreType.PCD)
        return self.copy_from(
            f"{self.crash_folder}/*",
            pathlib.Path(dst) / self.name,
            timeout=300,
            recurcive=True,
            mkdir=True,
        )

    def wait_for_linux_boot(self) -> bool:
        """waits to Linux boot msg "Welcome to EyeQ5"

        Returns:
            bool: boot msg recived
        """
        boot_msg = b"Welcome to EyeQ5"
        return boot_msg in self.wait_for_msg(boot_msg, 120)

    def get_all_frames(self) -> list[str]:
        """get all frames ran from the app_log

        Returns:
            list[str]: list contain all frames that ran
        """
        frames_string = "running frame:"
        pat = re.compile(rf"{frames_string} (\d+)", re.IGNORECASE)
        stdout = self.ssh_cmd_stdout(
            f"grep -i {frames_string!r} /tmp/app_log.txt",
            skip_logging=True,
        )
        return pat.findall(stdout)

    def wait_for_frames(
        self,
        timeout: float = 180,
        frames: int = 10,
    ) -> bool:
        """waits for given number of frames

        Args:
            timeout (float, optional): how much time to wait. Defaults to 180.
            frames (int, optional): how many frames to wait for. Defaults to 10.

        Returns:
            bool: if we got the given number of frames
        """
        _timeout = time.time() + timeout
        all_frames = []
        while time.time() < _timeout:
            all_frames = self.get_all_frames()
            if all_frames:
                self.logger.debug(f"last frame is: {all_frames[-1]}")
            if len(all_frames) > frames:
                return True

        self.logger.warning(f"did not run {frames} frames. frames got={all_frames}")
        return False

    def is_mest_alive(self) -> bool:
        """Return if MEST is alive"""
        return self.ssh_cmd_stdout("pgrep cv_main_thread") != ""

    def is_alive(self, timeout: float = 1, frames: int = 10) -> bool:
        """Return if EQ is alive - MEST is running and more then 10 frames ran"""
        return self.is_mest_alive() and self.wait_for_frames(
            timeout=timeout,
            frames=frames,
        )

    def run_ssh_cmd(
        self,
        cmd: str,
        timeout: float = 5,
        **kwargs: Any,
    ) -> CompletedProcess[str]:
        """run ssh commad on EQ

        Args:
            cmd (str): the command to run
            timeout (float, optional): timeout for the command. Defaults to 5.

        Returns:
            CompletedProcess[str]: the command process
        """
        assert self.os_type == OSType.LINUX
        ssh_cmd = ["ssh"] + NO_KEY_CHECK + [self._ssh_root]
        ssh_cmd.append(cmd)
        return self._sp_cmd(ssh_cmd, timeout, **kwargs)

    def path_exists(self, path: pathlib.Path | str) -> bool:
        """check if path exists on EQ

        Args:
            path (pathlib.Path | str): the path to check

        Returns:
            bool: if the path exists
        """
        return self.run_ssh_cmd(f"ls {path}").returncode == 0

    def ssh_cmd_stdout(self, cmd: str, **kwargs: Any) -> str:
        """return only the stdout from ssh command

        Args:
            cmd (str): the command to run

        Returns:
            str: stdout for the command
        """
        return self.run_ssh_cmd(cmd, **kwargs).stdout

    def list_dir(self, _dir: pathlib.Path | str) -> list[str]:
        """list specific dir

        Args:
            _dir (pathlib.Path | str): the path to the dir

        Raises:
            FileNotFoundError: If the dir is not exists
            Exception: for unexpected Exception

        Returns:
            list[str]: list of file in dir.
        """
        ls_cmd = self.run_ssh_cmd(f"ls -1 {_dir}")
        if ls_cmd.returncode == 0:
            return ls_cmd.stdout.splitlines()
        elif "No such file or directory" in ls_cmd.stderr:
            raise FileNotFoundError(ls_cmd.stderr)
        else:
            raise Exception(ls_cmd.stderr)

    def wait_for_core_write(
        self,
        core_type: CoreType = CoreType.PCD,
        timeout: float = 180,
    ) -> bool:
        """wait for core write completion

        Args:
            core_type (CoreType): The type of Core

        Raises:
            NotImplementedError: If the Core type is not implemented

        Returns:
            bool: if the core msg has recived.
        """
        self.logger.debug(f"Waiting for {core_type.name} write completion")
        if core_type == CoreType.PCD:
            core_complete_msg = PCD_WRITE_COMPLETE
        elif core_type == CoreType.FCD:
            core_complete_msg = FCD_WRITE_COMPLETE
        else:
            raise NotImplementedError
        read_from_ser = self.wait_for_msg(core_complete_msg, timeout)
        res = core_complete_msg in read_from_ser
        if not res:
            self.logger.warning(
                "Writing Core did not complete successfully got:\n"
                f"{read_from_ser.decode()}",
            )
        return res

    def delete_crash_folder(self) -> CompletedProcess[str]:
        """Delete PCD and FCD crash folder"""
        return self.run_ssh_cmd(f"rm -rf {self.crash_folder}", timeout=20)

    def _sp_cmd(
        self,
        cmd: list[str],
        timeout: float,
        skip_logging: bool = False,
        **kwargs: Any,
    ) -> CompletedProcess[str]:
        if not skip_logging:
            self.logger.debug(f"[ssh] running cmd: {' '.join(cmd)!r}")
        try:
            res = subprocess.run(
                cmd,
                capture_output=True,
                timeout=timeout,
                text=True,
                **kwargs,
            )
        except subprocess.CalledProcessError as e:
            self.logger.exception(e.stderr)
            raise
        if not skip_logging:
            self.logger.debug(
                "cmd result: ("
                f"returncode={res.returncode}, "
                f"stdout={res.stdout!r}, "
                f"stderr={res.stderr!r})",
            )
        return res

    def _scp(
        self,
        _from: str,
        _to: str,
        timeout: float = 5,
        recurcive: bool = False,
        **kwargs: Any,
    ) -> CompletedProcess[str]:
        cmd = ["scp"] + NO_KEY_CHECK
        if recurcive:
            cmd += ["-r"]
        cmd += [_from]
        cmd += [_to]
        return self._sp_cmd(cmd, timeout, **kwargs)
