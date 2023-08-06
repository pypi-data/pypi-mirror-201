from __future__ import annotations

import re


def filter_ansi_escape(text: str) -> str:
    """filter ascii escape characters, removing coloring and unprintable chars.

    Args:
        text (str): the text to filter

    Returns:
        str: the text without the escape characters
    """
    COLOR_ESC = r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])"
    ESC_CHARS = r"[\x00-\x09]|[\x0B-\x1F]"
    ansi_escape = re.compile(f"{COLOR_ESC}|{ESC_CHARS}")
    return ansi_escape.sub("", text)
