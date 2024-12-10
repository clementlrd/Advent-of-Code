from operator import attrgetter
from dataclasses import dataclass

from aoc import section, load_input
from aoc.itertools import lmap


@dataclass
class Chunk:
    pos: int
    length: int
    id_: int = -1


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

    reverse_data_disk = ((i, disk[i]) for i in range(len(disk)-1,-1, -1) if disk[i] != -1)
    for i in filter(lambda i: disk[i] == -1, range(len(disk))):
        # get the next piece of data from the right
        k, id_ = next(reverse_data_disk)
        # make sure the next free space is not beyond the data
        if i >= k:
            break
        # move data
        disk[i] = id_
        disk[k] = -1

    return sum( i * v for i, v in enumerate(disk) if v != -1 )


@section.p2(sol=6423258376982)
def part_2() -> int:
    """Code for section 2"""
    disk, free, data = parse(load_input())

    # make sur the free slots are sorted by space, the order is kept during the whole process
    free.sort(key=attrgetter("pos"))
    data.sort(key=attrgetter("id_"), reverse=True)
    for c in data:
        # find available space
        for free_slot in free:
            if free_slot.pos > c.pos:
                break  # don't move chunk if the free slot is farther on the disk 
            if c.length <= free_slot.length:
                # write data to disk
                for j in range(free_slot.pos, free_slot.pos + c.length):
                    disk[j] = c.id_
                # erase data
                for j in range(c.pos, c.pos + c.length):
                    disk[j] = -1
                # update remaining space
                # no need to update the "data" structure as we focus on the disk
                if (d := free_slot.length - c.length) > 0:
                    free_slot.pos += c.length; free_slot.length = d
                    # - don't need to add the freed space as it is above the next data chunk to move
                    # - don't need to merge free slots as there would be no one to merge
                else:
                    free.remove(free_slot)
                break

    return sum( i * v for i, v in enumerate(disk) if v != -1 )

if __name__ == "__main__":
    part_1()
    part_2()
