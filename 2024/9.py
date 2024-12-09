from typing import NamedTuple
from operator import attrgetter

from aoc import section, load_input
from aoc.itertools import lmap


class Chunk(NamedTuple):
    pos: int
    length: int
    id_: int = -1

    def __repr__(self) -> str:
        return str(tuple(self if self.id_ != -1 else self[:-1]))


def parse(raw_data: list[str]):
    """Parse input into ..."""
    layout = lmap(int, raw_data[0])

    # build data and free chunks from layout
    cursor, free, data = 0, list[Chunk](),list[Chunk]()
    for i, n in enumerate(layout):
        if not n:
            continue
        (free if i % 2 else data).append(Chunk(cursor, n, -1 if i % 2 else i // 2))
        cursor += n

    # write chunks to disk
    disk = [-1] * sum(layout)
    for c in data:
        for i in range(c.length):
            assert c.id_ != -1
            disk[c.pos + i] = c.id_
    assert all(disk[c.pos + i] == -1 for c in free for i in range(c.length))
    return disk, free, data


@section.p1(sol=6386640365805)
def part_1() -> int:
    """Code for section 1"""
    disk, _, _ = parse(load_input())

    reverse_disk = ((k, id_) for k, id_ in enumerate(disk[::-1]) if id_ != -1)
    for i in range(len(disk)):
        if disk[i] == -1:
            k, id_ = next(reverse_disk)
            if i >= len(disk) - k:
                break
            disk[i] = id_
            disk[-k - 1] = -1

    return sum( i * v for i, v in enumerate(disk) if v != -1 )


# < 8587288893605
@section.p2()
def part_2() -> int:
    """Code for section 2"""
    disk, free, data = parse(load_input())

    for c in sorted(data, key=attrgetter("id_"), reverse=True):
        # find available space
        for free_slot in sorted(free, key=attrgetter("pos")):
            if c.length <= free_slot.length:
                # write data to disk
                for j in range(free_slot.pos, free_slot.pos + c.length):
                    disk[j] = c.id_
                # erase data
                for j in range(c.pos, c.pos + c.length):
                    disk[j] = -1
                free.remove(free_slot)
                # register remaining space
                if (d := free_slot.length - c.length) > 0:
                    free.append(Chunk(free_slot.pos + c.length, d))
                # no need to update the "data" structure as we focus on the disk
                break

    return sum( i * v for i, v in enumerate(disk) if v != -1)

if __name__ == "__main__":
    part_1()
    part_2()
