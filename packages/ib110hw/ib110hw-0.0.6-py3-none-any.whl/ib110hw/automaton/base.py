from typing import Set


class BaseFiniteAutomaton:
    """
    Represents an abstract Finite Automaton class. This class cannot be instantiated.
    """

    def __new__(cls, *args, **kwargs):
        if cls is BaseFiniteAutomaton:
            raise TypeError("Only NFA and DFA can be instantiated!")

        return object.__new__(cls)

    def __init__(
        self,
        states: Set[str],
        alphabet: Set[str],
        initial_state: str,
        final_states: Set[str],
    ) -> None:
        self.states = states or set()
        self.alphabet = alphabet or set()
        self.initial_state = initial_state
        self.final_states = final_states or set()

    def __repr__(self) -> str:
        alphabet_str = ",".join(self.alphabet)
        states_str = ",".join(self.states)
        final_states_str = ",".join(self.final_states)

        return f"alphabet: {alphabet_str}\nstates: {states_str}\nfinal states: {final_states_str}\n"

    def __repr_row_prefix__(self, state: str):
        if state == self.initial_state:
            return "<-> " if state in self.final_states else "--> "

        return "<-- " if state in self.final_states else "    "

    def add_state(self, state: str, is_final: bool = False) -> bool:
        if state in self.states:
            return False

        if is_final:
            self.final_states.add(state)

        self.states.add(state)

        return True

    def remove_state(self, state) -> bool:
        if state not in self.states:
            return False

        if state in self.final_states:
            self.final_states.remove(state)

        self.states.difference_update({state})

        return True

    def is_valid(self) -> bool:
        return (
            self.states
            and self.initial_state in self.states
            and self.final_states.issubset(self.states)
        )

    def complement(self) -> None:
        """
        Complements the automaton. (Final states will become non-final and vice-versa).
        """
        self.final_states = self.states - self.final_states


if __name__ == "__main__":
    pass
