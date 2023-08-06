from __future__ import annotations

from me_setups.boards.gas52 import Gas52Board
from me_setups.boards.types import BoardType
from me_setups.components.mcu import McuType


Gas52 = Gas52Board


class Gas52EvoB1(Gas52Board):
    def __init__(self) -> None:
        super().__init__(
            mcu=Gas52Board.create_mcu(mcu_type=McuType.ASR),
            board_type=BoardType.EVO,
            board_name="GAS52-EVO_B-B1",
            board_rev="0x1",
        )


class Gas52EvoC1(Gas52Board):
    def __init__(self) -> None:
        super().__init__(
            mcu=Gas52Board.create_mcu(mcu_type=McuType.ASR),
            board_type=BoardType.EVO,
            board_name="GAS52-EVO_B-C1",
            board_rev="0x2",
        )


Gas52Evo = Gas52EvoC1


def get_board(board_type: BoardType) -> Gas52Board | Gas52Evo:
    if board_type == BoardType.EVO:
        return Gas52Evo()
    else:
        return Gas52Board()
