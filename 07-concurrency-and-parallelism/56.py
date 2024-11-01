EMPTY = "-"
ALIVE = "*"


class Grid:

    def __init__(self, height: int, width: int) -> None:
        self.height = height
        self.width = width
        self.rows = []
        for _ in range(height):
            self.rows.append([EMPTY] * width)

    def get(self, y: int, x: int) -> str:
        return self.rows[y % self.height][x % self.width]

    def set(self, y: int, x: int, state: str) -> None:
        self.rows[y % self.height][x % self.width] = state

    def __str__(self) -> str:
        return "\n".join("".join(row) for row in self.rows)

    def count_neighbors(self, y: int, x: int) -> int:
        neighbors = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        count = 0
        for dy, dx in neighbors:
            if self.get(y + dy, x + dx) == ALIVE:
                count += 1
        return count

    def next_state(self, y: int, x: int) -> str:
        current_state = self.get(y, x)
        count = self.count_neighbors(y, x)
        if current_state == ALIVE:
            if count < 2:
                return EMPTY
            if count > 3:
                return EMPTY
        else:
            if count == 3:
                return ALIVE
        return current_state

    def next_gen(self) -> None:
        new_grid = Grid(self.height, self.width)
        for y in range(self.height):
            for x in range(self.width):
                new_grid.set(y, x, self.next_state(y, x))
        self.rows = new_grid.rows

    def print_columns(self, number: int) -> None:
        grids = [str(self)]
        for _ in range(number - 1):
            self.next_gen()
            grids.append(str(self))

        split_lines = [grid.split('\n') for grid in grids]
        res = "\n".join(
            "|".join([line[i] for line in split_lines])
            for i in range(len(split_lines[0]))
        )
        print(str(res))


grid = Grid(5, 9)
grid.set(0, 3, ALIVE)
grid.set(1, 4, ALIVE)
grid.set(2, 2, ALIVE)
grid.set(2, 3, ALIVE)
grid.set(2, 4, ALIVE)

grid.print_columns(10)
