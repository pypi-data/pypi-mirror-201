from sys import path

path.append("../src/ib110hw")
from turing.dtm import DTM
from turing.mtm import MTM
from turing.tape import Direction

DTM_MACHINE: DTM = DTM(
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


MTM_MACHINE: MTM = MTM(
    states={"init", "goToEnd", "goToStart", "check", "accept", "reject"},
    initial_state="init",
    input_alphabet={"a", "b"},
    acc_states={"accept"},
    rej_states={"reject"},
    transitions={
        "init": {(">", ""): ("copy", (">", ""), (Direction.RIGHT, Direction.STAY))},
        "copy": {
            ("a", ""): ("copy", ("a", "a"), (Direction.RIGHT, Direction.RIGHT)),
            ("b", ""): ("copy", ("b", "b"), (Direction.RIGHT, Direction.RIGHT)),
            ("", ""): ("goToStart", ("", ""), (Direction.LEFT, Direction.STAY)),
        },
        "goToStart": {
            ("a", ""): ("goToStart", ("a", ""), (Direction.LEFT, Direction.STAY)),
            ("b", ""): ("goToStart", ("b", ""), (Direction.LEFT, Direction.STAY)),
            (">", ""): ("check", (">", ""), (Direction.RIGHT, Direction.LEFT)),
        },
        "check": {
            ("a", "a"): ("check", ("a", "a"), (Direction.RIGHT, Direction.LEFT)),
            ("b", "b"): ("check", ("b", "b"), (Direction.RIGHT, Direction.LEFT)),
            ("", ""): ("accept", ("", ""), (Direction.STAY, Direction.STAY)),
            ("a", "b"): ("reject", ("a", "b"), (Direction.STAY, Direction.STAY)),
            ("b", "a"): ("reject", ("b", "a"), (Direction.STAY, Direction.STAY)),
        },
    },
)

DTM_MACHINE.max_steps = 10000
DTM_MACHINE.write_to_tape("abba")
DTM_MACHINE.simulate(to_file=True, delay=0.2, path="./simulation_dtm.md")

MTM_MACHINE.max_steps = 10000
MTM_MACHINE.write_to_tape("abba")
MTM_MACHINE.simulate(to_file=True, delay=0.2, path="./simulation_mtm.md")
