import pygame as pg
import copy
import math

# screen_size = [ 800, 600 ]
# screen_size = [ 1000, 700 ]
screen_size = [ 1600, 900 ]
# screen_size = [ 2000, 1200 ]
# screen_size = [ 3500, 2200 ]

speed = 1
shows_roots = False
shows_city_index = False

TEXT_COLOR = ( 0, 0, 63 )
WAIT_ONE_FRAME_MILLIS = 15
ROOT_ANIM_MILLIS = 1000
FONT_SIZE = screen_size[0] // 80
CITY_RADIUS = 6
ROOTS_HEIGHT = FONT_SIZE * 5

BACK_COLOR = ( 255, 255, 255 )
# fixed, grayed, fixing, adjacents, updating, 
EDGE_LINE_COLORS = [
  (152,78,163),
  (242,242,242),
  ( 0, 63, 0 ),
  (192,192,192),
  (192,255,192),
]
EDGE_TEXT_COLORS = [
  (55,126,184),
  (242,242,242),
  ( 0, 63, 0 ),
  (192,192,192),
  (31,63,31),
]
CITY_NAME_COLORS = [
  (55,126,184),
  (192,192,192),
]
CITY_BODY_COLORS = [
  (229,216,189),
  (242,242,242),
  (127,63,32),
  (152,78,163),
]
CITY_OUTLINE_COLORS = [
  (166,86,40),
  (192,192,192),
  (63,63,63),
  (63,0,0),
]
ROOTS_BODY_COLOR = (242, 242, 242)
ROOTS_BODY_COLOR_CMP = (204,235,197)
ROOTS_BODY_COLOR_CMP_1 = (179,205,227)
ROOTS_BODY_COLOR_CMP_2 = (204,235,197)
ROOTS_BODY_COLOR_EMP = (179,205,227)
ROOTS_BODY_COLOR_ROOT = (251,180,174)
ROOTS_BODY_COLOR_VIA = (254,217,166)
ROOTS_BODY_COLOR_UPDATE = (228,26,28)
ROOTS_EDGE_COLOR = ( 0, 63, 0 )
ROOTS_LIGHT_COLOR = ( 192, 255, 192 )
ROOTS_TEXT_COLOR = TEXT_COLOR

class Context: pass
ctx = Context()

def init(title):
  global screen
  pg.init()
  screen = pg.display.set_mode(screen_size)
  pg.display.set_caption(title)
  clear()

def clear(color = (255,255,255)):
  screen.fill(color)

def wait(millis):
  millis = int(millis / speed)
  if millis < WAIT_ONE_FRAME_MILLIS: millis = WAIT_ONE_FRAME_MILLIS

  pg.time.wait(millis)
  loop = True
  first = True
  while loop:
    if first:
      first = False
      loop = False
    for e in pg.event.get():
      if e.type == pg.QUIT:
        pg.quit()
      elif e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
        pg.quit()
      elif e.type == pg.KEYDOWN and e.key == pg.K_SPACE:
        loop = True
      elif e.type == pg.KEYUP and e.key == pg.K_SPACE:
        loop = False
      elif e.type == pg.MOUSEMOTION:
        if hasattr(ctx, 'on_mouse_motion'):
          ctx.on_mouse_motion()

def wait_for_keydown():
  loop = True
  while loop:
    for e in pg.event.get():
      if e.type == pg.QUIT:
        loop = False
        pg.quit()
      elif e.type == pg.KEYDOWN:
        loop = False

def end():
  loop = True
  while loop:
    for e in pg.event.get():
      if e.type == pg.QUIT:
        loop = False
      elif e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
        loop = False
      elif e.type == pg.MOUSEMOTION:
        if hasattr(ctx, 'on_mouse_motion'):
          ctx.on_mouse_motion()
  pg.quit()

