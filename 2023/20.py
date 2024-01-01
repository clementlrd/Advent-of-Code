"""Resolve a daily problem"""  # pylint: disable=invalid-name
from __future__ import annotations
from typing import TypedDict, Protocol, Iterable, Iterator
from dataclasses import dataclass, field
from itertools import accumulate, repeat
from collections import defaultdict
from queue import Queue
from enum import Enum
import math
from utils import section


class Pulse(Enum):
    """Represents a signal pulse"""
    Low = 0
    High = 1


class Module(Protocol):
    """Represents a module.
    A module can send signals to all of its destinations according to
    its internal state and the signal it has received."""
    destinations: list[str]

    def send(self, module: str, input_signal: Pulse) -> Pulse | None:
        """Send a signal to its destinations when receiving the signal `input` from `module`."""


@dataclass(frozen=True, slots=True)
class Broadcaster:
    """A module that send the signal it receives from a `button`."""
    destinations: list[str]

    def send(self, module: str, input_signal: Pulse) -> Pulse | None:
        assert module == 'button', "Broadcaster only receives signal from `button` module."
        return input_signal


@dataclass(slots=True)
class FlipFlop:
    """A module that send a signal according to its internal state."""
    destinations: list[str]
    state: int = 0

    def send(self, _: str, input_signal: Pulse) -> Pulse | None:
        if input_signal != Pulse.Low:
            return None
        self.state = not self.state  # switch
        return Pulse(self.state)


@dataclass(slots=True)
class Conjunction(Module):
    """A module that send a signal according to its memory
    from the latest signal it has received from each module."""
    destinations: list[str]
    memory: dict[str, Pulse] = field(init=False)

    def connect(self, inputs: Iterable[str]) -> None:
        """This module needs to be connected to its inputs to construct its memory."""
        self.memory = dict.fromkeys(inputs, Pulse.Low)

    def send(self, module: str, input_signal: Pulse) -> Pulse | None:
        self.memory[module] = input_signal
        filled = all(v == Pulse.High for v in self.memory.values())
        return Pulse(not filled)


class Circuit:
    """Create a circuit of modules, where there is a button that can be pressed,
    connected to a broadcaster and a serie of modules (Conjunctions and FlipFlop).
    """

    class InfoDict(TypedDict):
        """Collects informations when the button is pressed"""
        Low: int
        High: int
        triggered: dict[tuple[str, Pulse], bool]

    def __init__(self, data: Iterable[str]) -> None:
        module_class = {'b': Broadcaster, '%': FlipFlop, '&': Conjunction}
        self.output_to_input: dict[str, set[str]] = defaultdict(set)  # to connect conjunctions
        self.modules = dict[str, Module]()
        self.info: Circuit.InfoDict = {'Low': 0, 'High': 0, 'triggered': {}}

        for row in data:
            module, dest = row.split(' -> ')
            destinations = dest.split(', ')

            # register module
            name = module if module == "broadcaster" else module[1:]
            self.modules[name] = module_class[module[0]](destinations)

            # gather informations for connections
            for dest in destinations:
                self.output_to_input[dest].add(name)

        # connect conjunction modules
        for name, module in self.modules.items():
            if isinstance(module, Conjunction):
                module.connect(list(self.output_to_input[name]))

    def add_watchers(self, watchers: Iterable[tuple[str, Pulse]]):
        """Register watchers to know if a module has been activated with the given pulse."""
        for e in watchers:
            self.info['triggered'][e] = False

    def press_button(self) -> None:
        """Press button to send Low Signal to the broadcaster.
        The system is not reset if the button is pressed another time."""

        queue = Queue[tuple[str, Pulse, str]]()  # BFS
        queue.put(('button', Pulse.Low, 'broadcaster'))
        while not queue.empty():
            previous, pulse, name = queue.get()
            self.info[pulse.name] += 1   # register pulse

            if (previous, pulse) in self.info['triggered']:
                # register that the module is trigger with the given signal
                self.info['triggered'][(previous, pulse)] = True
            if name not in self.modules:
                continue  # destination not in registered modules
            module = self.modules[name]

            if (new_pulse := module.send(previous, pulse)) is None:
                continue
            for m, p in zip(module.destinations, repeat(new_pulse)):
                queue.put((name, p, m))


@section(year=2023, day=20, part=1, sol=944750144)
def part_1(data: Iterator[str]) -> int:
    """Code for section 1"""
    circuit = Circuit(data)
    for _ in range(1000):
        circuit.press_button()
    return circuit.info['Low'] * circuit.info['High']


@section(year=2023, day=20, part=2, sol=222718819437131)
def part_2(data: Iterator[str]) -> int:
    """Code for section 2"""
    circuit = Circuit(data)
    # get modules sending signal into `kz`, the predecessor of `rx`.
    last_lvl = circuit.output_to_input['kz']
    circuit.add_watchers(zip(last_lvl, repeat(Pulse.High)))
    cycles = dict.fromkeys(last_lvl, -1)

    for step in accumulate(repeat(1)):
        circuit.press_button()
        for (name, _), is_triggered in circuit.info['triggered'].items():
            if cycles[name] < 0 and is_triggered:
                cycles[name] = step
        if all(v > 0 for v in cycles.values()):
            break

    return math.lcm(*cycles.values())


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    part_1()
    part_2()
