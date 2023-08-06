from hypothesis import given
from sys import path
from generation import acc_palindromes, rej_palindromes

path.append("../src/ib110hw")
from turing.dtm import DTM
from turing.tape import Direction

PALINDROME_MACHINE: DTM = DTM(
    states={
        "init",
        "mark",
        "gotoEndA",
        "checkA",
        "gotoEndB",
        "checkB",
        "accept",
        "reject",
    },
    input_alphabet={"a", "b"},
    acc_states={"accept"},
    rej_states={"reject"},
    initial_state="init",
    transitions={
        "init": {
            ">": ("mark", ">", Direction.RIGHT),
        },
        "mark": {
            "a": ("foundA", "X", Direction.RIGHT),
            "b": ("foundB", "X", Direction.RIGHT),
            "X": ("accept", "X", Direction.STAY),
            "": ("accept", "", Direction.STAY),
        },
        "foundA": {
            "a": ("foundA", "a", Direction.RIGHT),
            "b": ("foundA", "b", Direction.RIGHT),
            "X": ("checkA", "X", Direction.LEFT),
            "": ("checkA", "", Direction.LEFT),
        },
        "checkA": {
            "a": ("back", "X", Direction.LEFT),
            "b": ("reject", "b", Direction.STAY),
            "X": ("accept", "X", Direction.STAY),
        },
        "foundB": {
            "a": ("foundB", "a", Direction.RIGHT),
            "b": ("foundB", "b", Direction.RIGHT),
            "X": ("checkB", "X", Direction.LEFT),
            "": ("checkB", "", Direction.LEFT),
        },
        "checkB": {
            "a": ("reject", "a", Direction.STAY),
            "b": ("back", "X", Direction.LEFT),
            "X": ("accept", "X", Direction.STAY),
        },
        "back": {
            "a": ("back", "a", Direction.LEFT),
            "b": ("back", "b", Direction.LEFT),
            "X": ("mark", "X", Direction.RIGHT),
        },
    },
)

PALINDROME_MACHINE.max_steps = 10000


@given(acc_palindromes())
def test_simulate_acc(input_str: str):
    PALINDROME_MACHINE.write_to_tape(input_str)
    assert PALINDROME_MACHINE.simulate(to_console=False)
    PALINDROME_MACHINE.clear_tape()


@given(rej_palindromes())
def test_simulate_rej(input_str: str):
    PALINDROME_MACHINE.write_to_tape(input_str)
    assert not PALINDROME_MACHINE.simulate(to_console=False)
    PALINDROME_MACHINE.clear_tape()
