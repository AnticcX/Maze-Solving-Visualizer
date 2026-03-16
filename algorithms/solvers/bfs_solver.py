from collections import deque
import time

def bfs(maze):
    rows = len(maze)
    cols = len(maze[0])

    start = None
    end = None

    # Locate Start and End
    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == 'S':
                start = (r, c)
            elif maze[r][c] == 'E':
                end = (r, c)

    if not start or not end:
        return None, 0, 0

    queue = deque([start])
    visited = set([start])
    parent = {}

    start_time = time.time()

    while queue:
        current = queue.popleft()

        if current == end:
            break

        r, c = current
        neighbors = [(r+1, c), (r-1, c), (r, c+1), (r, c-1)]

        for nr, nc in neighbors:
            if 0 <= nr < rows and 0 <= nc < cols:
                if maze[nr][nc] != '#' and (nr, nc) not in visited:
                    queue.append((nr, nc))
                    visited.add((nr, nc))
                    parent[(nr, nc)] = current

    runtime = time.time() - start_time

    if end not in parent and end != start:
        return None, len(visited), runtime

    path = []
    node = end
    while node != start:
        path.append(node)
        node = parent[node]
    path.append(start)
    path.reverse()

    return path, len(visited), runtime
