from __future__ import annotations

from me_setups.components.comp import Component


class Mcs(Component):
    @property
    def prompt(self) -> bytes:
        return b"Shell>"
