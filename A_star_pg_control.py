import pygame as pg
from heapq import *
import sys

def get_circle(x, y):
    return (x * FLOOR_TILE + FLOOR_TILE // 2, y * FLOOR_TILE + FLOOR_TILE // 2), FLOOR_TILE // 4


def get_neighbours(x, y):
    check_neighbour = lambda x, y: True if 0 <= x < cols and 0 <= y < rows else False
    ways = [-1, 0], [0, -1], [1, 0], [0, 1] #, [-1, -1], [1, -1], [1, 1], [-1, 1]
    return [(grid[y + dy][x + dx], (x + dx, y + dy)) for dx, dy in ways if check_neighbour(x + dx, y + dy)]


def get_click_mouse_pos():
    x, y = pg.mouse.get_pos()
    grid_x, grid_y = x // FLOOR_TILE, y // FLOOR_TILE
    pg.draw.circle(screen, pg.Color('white'), *get_circle(grid_x, grid_y))
    click = pg.mouse.get_pressed()
    return (grid_x, grid_y) if click[0] else False


def heuristic(a, b): # 估价函数
   return abs(a[0] - b[0]) + abs(a[1] - b[1])


# def heuristic(a, b):
#    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def dijkstra(start, goal, graph):
    queue = []
    heappush(queue, (0, start))
    cost_visited = {start: 0}
    visited = {start: None}

    while queue:
        cur_cost, cur_node = heappop(queue)
        if cur_node == goal:
            break

        neighbours = graph[cur_node]
        for neighbour in neighbours:
            neigh_cost, neigh_node = neighbour
            new_cost = cost_visited[cur_node] + neigh_cost

            if neigh_node not in cost_visited or new_cost < cost_visited[neigh_node]:
                priority = new_cost + heuristic(neigh_node, goal)
                heappush(queue, (priority, neigh_node))
                cost_visited[neigh_node] = new_cost
                visited[neigh_node] = cur_node
    return visited


cols, rows = 23, 13 # 图的列，行
FLOOR_TILE = 50  # 格子

pg.init() # 实例化
screen = pg.display.set_mode([cols * FLOOR_TILE, rows * FLOOR_TILE])
pg.display.set_caption("hi A-star_control")
clock = pg.time.Clock()
# grid 网格
grid = ['22222222222222222222212',
        '22222292222911112244412',
        '22444422211112911444412',
        '24444444212777771444912',
        '24444444219777771244112',
        '92444444212777791192144',
        '22229444212777779111144',
        '11111112212777772771122',
        '27722211112777772771244',
        '27722777712222772221244',
        '22292777711144429221244',
        '22922777222144422211944',
        '22222777229111111119222']
grid = [[int(char) for char in string ] for string in grid] # 转换成int型
# adjacency dict
graph = {}
for y, row in enumerate(grid):
    for x, col in enumerate(row):
        graph[(x, y)] = graph.get((x, y), []) + get_neighbours(x, y)

start = (0, 7)
goal = start
queue = []
heappush(queue, (0, start))
visited = {start: None}

bg = pg.image.load('img/1.png').convert()
bg = pg.transform.scale(bg, (cols * FLOOR_TILE, rows * FLOOR_TILE))
while True:
    # fill screen
    screen.blit(bg, (0, 0))

    # bfs, get path to mouse click
    mouse_pos = get_click_mouse_pos()
    if mouse_pos:
        visited = dijkstra(start, mouse_pos, graph)
        goal = mouse_pos

    # draw path
    path_head, path_segment = goal, goal
    while path_segment and path_segment in visited:
        pg.draw.circle(screen, pg.Color('white'), *get_circle(*path_segment))
        path_segment = visited[path_segment]
    pg.draw.circle(screen, pg.Color('black'), *get_circle(*start))
    pg.draw.circle(screen, pg.Color('blue'), *get_circle(*path_head))

    # pygame necessary lines
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
    pg.display.flip() # 刷新显示
    clock.tick(8) # 绘制的最大频率