def compute_min_max():
  global min_x, min_y, max_x, max_y
  min_x, max_x = float('inf'), float('-inf')
  min_y, max_y = float('inf'), float('-inf')
  for c in the_cities:
    if min_x > c.x: min_x = c.x
    if min_y > c.y: min_y = c.y
    if max_x < c.x: max_x = c.x
    if max_y < c.y: max_y = c.y
  # print('min:', (min_x, min_y), 'max:', (max_x, max_y))

  global diff_x, diff_y
  diff_x = max_x - min_x
  diff_y = max_y - min_y

  global margin_x, margin_y, scale_w, scale_h
  margin_x = screen_size[0] // 20
  scale_w = screen_size[0] - 2 * margin_x
  margin_y = screen_size[1] // 20
  margin_b = (ROOTS_HEIGHT + FONT_SIZE) if shows_roots else margin_y
  scale_h = screen_size[1] - margin_y - margin_b
  print('sc:', (scale_w,scale_h), 'm:', margin_y, margin_b, 'sr:',shows_roots)

def o2s(x, y):
  dx, dy = x - min_x, y - min_y
  x = margin_x + dx / diff_x * scale_w
  y = margin_y + dy / diff_y * scale_h
  return [x, y]

def xy2s(xy):
  sxy = o2s(xy[0], xy[1])
  # print(xy, '->', sxy)
  return [sxy[0], sxy[1]]

def city2s(city):
  return xy2s([city.x, city.y])

