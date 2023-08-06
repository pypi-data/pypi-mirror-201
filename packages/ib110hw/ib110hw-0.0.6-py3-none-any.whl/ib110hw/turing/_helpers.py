from os import name, system
from typing import TextIO, List
from .tape import Tape


def clear_console() -> None:
    if name == "posix":
        system("clear")
    else:
        system("cls")


def close_file(file: TextIO) -> None:
    if file:
        file.close()


def tape_to_md(tape: Tape, index: int = None) -> str:
    index_str = "" if index is None else f"<b>Tape {index}:</b>"
    tape_str = f"{tape}".replace("^", "<b>^</b>")
    return f"{index_str}\n{tape_str}\n"


def rule_to_md(rule_str: str) -> str:
    return f"######{rule_str.replace('->', '&rarr;')}"


def dtm_config_to_md(tape: Tape, rule_str: str) -> str:
    header_str = rule_to_md(rule_str)
    tape_str = tape_to_md(tape)

    return f"{header_str}\n<pre>\n{tape_str}</pre>\n---\n"


def mtm_config_to_md(tapes: List[Tape], rule_str: str) -> str:
    header_str = rule_to_md(rule_str)
    tapes_str = "".join(tape_to_md(tape, i) for i, tape in enumerate(tapes))

    return f"{header_str}\n<pre>\n{tapes_str}</pre>\n---\n"
