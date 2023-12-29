"""Resolve a daily problem"""  # pylint: disable=invalid-name
from __future__ import annotations
from typing import Optional, Protocol, Any, Iterable, Iterator
from dataclasses import dataclass, field
from itertools import accumulate, repeat
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


Circuit = dict[str, Module]


@dataclass
class Broadcaster(Module):
    """A module that send the signal it receives from a `button`."""
    destinations: list[str]

    def send(self, module: str, input_signal: Pulse) -> Pulse | None:
        assert module == 'button', "Broadcaster only receives signal from `button` module."
        return input_signal


@dataclass
class FlipFlop(Module):
    """A module that send a signal according to its internal state."""
    destinations: list[str]
    state: int = 0

    def send(self, _: str, input_signal: Pulse) -> Pulse | None:
        if input_signal != Pulse.Low:
            return None
        self.state = not self.state  # switch
        return Pulse(self.state)


@dataclass
class Conjonction(Module):
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


def press_button(
    modules: dict[str, Module],
    watch_trigger: Optional[dict[str, Pulse]] = None
) -> dict[str, Any]:
    """Press a buttons and wait until all the signals has been propagated.
    It returns a dictionnary with data: The number of low pulses and high pulses sent,
    and whether a module have been triggered with a pulse or not."""
    # TODO: add into a class named Button
    # setup data
    data: dict[str, Any] = {'Low': 0, 'High': 0, 'triggered': {}}
    if watch_trigger is not None:
        data['triggered'] = {k: False for k in watch_trigger.keys()}

    # main loop
    queue = Queue[tuple[str, Pulse, str]]()  # BFS
    queue.put(('button', Pulse.Low, 'broadcaster'))
    while not queue.empty():
        previous, pulse, name = queue.get()
        data[pulse.name] += 1   # register pulse

        if watch_trigger is not None and pulse == watch_trigger.get(previous, None):
            # register that the module is trigger with the given signal
            data['triggered'][previous] = True
        if name == 'rx':
            continue  # not in registered modules
        module = modules[name]

        new_pulse = module.send(previous, pulse)
        if new_pulse is None:
            continue
        for m, p in zip(module.destinations, repeat(new_pulse)):
            queue.put((name, p, m))

    return data


def build_modules(data: Iterator[str]) -> tuple[Circuit, set[str]]:
    """Build modules from input."""
    module_class = {'b': Broadcaster, '%': FlipFlop, '&': Conjonction}
    output_to_input: dict[str, set[str]] = {}
    modules: Circuit = {}

    for row in data:
        module, dest = row.split(' -> ')
        destinations = dest.split(', ')

        # register module
        name = module if module == "broadcaster" else module[1:]
        modules[name] = module_class[module[0]](destinations)

        # gather informations
        for dest in destinations:
            if dest not in output_to_input:
                output_to_input[dest] = set[str]()
            output_to_input[dest].add(name)

    # connect Conjonction modules
    for name, module in modules.items():
        if isinstance(module, Conjonction):
            module.connect(list(output_to_input[name]))

    # get modules sending signal into `kz`, the predecessor of `rx`.
    return (modules, output_to_input['kz'])


@section(year=2023, day=20, part=1, sol=944750144)
def part_1(data: Iterator[str]) -> int:
    """Code for section 1"""
    modules, _, pulses = *build_modules(data), [0, 0]
    for _ in range(1000):
        info = press_button(modules)
        for i, k in enumerate(Pulse):
            pulses[i] += info[k.name]
    return pulses[0] * pulses[1]


@section(year=2023, day=20, part=2, sol=222718819437131)
def part_2(data: Iterator[str]) -> int:
    """Code for section 2"""
    modules, last_lvl = build_modules(data)
    cycles = dict.fromkeys(last_lvl, -1)
    watch = dict.fromkeys(last_lvl, Pulse.High)

    for step in accumulate(repeat(1)):
        info = press_button(modules, watch_trigger=watch)['triggered']
        for name, is_triggered in info.items():
            if cycles[name] < 0 and is_triggered:
                cycles[name] = step
        if all(v > 0 for v in cycles.values()):
            break

    return math.lcm(*cycles.values())


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    part_1()
    part_2()
