import sys

class Maze:
    def __init__(self, n):
        self.n = n
        self.grid = [['█' for _ in range(2 * n + 1)] for _ in range(2 * n + 1)]
        for i in range(n):
            for j in range(n):
                self.grid[2 * i + 1][2 * j + 1] = '·'

    def __str__(self):
        return '\n'.join(''.join(row) for row in self.grid)

    def _parse_coordinates(self, key):
        y0 = key[0]
        x0 = key[1].start
        y1 = key[1].stop
        x1 = key[2]
        return x0, y0, x1, y1

    def __setitem__(self, key, value):
        x0, y0, x1, y1 = self._parse_coordinates(key)
        if value == '·':
            if x0 == x1:
                for j in range(max(min(y0, y1), 0) + 1, min(max(y0, y1) + 1, self.n)):
                    self.grid[2 * x0 + 1][2 * j] = '·'
            elif y0 == y1:
                for i in range(max(min(x0, x1), 0) + 1, min(max(x0, x1) + 1, self.n)):
                    self.grid[i * 2][2 * y0 + 1] = '·'
        elif value == '█':
            if x0 == x1:
                for j in range(max(min(y0, y1), 0) + 1, min(max(y0, y1) + 1, self.n)):
                    self.grid[2 * x0 + 1][j] = '█'
            elif y0 == y1:
                for i in range(max(min(x0, x1), 0) + 1, min(max(x0, x1) + 1, self.n)):
                    self.grid[2 * i][2 * y0 + 1] = '█'

    def __getitem__(self, key):
        x0, y0, x1, y1 = self._parse_coordinates(key)
        visited = set()
        def dfs(x, y):
            if (x, y) == (x1, y1):
                return True
            visited.add((x, y))
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.n and 0 <= ny < self.n and (nx, ny) not in visited
                        and self.grid[2 * x + dx + 1][2 * y + dy + 1] == '·'):
                    if dfs(nx, ny):
                        return True
            return False
        return dfs(x0, y0)

exec(sys.stdin.read())