"""Resolve a daily problem"""  # pylint: disable=invalid-name
from __future__ import annotations
from typing import Callable, Iterator, TypeVar, Generic
from dataclasses import dataclass
from copy import deepcopy
import operator
from queue import LifoQueue
from functools import reduce

from utils import section, lmap

operators = {'<': operator.lt, '>': operator.gt}
variables = ('x', 'm', 'a', 's')


@dataclass
class Range:
    # start and end inside the range
    start: int
    end: int

    def __len__(self):
        return self.end - self.start + 1

    def __lt__(self, x: int) -> tuple[Range | None, Range | None]:
        # succes, echec
        if self.end < x:
            return self, None
        if self.start >= x:
            return None, self
        return Range(self.start, x - 1), Range(x, self.end)

    def __gt__(self, x: int) -> tuple[Range | None, Range | None]:
        # succes, echec
        if self.start > x:
            return self, None
        if self.end <= x:
            return None, self
        return Range(x + 1, self.end), Range(self.start, x)

    def __iter__(self) -> Iterator[int]:
        return iter(range(self.start, self.end + 1))


T = TypeVar('T', bound=int | Range)


@dataclass
class Part(Generic[T]):
    x: T
    m: T
    a: T
    s: T

    @staticmethod
    def from_json(obj: str) -> Part[int]:
        return Part[int](**{x[0]: int(x[2:]) for x in obj[1:-1].split(',')})


@dataclass
class Rule:
    variable: str
    op: Callable
    bound: int
    destination: str

    @classmethod
    def from_repr(cls, _repr: str) -> Rule:
        cond, dest = _repr.split(':')
        v, op, b = cond[0], cond[1], cond[2:]
        return cls(variable=v, op=operators[op], bound=int(b), destination=dest)

    def condition(self, part: Part[int]) -> bool:
        return self.op(getattr(part, self.variable), self.bound)


@dataclass
class Workflow:
    rules: list[Rule]
    final: str

    def execute(self, part: Part[int]) -> str:
        for rule in self.rules:
            if rule.condition(part):
                return rule.destination
        return self.final

    def execute_range(self, rpart: Part[Range]) -> Iterator[tuple[Part[Range], str]]:
        for rule in self.rules:
            success, echec = rule.op(getattr(rpart, rule.variable), rule.bound)
            if success is not None and len(success) > 0:
                new_rpart = deepcopy(rpart)
                setattr(new_rpart, rule.variable, success)
                yield new_rpart, rule.destination
            if echec is None or len(echec) <= 0:
                return
            setattr(rpart, rule.variable, echec)
        yield rpart, self.final


def create_workflows(data: Iterator[str]) -> dict[str, Workflow]:
    """Consume data iterator to create workflows until there is an empty line."""
    workflows = {}
    for row in data:
        if not row:
            break
        name, rules = row.split('{')
        rules = rules[:-1].split(',')
        workflows[name] = Workflow(lmap(Rule.from_repr, rules[:-1]), final=rules[-1])
    return workflows


@section(year=2023, day=19, part=1, sol=263678)
def part_1(data: Iterator[str]) -> int:
    """Code for section 1"""
    workflows, parts = create_workflows(data), lmap(Part.from_json, data)

    total = 0
    for part in parts:
        dest = 'in'
        while dest not in ('R', 'A'):
            dest = workflows[dest].execute(part)
        if dest == 'A':
            total += sum((getattr(part, n) for n in variables))
    return total


@section(year=2023, day=19, part=2, sol=125455345557345)
def part_2(data: Iterator[str]) -> int:
    """Code for section 2"""
    workflows = create_workflows(data)
    range_part = Part(**{n: Range(1, 4000) for n in variables})

    accepted = list[Part[Range]]()
    queue = LifoQueue[tuple[Part[Range], str]]()
    queue.put((range_part, 'in'))
    while not queue.empty():
        part, dest = queue.get()
        for _p, _d in workflows[dest].execute_range(part):
            if _d == 'A':
                accepted.append(_p)
            elif _d != 'R':
                queue.put((_p, _d))

    return sum((reduce(operator.mul, (len(getattr(part, n))
               for n in variables)) for part in accepted))


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    part_1()
    part_2()
