import pygame as pg
from heapq import *
import sys

def get_circle(x, y):
    return (x * FLOOR_TILE + FLOOR_TILE // 2, y * FLOOR_TILE + FLOOR_TILE // 2), FLOOR_TILE // 4


def get_rect(x, y):
    return x * FLOOR_TILE + 1, y * FLOOR_TILE + 1, FLOOR_TILE - 2, FLOOR_TILE - 2


def get_next_nodes(x, y):
    check_next_node = lambda x, y: True if 0 <= x < cols and 0 <= y < rows else False
    directions = [-1, 0], [0, -1], [1, 0], [0, 1]
    return [(grid[y + dy][x + dx], (x + dx, y + dy)) for dx, dy in directions if check_next_node(x + dx, y + dy)]


def heuristic(a, b): # 估价函数
   return abs(a[0] - b[0]) + abs(a[1] - b[1])


cols, rows = 23, 13 # 图的列，行
FLOOR_TILE = 50 # 格子

pg.init() # 实例化
screen = pg.display.set_mode([cols * FLOOR_TILE, rows * FLOOR_TILE])
pg.display.set_caption("hi A-star")
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

graph = {}
for y, row in enumerate(grid):
    for x, col in enumerate(row):
        graph[(x, y)] = graph.get((x, y), []) + get_next_nodes(x, y)

print(graph)
# settings
start = (0, 7)
end = (22, 7)
queue = []
heappush(queue, (0, start))
cost_visited = {start: 0}
visited = {start: None}

bg = pg.image.load('img/1.png').convert()
bg = pg.transform.scale(bg, (cols * FLOOR_TILE, rows * FLOOR_TILE))

while True:
    # fill screen
    screen.blit(bg, (0, 0))
    # draw work
    [pg.draw.rect(screen, pg.Color('forestgreen'), get_rect(x, y), 1) for x, y in visited]
    [pg.draw.rect(screen, pg.Color('darkslategray'), get_rect(*xy)) for _, xy in queue]
    pg.draw.circle(screen, pg.Color('purple'), *get_circle(*end))

    # logic
    if queue:
        cur_cost, cur_node = heappop(queue)
        if cur_node == end:
            queue = []
            continue

        next_nodes = graph[cur_node]
        for next_node in next_nodes:
            neigh_cost, neigh_node = next_node
            new_cost = cost_visited[cur_node] + neigh_cost

            if neigh_node not in cost_visited or new_cost < cost_visited[neigh_node]:
                priority = new_cost + heuristic(neigh_node, end)
                heappush(queue, (priority, neigh_node))
                cost_visited[neigh_node] = new_cost
                visited[neigh_node] = cur_node

    # 绘制路径
    path_head, path_segment = cur_node, cur_node
    while path_segment:
        pg.draw.circle(screen, pg.Color('white'), *get_circle(*path_segment))
        path_segment = visited[path_segment]
    pg.draw.circle(screen, pg.Color('black'), *get_circle(*start))
    pg.draw.circle(screen, pg.Color('blue'), *get_circle(*path_head))

    # 获取事情，用于退出
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
    pg.display.flip() # 刷新显示
    clock.tick(8) # 绘制的最大帧率