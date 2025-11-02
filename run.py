#!/usr/bin/env python
import sys
import heapq

ENERGY = {"A": 1, "B": 10, "C": 100, "D": 1000}
ROOMS = {"A": 0, "B": 1, "C": 2, "D": 3}
DOORS = [2, 4, 6, 8]
HALL_POS = [0, 1, 3, 5, 7, 9, 10]


def parse_input(lines):
    """Парсит лабиринт, возвращает состояние коридора и комнат."""
    room_lines = [line for line in lines[2:] if any(c in "ABCD" for c in line)]
    hallway = tuple("." * 11)
    rooms = tuple(tuple(line[i] for line in room_lines) for i in (3, 5, 7, 9))
    return hallway, rooms


def path_clear(h, a, b):
    """Проверяет, свободен ли путь в коридоре между двумя позициями."""
    return all(h[i] == "." for i in (range(a+1, b+1) if a < b else range(b, a)))


def gen_moves(h, rooms):
    """Генерирует все допустимые ходы из текущего состояния."""
    depth = len(rooms[0])

    # Из коридора в комнату
    for pos, c in enumerate(h):
        if c == ".":
            continue
        ri = ROOMS[c]
        door = DOORS[ri]
        room = rooms[ri]
        if any(x not in (".", c) for x in room) or not path_clear(h, pos, door):
            continue
        d = max(i for i, x in enumerate(room) if x == ".")
        steps = abs(door-pos)+d+1
        new_h = list(h)
        new_h[pos] = "."
        new_r = [list(r) for r in rooms]
        new_r[ri][d] = c
        yield steps*ENERGY[c], (tuple(new_h), tuple(tuple(r) for r in new_r))

    # Из комнаты в коридор
    for ri, room in enumerate(rooms):
        door = DOORS[ri]
        for d, c in enumerate(room):
            if c == ".":
                continue
            if all(x in (".", "ABCD"[ri]) for x in room[d:]):
                break
            for pos in HALL_POS:
                if path_clear(h, door, pos):
                    steps = abs(door-pos)+d+1
                    new_h = list(h)
                    new_h[pos] = c
                    new_r = [list(r) for r in rooms]
                    new_r[ri][d] = "."
                    yield steps*ENERGY[c], (tuple(new_h), tuple(tuple(r) for r in new_r))
            break


def solve(lines):
    """
    Решает задачу минимальной энергии для перемещения объектов в целевые комнаты.
    """
    h, rooms = parse_input(lines)
    depth = len(rooms[0])
    goal = (tuple("."*11), tuple(tuple(c for _ in range(depth))
            for c in "ABCD"))
    start = (h, rooms)
    seen = {start: 0}
    pq = [(0, start)]

    while pq:
        cost, state = heapq.heappop(pq)
        if state == goal:
            return cost
        if cost > seen[state]:
            continue
        for move_cost, new_state in gen_moves(*state):
            new_cost = cost+move_cost
            if new_cost < seen.get(new_state, float('inf')):
                seen[new_state] = new_cost
                heapq.heappush(pq, (new_cost, new_state))
    return -1


def main():
    """Чтение входа и вывод результата."""
    lines = [l.rstrip("\n") for l in sys.stdin if l.strip()]
    print(solve(lines))


if __name__ == "__main__":
    main()
