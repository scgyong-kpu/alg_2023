from vis.planar import *
from copy import deepcopy

class EulerVisualizer(PlanarVisualizer):
  def_city_context = {
    'city_body_color': Color.LightBlue,
    'city_line_color': Color.DeepSkyBlue,
    'city_name_color': Color.DarkBlue,
    'shows_city_index': True,
    # 'shows_city_coord': True,
  }
  cctx_mark = {
    'city_body_color': Color.Crimson,
    'city_line_color': Color.line,
    'city_name_color': Color.DarkRed,
    'shows_city_index': True,
    # 'shows_city_coord': True,
  }
  cctx_cand = {
    'city_body_color': Color.Ivory,
    'city_line_color': Color.Silver,
    'city_name_color': Color.Gray,
    'shows_city_index': True,
  }
  cctx_finish = {
    'city_body_color': Color.RoyalBlue,
    'city_line_color': Color.Navy,
    'city_name_color': Color.MidnightBlue,
    'shows_city_index': True,
  }
  def_edge_context = {
    'edge_line_color': Color.Lime,
    'edge_value_color': Color.DarkOliveGreen,
  }
  ectx_removed = {
    'edge_line_color': Color.LemonChiffon,
    # 'edge_value_color': Color.Gray,
  }
  ectx_finished = {
    'edge_line_color': Color.FireBrick,
    # 'edge_value_color': Color.Gray,
  }
  def setup(self, data):
    super().setup(data)
    self.copy_adj_list = []
    self.visit_stack = []
    self.visit_set = set()
    self.visit_edges = []
    self.cycle_index = -1
    for sub in data.adj_list:
      self.copy_adj_list.append(deepcopy(sub))
    # self.copy_adj_list = deepcopy(data.adj_list)
    self.curr_vertex = -1
    self.cand_vertex = -1
    self.orders = dict()
  def mark_vertex(self, index):
    self.curr_vertex = index
    self.set_city_context(index, self.cctx_mark)
    self.draw()
    self.wait(1000)
  def remove_edge(self, u, v):
    self.cycle_index = v
    self.set_city_context(v, self.cctx_cand)
    self.set_edge_context(u, v, self.ectx_removed)
    self.draw()
    self.wait(1000)
  def revive_edge(self, u, v):
    # print(f'revive_edge({u},{v})')
    self.set_city_context(v, self.def_city_context)
    self.set_edge_context(u, v, self.def_edge_context)
    self.draw()
    self.wait(1000)
  def settle_edge(self, u, v):
    # print('settle_edge', self.data.visited)
    self.curr_vertex = -1
    if not u in self.orders:
      self.orders[u] = len(self.orders)
    finished = len(self.data.adj_list[u]) == 0
    cctx = self.cctx_finish if finished else self.def_city_context
    self.set_city_context(u, cctx)
    # alive = v in self.data.adj_list[u]
    # ectx = def_edge_context if alive else self.ectx_finished
    self.set_edge_context(u, v, self.ectx_finished)
    self.draw()
    self.wait(1000)
  def dfs_push(self, index=-1):
    if index < 0:
      self.visit_stack = []
      self.visit_set = set()
      self.visit_edges = []
    else:
      top = self.visit_stack[-1] if self.visit_stack else -1
      self.visit_stack.append(index)
      self.visit_set.add(index)
      if top >= 0:
        self.visit_edges.append((top, index))
    self.draw()
    self.wait(500)
  def dfs_pop(self):
    if self.visit_stack:
      prev_top = self.visit_stack.pop()
      wait = 100
    else:
      wait = 1000
      print('already empty')

    if self.visit_stack:
      top = self.visit_stack[-1]
      self.visit_edges.append((prev_top, top))
    else:
      self.visit_set = set()
      self.visit_edges = []
    self.draw()
    self.wait(wait)

  def finish_euler(self, vertices):
    self.visit_stack = vertices
    self.visit_edges = []
    u = vertices[0]
    for i in range(1, len(vertices)):
      v = vertices[i]
      self.visit_edges.append((u, v))
      self.draw()
      self.wait(100)
      u = v

  def calc_coords(self):
    super().calc_coords()
    self.city_radius *= 3

  def draw_content(self, **args):
    self.draw_all_copy_adj_list()
    self.draw_all_cities()
    self.draw_visit_edges()
    if self.visit_stack and self.cycle_index in self.visit_set:
      self.draw_cycled()

  def draw_cycled(self):
    x,y = self.o2s(self.max_x, self.min_y)
    x += self.separator_size
    self.draw_text('CYCLES !!', [x,y], center=False)


  def draw_visit_edges(self):
    for u, v in self.visit_edges:
      self.draw_directed_edge(u, v, edge_line_color=Color.HotPink)

  def draw_all_copy_adj_list(self):
    for u in range(len(self.copy_adj_list)):
      for v in self.copy_adj_list[u]:
        if u >= v: continue
        ctx = self.get_edge_context(u, v)
        if not ctx: ctx = self.def_edge_context
        self.draw_edge(u, v, None, **ctx)

  def draw_city(self, city, **args):
    super().draw_city(city, **args)
    self.draw_visited(city)
    if city == self.curr_vertex:
      xy = self.city2s(self.data.cities[city])
      self.draw_text(f'{len(self.data.adj_list[city])}', xy)
    elif city in self.orders:
      xy = self.city2s(self.data.cities[city])
      order = self.orders[city] + 1
      self.draw_text(f'{order}', xy)


  def draw_visited(self, index):
    if not isinstance(index, int): return
    if not index in self.visit_set: return
    city = self.data.cities[index]
    xy = self.xy2s([city.x, city.y])
    radius = 1.2 * self.city_radius
    pg.draw.circle(self.screen, Color.line, xy, radius, 1)
