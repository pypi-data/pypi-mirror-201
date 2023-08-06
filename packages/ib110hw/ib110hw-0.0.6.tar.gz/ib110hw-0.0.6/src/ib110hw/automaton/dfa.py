from typing import Dict, Optional, Set

from .base import BaseFiniteAutomaton

DFARules = Dict[str, str]
DFATransitions = Dict[str, DFARules]


class DFA(BaseFiniteAutomaton):
    """
    Deterministic Finite Automaton.
    """

    def __init__(
        self,
        states: Set[str] = None,
        alphabet: Set[str] = None,
        initial_state: str = None,
        final_states: Set[str] = None,
        transitions: DFATransitions = None,
    ):
        super().__init__(states, alphabet, initial_state, final_states)
        self.transitions = transitions or {}

    def __repr__(self) -> str:
        return super().__repr__() + "\n" + self.__repr_transitions__()

    def __repr_transitions__(self) -> str:
        def get_max_cell_width() -> int:
            max_cell_width = 5

            for key, val in self.transitions.items():
                for next_val in val.values():
                    max_cell_width = max(max_cell_width, len(next_val), len(key))

            # add 4 for spaces on both sides
            return max_cell_width + 4

        cell_width = get_max_cell_width()

        # create header
        header = f"{'DFA': ^{cell_width+5}}|"
        for letter in sorted(self.alphabet):
            header += f"{letter: ^{cell_width}}|"

        # create table rows
        rows = ""
        for state in sorted(self.states):
            row_prefix = self.__repr_row_prefix__(state)
            rows += f"{row_prefix: ^5}{state or 'empty': <{cell_width}}"

            for letter in sorted(self.alphabet):
                transition = self.get_transition(state, letter)
                rows += f"|{transition or 'empty': ^{cell_width}}"

            rows += "\n"

        divider = "-" * rows.index("\n")

        return "\n".join([header[:-1], divider, rows])

    def get_transition(self, state_from: str, symbol: str) -> Optional[str]:
        """
        Returns next state from the provided state by symbol.

        Args:
            state_from (str): State name where the transition starts.
            symbol (str): Transition symbol.

        Returns:
            str: Next state if such transition exists, None otherwise.
        """
        return self.transitions.get(state_from, {}).get(symbol, None)

    def set_transition(self, state_from: str, state_to: str, symbol: str) -> None:
        """
        Adds/changes transition to automaton.
        If the automaton already contains transition from 'state_from' by 'symbol', it will be overwritten.

        Args:
            state_from (str): State name where the transition starts.
            state_to (str): State name where the transition ends.
            symbol (str): Transition symbol.
        """
        if state_from not in self.transitions.keys():
            self.transitions[state_from] = {symbol: state_to}
        else:
            self.transitions[state_from][symbol] = state_to

    def add_transition(self, state_from: str, state_to: str, symbol: str) -> bool:
        """
        Adds transition to automaton. And returns bool value based on a change.
        Nothing changes if the automaton already contains transition from 'state_from' by 'symbol'.

        Args:
            state_from (str): State name where the transition starts.
            state_to (str): State name where the transition ends.
            symbol (str): Transition symbol.

        Returns:
            bool: True if transition was added, False otherwise.
        """
        if not self.get_transition(state_from, symbol):
            if state_from not in self.transitions.keys():
                self.transitions[state_from] = {}

            self.transitions[state_from][symbol] = state_to
            return True

        return False

    def remove_transition(self, state_from: str, symbol: str) -> bool:
        """
        Removes transition from the automaton and returns bool based on success.

        Args:
            state_from (str): State name which the transition starts from.
            symbol (str): Transition symbol.

        Returns:
            bool: True if the automaton contained such transition, False otherwise.
        """
        if self.get_transition(state_from, symbol):
            del self.transitions[state_from][symbol]
            return True

        return False

    def get_symbols_between_states(self, state_from: str, state_to: str) -> Set[str]:
        """
        Returns set of symbols between two neighbouring states.
        Args:
            state_from: State name where the transition starts.
            state_to: State name where the transition ends.

        Returns:
            Set of symbols.
        """
        return {
            s
            for s in self.transitions[state_from].keys()
            if self.get_transition(state_from, s) == state_to
        }

    def add_state(self, state: str, is_final: bool = False) -> bool:
        """
        Adds a state to the automaton.

        Args:
            state (str): Name of the state to be added.
            is_final (bool, optional): Whether to mark the state as final. Defaults to False.

        Returns:
            bool: True if automaton did not contain such state, False otherwise.
        """
        return super().add_state(state, is_final)

    def remove_state(self, state) -> bool:
        """
        Removes the provided state from the automaton (from its states and transitions).

        Args:
            state (str): State to be removed.

        Returns:
            bool: True if automaton contained such state, False otherwise.
        """

        if not super().remove_state(state):
            return False

        self.transitions.pop(state, None)

        for s in self.transitions.keys():
            for symbol in list(self.transitions[s]):
                if self.transitions[s][symbol] == state:
                    del self.transitions[s][symbol]

        return True

    def is_accepted(self, input_string: str) -> bool:
        """
        Checks whether the provided string is accepted by the automaton.

        Args:
            input_string (str): Input string to be tested.

        Returns:
            bool: True if word is accepted, False otherwise.
        """
        current_state = self.initial_state

        for symbol in input_string:
            if not (current_state := self.get_transition(current_state, symbol)):
                return False

        return current_state in self.final_states

    def is_valid(self) -> bool:
        """
        Checks whether the DFA is valid:
            1. The states set is not empty.
            2. The initial state is in states.
            3. Final states are subset of states.
            4. The alphabet does not contain ε ('').
            5. The transition function contains characters only from its alphabet.
            6. The transition function contains states only from its states set.
            7. The transition function is total.

        Returns:
            bool: True if DFA is valid, False otherwise.
        """
        # creates set of states used in the transition function
        used_states = set(
            sum((list(v.values()) for v in list(self.transitions.values())), [])
        ) | set(self.transitions.keys())

        # creates a set of symbols used in the transition function
        used_symbols = set(sum((list(v.keys()) for v in self.transitions.values()), []))

        # rules 1 - 6
        if (
            not super().is_valid()
            or "" in self.alphabet
            or self.states.symmetric_difference(used_states)
            or used_symbols.symmetric_difference(self.alphabet)
        ):
            return False

        # rule 7
        if self.states - set(self.transitions.keys()) or any(
            self.alphabet - {*rule.keys()} for rule in self.transitions.values()
        ):
            return False

        return True


if __name__ == "__main__":
    pass
