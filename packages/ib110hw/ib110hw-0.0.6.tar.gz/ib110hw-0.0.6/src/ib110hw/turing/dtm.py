from os import name, system
from time import sleep
from typing import Dict, Optional, Set, Tuple

from .base import BaseTuringMachine, MAX_STEPS_ERROR_MSG
from .tape import Direction, Tape, START_SYMBOL
from ._helpers import dtm_config_to_md, clear_console, close_file

DTMRule = Tuple[str, str, Direction]
DTMRules = Dict[str, DTMRule]
DTMTransitions = Dict[str, DTMRules]


class DTM(BaseTuringMachine):
    """
    Represents a Deterministic Turing Machine
    """

    def __init__(
        self,
        states: Set[str] = None,
        input_alphabet: Set[str] = None,
        acc_states: Set[str] = None,
        rej_states: Set[str] = None,
        transitions: DTMTransitions = None,
        tape: Tape = None,
        initial_state: str = "init",
        start_symbol: str = START_SYMBOL,
    ) -> None:
        super().__init__(
            states,
            input_alphabet,
            acc_states,
            rej_states,
            initial_state,
            start_symbol,
        )
        self.transitions = transitions or Tape()
        self.tape = tape or Tape()

    def get_transition(self, state: str, read: str) -> Optional[DTMRule]:
        """
        Gets the transition based on the provided state and read symbol.

        Args:
            state (str): Current state of the DTM.
            read (str): Symbol read by the tape head.

        Returns:
            DTMRule: Transition based on the provided parms if exists, None otherwise.
        """
        return self.transitions.get(state, {}).get(read, None)

    def write_to_tape(self, input_str: str) -> None:
        """
        Writes the provided string on the tape.

        Args:
            input_str (str): String to be written on the tape.
        """
        self.tape.write(self.start_symbol + input_str)

    def clear_tape(self) -> None:
        """
        Clears the contents of the tape.
        """
        self.tape.clear()

    def read_tape(self) -> str:
        """
        Reads contents of the tape.

        Returns:
            str: String written on the tape.
        """
        return self.tape.read()

    def simulate(
        self,
        to_console: bool = True,
        to_file: bool = False,
        path: str = "simulation.md",
        delay: float = 0.5,
    ) -> bool:
        """
        Simulates the machine on its current tape configuration.

        Args:
            to_console (bool, optional): Set to False if you only want to see the result. Defaults to True.
            to_file (bool, optional): Set to True if you want to save every step to the file. Defaults to False.
            path (str, optional): Path to the .md file with the step history. Defaults to "simulation.md".
            delay (float, optional): The delay (s) between each step when printing to console. Defaults to 0.5.

        Returns:
            bool: False if the machine rejects the word or exceeds the 'max_steps' value, True otherwise.
        """
        state: str = self.initial_state
        steps: int = 1
        output_file = None

        def get_rule_string() -> str:
            row = self.get_transition(state, self.tape.current.value)
            step_index = steps if row else steps - 1
            next_step = f"{state}, {self.tape.current.value}"

            return f"{step_index}. ({next_step}) -> {row}\n"

        def print_machine_configuration() -> None:
            rule_str = get_rule_string()

            if output_file:
                output_file.write(dtm_config_to_md(self.tape, rule_str))

            if to_console:
                clear_console()
                print(f"{rule_str}\n{self.tape}")
                sleep(delay)

        # the simulation itself starts here
        if to_file:
            output_file = open(path, "w")

        while steps <= (self.max_steps + 1):
            print_machine_configuration()

            if state in self.acc_states:
                close_file(output_file)
                return True

            rule = self.get_transition(state, self.tape.current.value)

            if not rule or rule[0] in self.rej_states:
                close_file(output_file)
                return False

            steps += 1
            state, write, direction = rule
            self.tape.write_symbol(write)
            self.tape.move(direction)

        close_file()
        print(MAX_STEPS_ERROR_MSG.format(self.max_steps))

        return False


if __name__ == "__main__":
    pass