def xy_center(xy1, xy2, t=1):
  x1,y1 = xy1[0], xy1[1]
  x2,y2 = xy2[0], xy2[1]
  return [(x1*t+x2*(2-t))//2, (y1*t+y2*(2-t))//2]

def setup(list, edges=None):
  global the_cities
  the_cities = list

  global the_edges
  the_edges = edges

  compute_min_max()
  global font
  font = pg.font.SysFont("arial", FONT_SIZE) 

  clear(BACK_COLOR)
  update_display()

def update_display():
  pg.display.flip()

def draw_text(text, xy, color, horz_center = True):
  img = font.render(text, True, color)
  if (horz_center):
    rect = img.get_rect(center = xy)
    screen.blit(img, rect)
  else:
    screen.blit(img, xy)

def draw_all_cities():
  for city in the_cities:
    draw_city(city)

def draw_city(city, bodycolor=0, outlinecolor=0, namecolor=0):
  if isinstance(city, int):
    city = the_cities[city]
  xy = xy2s([city.x, city.y])
  if isinstance(bodycolor, int): bodycolor = CITY_BODY_COLORS[bodycolor]
  if isinstance(outlinecolor, int): outlinecolor = CITY_OUTLINE_COLORS[outlinecolor]
  pg.draw.circle(screen, bodycolor, xy, CITY_RADIUS)
  pg.draw.circle(screen, outlinecolor, xy, CITY_RADIUS, 1)
  xy[1] -= FONT_SIZE // 2 + CITY_RADIUS
  if isinstance(namecolor, int): namecolor = CITY_NAME_COLORS[namecolor]

  if shows_city_index: 
    text = '%d.%s' % (city.index, city.name)
  elif hasattr(city, 'weight'):
    text = '%s %d' % (city.name, city.weight)  
  else:
    text = city.name

  draw_text(text, xy, namecolor)

def draw_edge(c1, c2, value=None, linecolor=0, textcolor=0):
  if isinstance(c1, int): c1 = the_cities[c1]
  if isinstance(c2, int): c2 = the_cities[c2]
  xy1, xy2 = city2s(c1), city2s(c2)
  if isinstance(linecolor, int): linecolor = EDGE_LINE_COLORS[linecolor]
  pg.draw.aaline(screen, linecolor, xy1, xy2)
  if value != None:
    xy = xy_center(xy1, xy2)
    if isinstance(textcolor, int): textcolor = EDGE_TEXT_COLORS[textcolor]
    draw_text('%d' % value, xy, color=textcolor)

INF = float('inf')
def draw_directed_edge(c1, c2, value=None, linecolor=0, textcolor=0):
  if isinstance(c1, int): c1 = the_cities[c1]
  if isinstance(c2, int): c2 = the_cities[c2]
  xy1, xy2 = city2s(c1), city2s(c2)
  if isinstance(linecolor, int): linecolor = EDGE_LINE_COLORS[linecolor]
  x1,y1 = xy1
  x2,y2 = xy2
  angle = math.atan2(y2-y1, x2-x1) + math.pi / 2
  shift_x = CITY_RADIUS * math.cos(angle)
  shift_y = CITY_RADIUS * math.sin(angle)
  sxy, dxy = shorter_line(x1+shift_x, y1+shift_y, x2+shift_x, y2+shift_y)
  pg.draw.aaline(screen, linecolor, sxy, dxy)
  draw_arrow(dxy, linecolor, sxy)
  # pg.draw.circle(screen, linecolor, dxy, CITY_RADIUS//2)
  # print(repr(c1), '->', repr(c2), value)
  if value != None and value != INF:
    xy = xy_center(dxy, sxy, 1.1)
    if isinstance(textcolor, int): textcolor = EDGE_TEXT_COLORS[textcolor]
    draw_text('%d' % value, xy, color=textcolor)

def shorter_line(x1,y1,x2,y2,sr=0.1,er=None):
  if er == None: er = sr
  dx1 = x1 + (x2-x1) * sr
  dy1 = y1 + (y2-y1) * sr
  dx2 = x2 - (x2-x1) * er
  dy2 = y2 - (y2-y1) * er
  return [dx1,dy1], [dx2,dy2]

def draw_arrow(xy2, linecolor, xy1):
  x1,y1 = xy1
  x2,y2 = xy2
  angle = math.atan2(y2-y1, x2-x1) + math.pi * 5 / 6 # 150 degree
  ax = x2 + CITY_RADIUS * math.cos(angle)
  ay = y2 + CITY_RADIUS * math.sin(angle)

  pg.draw.aaline(screen, linecolor, [x2,y2], [ax,ay])


def closest_init_brute():
  ctx.edges = []
  ctx.max_edges = 3

def closest_add(c1, c2, dist):
  at = -1
  for i in range(len(ctx.edges)):
    s,e,d = ctx.edges[i]
    if dist < d:
      at = i
      break
  if at >= 0:
    ctx.edges.insert(at, (c1, c2, dist))
  elif len(ctx.edges) < ctx.max_edges:
    ctx.edges.append((c1, c2, dist))
  ctx.edges = ctx.edges[:ctx.max_edges]

  clear()
  draw_all_cities()
  for s,e,d in ctx.edges:
    draw_edge(s, e, d)

  draw_edge(c1, c2, dist, textcolor=2)
  s,e,d = ctx.edges[0]
  draw_edge(s,e,d, textcolor=2)
  update_display()
  wait(1)
  clear()
  draw_all_cities()
  s,e,d = ctx.edges[0]
  draw_edge(s,e,d, textcolor=2)

def closest_init_dnc():
  ctx.stack = []
  ctx.max_level = 10
  ctx.closest = []

def closest_push(left, right, mid):
  ctx.stack.append((left, right, mid))
  draw_stack()

def closest_left(s, e, d):
  ctx.closest.append((s, e, d))

def draw_stack(wait_and_update=True):
  clear()
  margin_x = screen_size[0] // 20 // 2
  margin_y = screen_size[1] // 20 // 2
  y1 = margin_y
  y2 = screen_size[1] - margin_y
  x1 = margin_x
  x2 = screen_size[0] - margin_x
  prev_m = -2
  level = 0
  for (l, r, m) in ctx.stack:
    level += 1
    if prev_m == l - 1:
      x1 = mx
    elif prev_m == r:
      x2 = mx
    mxy1 = city2s(the_cities[m])
    mxy2 = city2s(the_cities[m+1])
    mx = (mxy1[0] + mxy2[0]) // 2
    draw_stack_rect(True, level, [x1, y1, mx-x1, y2-y1])
    draw_stack_rect(False, level, [mx, y1, x2-mx, y2-y1])
    x1 += 2
    x2 -= 2
    y1 += 2
    y2 -= 2
    prev_m = m

  draw_all_cities()
  for s,e,d in ctx.closest:
    draw_edge(s, e, d)

  if wait_and_update:
    update_display()
    wait(1000)

def draw_stack_rect(isleft, level, rect):
  bg, line = stack_rect_color(isleft, level)
  pg.draw.rect(screen, bg, rect)
  pg.draw.rect(screen, line, rect, 1)

def stack_rect_color(isleft, level):
  max_level = len(ctx.stack)

  r,g,b = 255,192,255
  if isleft: 
    b = 192
    r -= level * 10
  else:
    r = 192
    b -= level * 10

  bg = (r,g,b)
  line = (r//2, g//2, b//2)
  return bg, line

def closest_pop(ls, le, ld, rs, re, rd):
  ctx.stack.pop()
  ctx.closest.pop()
  draw_stack(False)
  if ld > rd:
    lc, rc = 1, 0
  else:
    lc, rc = 0, 1
  draw_edge(ls, le, ld, linecolor=lc)
  draw_edge(rs, re, rd, linecolor=rc)

  update_display()
  wait(1000)


def closest_strip(x1, x2, s, e, d):
  clear()
  draw_stack(False)
  sx1,_ = o2s(x1, 0)
  sx2,_ = o2s(x2, 0)

  margin_y = screen_size[1] // 20 // 2
  y1 = margin_y
  height = screen_size[1] - 2 * margin_y

  margin = 5
  rect = [sx1 - margin, y1, sx2 - sx1 + 2 * margin, height]
  pg.draw.rect(screen, CITY_BODY_COLORS[0], rect, 2)
  draw_edge(s, e, d)
  update_display()
  wait(1000)

def closest_close(s, e, d):
  clear()
  draw_stack(False)
  draw_edge(s, e, d)
  update_display()
  wait(1000)

def closest_dnc_brute(c1, c2, dist):
  draw_edge(c1, c2, dist)
  update_display()
  wait(1000)

def draw_all_edges(showsValue=False):
  for u,v,w in the_edges:
    if not showsValue: w = None
    draw_edge(u, v, w, linecolor=1, textcolor=1)

def mst_append(u, v, w, roots):
  draw_edge(u,v,w)
  if shows_roots:
    draw_roots(roots, u, v)
  update_display()
  wait(1000)

def mst_update_roots(u, v, roots):
  if not shows_roots: return
  draw_roots(roots, u, v)
  update_display()
  wait(1000)

def draw_roots(roots, u, v):
  sw, sh = screen_size
  rect = [ 0, sh - ROOTS_HEIGHT, sw, ROOTS_HEIGHT - 1]
  pg.draw.rect(screen, BACK_COLOR, rect)
  w = sw // len(roots)
  rect[0] = 1
  rect[2] = w - 2
  x,y = w // 2, sh - ROOTS_HEIGHT + FONT_SIZE
  for i in range(len(roots)):
    r = roots[i]
    if i == u:
      body = ROOTS_BODY_COLOR_CMP
    elif i == v:
      body = ROOTS_BODY_COLOR_EMP
    elif i == find_root(roots, v):
      body = ROOTS_BODY_COLOR_ROOT
    else:
      body = ROOTS_BODY_COLOR
    pg.draw.rect(screen, body, rect)
    pg.draw.rect(screen, ROOTS_EDGE_COLOR, rect, 1)
    draw_text(str(i), [x, y], TEXT_COLOR)
    draw_text(the_cities[i].name, [x, y + FONT_SIZE], TEXT_COLOR)
    draw_text(str(r), [x, y + 2 * FONT_SIZE], TEXT_COLOR)
    draw_text(the_cities[r].name, [x, y + 3 * FONT_SIZE], TEXT_COLOR)
    rect[0] += w
    x += w

def find_root(roots, u):
  if u != roots[u]:
    roots[u] = find_root(roots, roots[u]) # 경로압축
  return roots[u]

def prim_init(prim):
  global shows_roots
  shows_roots = True
  setup(prim.cities, prim.edges)
  ctx.data = prim
  ctx.updating_weight = None
  ctx.prevWeightIndices = dict()
  ctx.weightAnims = []

def dijkstra_init(dijkstra):
  prim_init(dijkstra)

def graph_show_adjacents(u=None, v=None, w=None):#adjs, weights=None, w=None, connects=None):
  clear()
  if u != None:
    ctx.u, ctx.v = u, v
    ctx.adjs = ctx.data.graph[v]

  for u1,v1,w1 in the_edges:
    draw_adj_edge(u1, v1, w1)

  for i in range(len(the_cities)):
    draw_adj_city(i)

  update_display()
  graph_draw_weights(ctx.data.weights)
  if w != None:
    ctx.weightAnims.append([v, 0, -1, w])

  animate_weights()

# fixed, grayed, fixing, adjacents, updating, 
def draw_adj_edge(u, v, w):
  if (u, v) == (ctx.u, ctx.v) or (u, v) == (ctx.v, ctx.u):
    linecolor = textcolor = 2
  elif u == ctx.v and v in ctx.adjs or v == ctx.v and u in ctx.adjs:
    linecolor = textcolor = 3
  elif (u,v) in ctx.data.mst or (v,u) in ctx.data.mst:
    # print((u,v), 'in mst')
    linecolor = textcolor = 0
  else:
    linecolor = textcolor = 1
  draw_edge(u, v, w, linecolor=linecolor, textcolor=textcolor)

# def prim_connects(u, v):
#   if v in ctx.data.connects and u == ctx.data.connects[v]:
#     return True
#   if u in ctx.data.connects and v == ctx.data.connects[u]:
#     return True
#   return False

def draw_adj_city(index):
  city = the_cities[index]
  if index == ctx.v:
    body = 3
    name = 0
  elif index == ctx.u:
    body = 2
    name = 0
  elif index in ctx.data.completed:
    body = 0
    name = 0
  else:
    body = 1
    name = 1
  draw_city(city, bodycolor=body, outlinecolor=body, namecolor=name)

def color_by_name(text):
  v = [0, 0, 0]
  i = 0
  for ch in text:
    v[i] += ord(ch)
    i = (i + 1) % 3

  for i in range(3):
    v[i] = 145 + v[i] % 11 * 11

  return (v[0], v[1], v[2])

def graph_update_weight(adj, weight):
  city = the_cities[adj]
  city.weight = weight
  ctx.updating_weight = adj
  # print('updating_weight:', ctx.updating_weight)
  w = ctx.data.graph[ctx.v][adj]
  draw_edge(ctx.v, adj, w, linecolor=4, textcolor=4)

  xy = city2s(city)
  draw_city(city)
  pg.draw.circle(screen, CITY_OUTLINE_COLORS[0], xy, CITY_RADIUS + 2, 1)
  update_display()
  wait(ROOT_ANIM_MILLIS // 2)
  graph_draw_weights(ctx.data.weights)
  animate_weights()

def animate_weights():
  erase_root_area()

  width = FONT_SIZE * 6
  frames = int(ROOT_ANIM_MILLIS / speed) // WAIT_ONE_FRAME_MILLIS
  if frames < 2: frames = 2
  for i in range(frames + 1):
    erase_root_area()
    for (v, s, e, w) in reversed(ctx.weightAnims):
      x = int(s * width + (e - s) * width * i / frames)
      draw_wait_box(v, x, w)
    pg.display.flip()
    wait(WAIT_ONE_FRAME_MILLIS)

  ctx.weightAnims = []

def draw_wait_box(v, x, prev_w):
  sw, sh = screen_size
  width = FONT_SIZE * 6
  rect = [ x + 1, sh - ROOTS_HEIGHT, width - 2, ROOTS_HEIGHT - 1 ]
  body = color_by_name(the_cities[v].name)
  pg.draw.rect(screen, body, rect)
  pg.draw.rect(screen, ROOTS_EDGE_COLOR, rect, 1)

  tx,ty = x + width // 2, sh - ROOTS_HEIGHT + FONT_SIZE

  u = ctx.data.connects[v]
  w = 0 if u == v else the_cities[v].weight#ctx.data.graph[u][v]
  draw_text('%d %s' % (u, the_cities[u].name), [tx, ty], TEXT_COLOR)
  draw_text('%d %s' % (v, the_cities[v].name), [tx, ty + FONT_SIZE], TEXT_COLOR)
  # print('prev_w=', prev_w, 'w=', w)
  if prev_w != w:
    draw_text(str(prev_w), [tx, ty + 2 * FONT_SIZE], TEXT_COLOR)
  draw_text('%d' % (w), [tx, ty + 3 * FONT_SIZE], TEXT_COLOR)

def erase_root_area():
  sw, sh = screen_size
  rect = [ 0, sh - ROOTS_HEIGHT, sw, ROOTS_HEIGHT]
  pg.draw.rect(screen, BACK_COLOR, rect)

def graph_draw_weights(weights):
  weights = copy.deepcopy(weights)
  sw, sh = screen_size
  width = FONT_SIZE * 6
  # x,y = width // 2, sh - ROOTS_HEIGHT + FONT_SIZE
  prev = copy.deepcopy(ctx.prevWeightIndices)
  # print('prev=', prev)
  ctx.prevWeightIndices = dict()
  ctx.weightAnims = []
  index = 0
  while weights:
    v, w = weights.popitem()
    (start, prev_w) = prev[v] if v in prev else (index-1, w)
    end = index
    ctx.weightAnims.append([v, start, end, prev_w])
    ctx.prevWeightIndices[v] = (index, w)
    index += 1

def graph_complete():
  ctx.adjs = []
  ctx.updating_weight = None
  ctx.u, ctx.v = None, None
  graph_show_adjacents()

def setcover_init(data):
  ctx.data = data
  setup(data.cities, data.edges)

def setcover_show(uncovered, cover, max):
  # print(ctx.data.city_set)
  print('Adding #%d:' % len(cover), the_cities[max].name, end=': ')
  if len(uncovered) < 10:
    for i in uncovered:
      print('%d.%s' % (i, the_cities[i].name), end=', ')
    print()
  else:
    print(uncovered)
  clear()
  for u,v,w in the_edges:
    lc = 0 if u in cover or v in cover else 1
    draw_edge(u, v, None, linecolor=lc)
  for i in range(len(the_cities)):
    if i in cover:
      body = line = 3
      name = 0
    elif i in uncovered:
      body = line = 1
      name = 1
    else:
      body = line = 0
      name = 0
    draw_city(the_cities[i], bodycolor=body, outlinecolor=line, namecolor=name)
  update_display()
  wait(1000)

def floyd_init(floyd):
  ctx.data = floyd
  ctx.on_mouse_motion = floyd_on_mouse
  ctx.u, ctx.v, ctx.k = None, None, None
  ctx.update = False
  setup(floyd.cities)
  global shows_city_index, diff_x
  shows_city_index = True
  diff_x *= 3 # make room for table

  global max_screen_x
  max_screen_x, _zero = o2s(max_x, 0)
  print('max_screen_x, _zero:', (max_screen_x, _zero))


  floyd_draw()

def floyd_compare(u, v, k):
  dgraph = ctx.data.dgraph
  msec = 1000
  if u == v or v == k or u == k: return
  if dgraph[u][k] == INF or dgraph[k][v] == INF:
    msec = 100
  ctx.u, ctx.v, ctx.k = u, v, k
  # print('floyd_compare:', u, v, k)
  ctx.update = False
  floyd_draw()
  draw_directed_edge(u, v, dgraph[u][v], linecolor=ROOTS_BODY_COLOR_UPDATE)
  draw_directed_edge(u, k, dgraph[u][k], linecolor=ROOTS_EDGE_COLOR)
  draw_directed_edge(k, v, dgraph[k][v], linecolor=ROOTS_EDGE_COLOR)
  update_display()
  wait(msec)

def floyd_update(u=None, v=None, k=None):
  ctx.u, ctx.v, ctx.k = u, v, k
  ctx.update = True
  # print('floyd_update:', k)
  floyd_draw()
  if u != None and v != None:
    value = ctx.data.dgraph[u][v]
    draw_directed_edge(u, v, value=value, linecolor=ROOTS_BODY_COLOR_UPDATE)
  update_display()
  wait(1000)

def floyd_draw():
  clear()
  draw_all_directed_edges(ctx.data.input)
  draw_known_path(ctx.u, ctx.v)
  draw_all_cities()
  draw_directed_edge_table()
  update_display()

def draw_known_path(u, v, color=TEXT_COLOR):
  if u == v: return
  if u == None: return
  while True:
    next_index = ctx.data.dirs[u][v]
    if next_index < 0: break
    value = ctx.data.dgraph[u][next_index]
    # print(u, next_index, value)
    draw_directed_edge(u, next_index, value=value, linecolor=color)
    if next_index == v: break
    u = next_index

def draw_all_directed_edges(dgraph, linecolor=3):
  for u, dests in dgraph.items():
    for v, w in dests.items():
      if w != INF:
        draw_directed_edge(u, v, w, linecolor=linecolor)

def draw_directed_edge_table():
  dgraph = ctx.data.dgraph
  n_cities = len(the_cities)
  table_x = max_screen_x + 2 * ROOTS_HEIGHT
  # print('RH:', ROOTS_HEIGHT, 'mx:', max_x, 'tx:', table_x)
  table_y = ROOTS_HEIGHT
  cell_w = (screen_size[0] - ROOTS_HEIGHT - table_x) // (n_cities + 1)
  cell_h = (screen_size[1] - ROOTS_HEIGHT - table_y) // (n_cities + 1)

  if ctx.k != None:
    xy = [table_x + cell_w // 2, table_y + cell_h // 2]
    draw_text('k=%d' % ctx.k, xy, TEXT_COLOR)
  y = table_y
  for u in range(-1, n_cities):
    x = table_x
    for v in range(-1, n_cities):
      if u < 0 and v < 0: 
        x += cell_w
        continue
      if u < 0 or v < 0:
        city = the_cities[u if u >= 0 else v]
        text = '%d.%s' % (city.index, city.name)
        color = (220, 220, 255)
      elif dgraph[u][v] != INF:
        text = dgraph[u][v]
        color = BACK_COLOR
      else:
        text = "∞"
        color = ROOTS_BODY_COLOR

      willUpdate = False
      if u == ctx.u and v == ctx.v:
        if ctx.update:
          color = ROOTS_BODY_COLOR_UPDATE 
        else:
          color = ROOTS_BODY_COLOR_VIA
          if dgraph[u][ctx.k] + dgraph[ctx.k][v] < dgraph[u][v]:
            willUpdate = True
      elif u == ctx.u and v == ctx.k:
        color = ROOTS_BODY_COLOR_CMP_1
      elif u == ctx.k and v == ctx.v:
        color = ROOTS_BODY_COLOR_CMP_2

      draw_de_table_cell(x, y, text, cell_w, cell_h, color)
      if willUpdate:
        radius = min(cell_w, cell_h) // 2
        tx, ty = x + cell_w // 2, y + cell_h // 2
        color = ROOTS_BODY_COLOR_UPDATE
        pg.draw.circle(screen, color, [tx, ty], radius, 1)
      x += cell_w
    y += cell_h

def draw_de_table_cell(x, y, value, w, h, bodycolor=BACK_COLOR):
  rect = [x, y, w+1, h+1]
  pg.draw.rect(screen, bodycolor, rect)
  pg.draw.rect(screen, ROOTS_LIGHT_COLOR, rect, 1)

  tx, ty = x + w // 2, y + h // 2
  vstr = "∞" if value == None else str(value)
  draw_text(vstr, [tx, ty], TEXT_COLOR)

# def floyd_end():
#   loop = True
#   while loop:
#     for e in pg.event.get():
#       if e.type == pg.QUIT:
#         loop = False
#       elif e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
#         loop = False
#       elif e.type == pg.MOUSEMOTION:
#         floyd_on_mouse()
#   pg.quit()

def floyd_on_mouse():
  x, y = pg.mouse.get_pos()
  n_cities = len(the_cities)

  table_x = max_screen_x + 2 * ROOTS_HEIGHT
  table_y = ROOTS_HEIGHT
  cell_w = (screen_size[0] - ROOTS_HEIGHT - table_x) // (n_cities + 1)
  cell_h = (screen_size[1] - ROOTS_HEIGHT - table_y) // (n_cities + 1)

  u = (y - table_y) // cell_h - 1
  v = (x - table_x) // cell_w - 1

  if u >= 0 and u < ctx.data.n_cities and \
     v >= 0 and v < ctx.data.n_cities:
    ctx.u, ctx.v = u, v
  else:
    ctx.u, ctx.v = None, None

  # print('ctx.u, ctx.v:', ctx.u, ctx.v)
  floyd_draw()

if __name__ == '__main__':
  from city import *
  # global shows_city_index
  init('Test')
  setup(five_letter_cities[:100])

  draw_all_cities()
  update_display()

  end()

