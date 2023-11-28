import math
from vis.base import *
from welzl import welzl

# t = 0.0 ~ 2.0 사이로 변화하는 값임. 1 이면 가운데임
def lerp_2d(xy1, xy2, t=1):
  # x1,y1 = xy1[0], xy1[1]
  # x2,y2 = xy2[0], xy2[1]
  x1,y1,x2,y2 = *xy1, *xy2
  return [(x1*(2-t)+x2*t)//2, (y1*(2-t)+y2*t)//2]

# 평면 시각화
class PlanarVisualizer(Visualizer):
  def_city_context = {
    'city_body_color': Color.LightBlue,
    'city_line_color': Color.DeepSkyBlue,
    'city_name_color': Color.DarkBlue,
    # 'shows_city_index': True,
    # 'shows_city_coord': True,
  }
  def_edge_context = {
    'edge_line_color': Color.Teal,
    'edge_value_color': Color.DarkGreen,
  }

  def setup(self, data):
    self.data = data
    self.compute_min_max()
    self.city_contexts = dict()
    self.edge_contexts = dict()
    self.legend_right = self.separator_size
    self.legend_bottom = self.separator_size
    # self.draw()

  def compute_min_max(self):
    min_x, max_x = float('inf'), float('-inf')
    min_y, max_y = float('inf'), float('-inf')
    for c in self.data.cities:
      if min_x > c.x: min_x = c.x
      if min_y > c.y: min_y = c.y
      if max_x < c.x: max_x = c.x
      if max_y < c.y: max_y = c.y
    self.min_x, self.max_x = min_x, max_x
    self.min_y, self.max_y = min_y, max_y

    self.diff_x = max_x - min_x
    self.diff_y = max_y - min_y

  def get_city_context(self, index):
    if index in self.city_contexts:
      return self.city_contexts[index]
    return None

  def set_city_context(self, index, context=None):
    if context == None:
      if index in self.city_contexts:
        del self.city_contexts[index]
    else:
      self.city_contexts[index] = context

  def get_edge_context(self, u,v):
    if u > v: u,v = v,u
    if (u,v) in self.edge_contexts:
      return self.edge_contexts[(u,v)]
    return None

  def set_edge_context(self, u,v, context):
    if u > v: u,v = v,u
    if context == None:
      del self.edge_contexts[(u,v)]
    else:
      self.edge_contexts[(u,v)] = context

  def draw(self, wait_msec=0):
    self.clear()
    self.calc_coords()
    self.draw_content()
    self.update_display()
    if wait_msec > 0:
      self.wait(wait_msec)

  def draw_content(self):
    if hasattr(self.data, 'edges'):
      self.draw_all_edges()
    self.draw_all_cities()

  def calc_coords(self):
    cw = self.config.screen_width - self.separator_size - self.legend_right
    ch = self.config.screen_height - self.separator_size - self.legend_bottom

    scale_x, scale_y = cw / self.diff_x, ch / self.diff_y
    if scale_x < scale_y:
      self.scale = scale_x
      self.diff = self.diff_x
    else:
      self.scale = scale_y
      self.diff = self.diff_y

    self.city_radius = self.config.font_size // 3

  def o2s(self, x, y):
    dx, dy = x - self.min_x, y - self.min_y
    x = self.separator_size + dx * self.scale
    y = self.separator_size + dy * self.scale
    return [x, y]

  def xy2s(self, xy):
    return self.o2s(xy[0], xy[1])

  def city2s(self, city):
    return self.xy2s([city.x, city.y])

  def draw_all_cities(self, **args):
    uses_ctx = len(args) == 0
    for i in range(len(self.data.cities)):
      if uses_ctx:
        ctx = self.get_city_context(i)
        if not ctx: ctx = self.def_city_context
      else:
        ctx = args
      self.draw_city(i, **ctx)

  def draw_all_edges(self, **args):
    uses_ctx = len(args) == 0
    for u,v,w in self.data.edges:
      if uses_ctx:
        ctx = self.get_edge_context(u, v)
        if not ctx: ctx = self.def_edge_context
      else:
        ctx = args
      self.draw_edge(u,v,w, **ctx)

  def draw_city(self, city, **args):
    if isinstance(city, int):
      city = self.data.cities[city]
    xy = self.xy2s([city.x, city.y])
    body_color = attr(args, 'city_body_color', Color.back)
    line_color = attr(args, 'city_line_color', Color.line)
    name_color = attr(args, 'city_name_color', Color.text)

    # def_city_context = {
    #   'city_body_color': Color.DeepSkyBlue,
    #   'city_line_color': Color.LightBlue,
    #   'city_name_color': Color.DarkBlue,

    radius = self.city_radius
    pg.draw.circle(self.screen, body_color, xy, radius)
    pg.draw.circle(self.screen, line_color, xy, radius, 1)

    xy[1] -= self.config.font_size // 2 + radius
    name = city.getName(**args)

    self.draw_text(name, xy, text_color=name_color, **args)

  def draw_edge(self, c1, c2, value=None, **args):
    if isinstance(c1, int): c1 = self.data.cities[c1]
    if isinstance(c2, int): c2 = self.data.cities[c2]
    xy1, xy2 = self.city2s(c1), self.city2s(c2)
    line_color = attr(args, 'edge_line_color', Color.line)
    thickness = attr(args, 'edge_line_width', 1)
    if thickness == 1:
      pg.draw.aaline(self.screen, line_color, xy1, xy2)
    else:
      pg.draw.line(self.screen, line_color, xy1, xy2, thickness)
    if value != None:
      shows_value = attr(args, 'shows_edge_value', False)
      if shows_value:
        xy = lerp_2d(xy1, xy2)
        value_color = attr(args, 'edge_value_color', Color.text)
        self.draw_text(f'{value}', xy, text_color=value_color)

  def draw_directed_edge(self, c1, c2, value=None, **args):
    if isinstance(c1, int): c1 = self.data.cities[c1]
    if isinstance(c2, int): c2 = self.data.cities[c2]
    x1,y1,x2,y2 = *self.city2s(c1), *self.city2s(c2)
    angle = math.atan2(y2-y1, x2-x1)
    shift_angle = angle + math.pi / 2
    radius = self.city_radius // 2
    shift_x = radius * math.cos(shift_angle)
    shift_y = radius * math.sin(shift_angle)
    sxy, dxy = self.shorter_line(x1+shift_x, y1+shift_y, x2+shift_x, y2+shift_y, angle)
    self.draw_arrow(sxy, dxy, angle, value, **args)

  def draw_arrow(self, sxy, dxy, angle=None, value=None, **args):
    line_color = attr(args, 'edge_line_color', Color.line)
    axy = self.get_arrow_pos(sxy, dxy, angle)
    pg.draw.aaline(self.screen, line_color, sxy, dxy)
    pg.draw.aaline(self.screen, line_color, dxy, axy)

    if value != None:
      shows_value = attr(args, 'shows_edge_value', False)
      if shows_value:
        xy = lerp_2d(sxy, dxy, 1.1) # at 55% position (1=50%, 2=100%)
        value_color = attr(args, 'edge_value_color', Color.line)
        self.draw_text(f'{value}', xy, text_color=value_color)

  def shorter_line(self, x1,y1,x2,y2,angle=None):
    diff = 2 * self.city_radius
    if angle == None:
      angle = math.atan2(y2-y1, x2-x1)
    dx = diff * math.cos(angle)
    dy = diff * math.sin(angle)
    return [x1+dx,y1+dy], [x2-dx,y2-dy]

  def get_arrow_pos(self, xy1, xy2, angle=None):
    length = 2 * self.city_radius
    x1,y1 = xy1
    x2,y2 = xy2
    if angle == None:
      angle = math.atan2(y2-y1, x2-x1)
    angle += math.pi * 5 / 6 # 150 degree
    ax = x2 + length * math.cos(angle)
    ay = y2 + length * math.sin(angle)
    return [ax, ay]


class KruskalVisualizer(PlanarVisualizer):
  normal_city_context = {
    'city_body_color': Color.LightBlue,
    'city_line_color': Color.DeepSkyBlue,
    'city_name_color': Color.DarkBlue,
    'shows_city_index': True,
    # 'shows_city_coord': True,
  }
  def_city_context = normal_city_context
  grayed_edge_context = {
    'edge_line_color': Color.WhiteSmoke,
    'edge_value_color': Color.WhiteSmoke,
    'shows_edge_value': True,
  }
  def_edge_context = {
    'edge_line_color': Color.Teal,
    'edge_value_color': Color.DarkGreen,
    'shows_edge_value': True,
  }
  ectx_ignore = {
    'edge_line_color': Color.Crimson,
    'edge_value_color': Color.DarkRed,
    'edge_line_width': 5,
    'shows_edge_value': True,
  }
  bctx_current = {
    'body_color': Color.LightSalmon,
    'line_color': Color.DarkRed,
    'text_color': Color.Indigo,
  }

  def setup(self, data):
    super().setup(data)
    self.candidates = []
    self.max_weight = max(e[2] for e in data.edges)
    self.appended_edge = (-1, -1)

  def calc_coords(self):
    self.legend_right = self.config.screen_width // 3
    self.legend_bottom = self.config.screen_height // 3

    super().calc_coords()

    self.weights_y = self.config.screen_height - self.legend_bottom + self.separator_size
    self.weights_w = self.config.screen_width - self.legend_right - self.separator_size
    self.weights_h = self.legend_bottom - 2 * self.separator_size

    self.roots_x = self.config.screen_width - self.legend_right + self.separator_size
    self.roots_w = self.legend_right - 2 * self.separator_size
    self.roots_x2 = self.roots_x + self.roots_w // 2
    self.roots_y = self.separator_size
    self.roots_h = self.config.screen_height - 2 * self.separator_size
    self.root_h = max(self.config.font_size, self.roots_h // len(self.data.cities))

  def draw_content(self):
    if hasattr(self.data, 'edges'):
      self.draw_all_edges()
    self.draw_all_cities(**self.def_city_context)

    self.draw_candidates()
    self.draw_right_pane()

  def get_edge_context(self, u,v):
    if u > v: u,v = v,u
    if (u,v) in self.candidates:
      return self.grayed_edge_context
    return super().get_edge_context(u, v)

  def sort_edges(self):
    self.candidates = []
    self.weights = dict()
    max_weight = 0
    for u,v,w in self.data.edges:
      if u > v: u,v = v,u
      self.candidates.append((u,v))
      self.weights[(u,v)] = w
      if max_weight < w:
        max_weight = w
      self.draw()
      self.wait(100)
    self.max_weight = max_weight

  def draw_candidates(self):
    x = self.separator_size
    y = self.weights_y
    legend = self.weights_h
    ix = self.weights_w // len(self.data.edges)
    for u,v,w in self.data.edges:
      if u > v: u,v = v,u
      if (u,v) in self.candidates:
        color = Color.Crimson
      else:
        color = Color.WhiteSmoke
      height = legend * w / self.max_weight
      pg.draw.line(self.screen, color, [x,y], [x,y+height])
      x += ix

  def append(self, u, v, w):
    if u > v: u,v = v,u
    if (u,v) in self.candidates:
      del self.candidates[self.candidates.index((u,v))]

    self.appended_edge = (u,v)
    self.draw()
    self.wait(1000)

  def ignore(self, u, v, w):
    if u > v: u,v = v,u
    self.draw()
    self.draw_edge(u, v, w, **self.ectx_ignore)
    self.update_display()
    self.wait(1000)

  def draw_right_pane(self):
    if not hasattr(self.data, 'roots'): return

    x = self.roots_x
    y = self.roots_y
    w = self.roots_w
    h = self.root_h
    u,v = self.appended_edge
    for i in range(len(self.data.roots)):
      r = self.data.roots[i]
      ci = self.data.cities[i]
      cr = self.data.cities[r]
      if i == v:
        ctx = self.bctx_current
      else:
        ctx = {}
      self.draw_box([x,y,w,h], text=f'{ci.index}.{ci.name} - {cr.index}.{cr.name}', **ctx)
      y += h

  def finish(self):
    self.appended_edge = -1, -1
    self.draw()

class PrimVisualizer(KruskalVisualizer):
  grayed_city_context = {
    'city_body_color': Color.WhiteSmoke,
    'city_line_color': Color.LightGray,
    'city_name_color': Color.LightGray,
    'shows_city_index': True,
    # 'shows_city_coord': True,
  }
  candidate_city_context = {
    'city_body_color': Color.PaleGreen,
    'city_line_color': Color.Magenta,
    'city_name_color': Color.SkyBlue,
    'shows_city_index': True,
    # 'shows_city_coord': True,
  }
  candidate_edge_context = {
    'edge_line_color': Color.LightGray,
    'edge_value_color': Color.SkyBlue,
    'shows_edge_value': True,
  }
  bctx_updated = {
    'body_color': Color.LightGreen,
    'line_color': Color.DarkGreen,
    'text_color': Color.text,
  }
  def_city_context = grayed_city_context
  def_edge_context = KruskalVisualizer.grayed_edge_context
  fixed_edge_context = KruskalVisualizer.def_edge_context
  fixing_edge_context = {
    'edge_line_color': Color.Crimson,
    'edge_value_color': Color.DarkRed,
    'shows_edge_value': True,
    'edge_line_width': 5,
  }
  compare_edge_context = {
    'edge_line_color': Color.LightGreen,
    'edge_value_color': Color.DarkGreen,
    'shows_edge_value': True,
    'edge_line_width': 5,
  }


  def setup(self, data):
    super().setup(data)
    self.weights = []
    self.connections = dict()
    self.fixing_index = -1
    self.current_index = -1

    self.wi_map = []
    # self.push_index = -1
    # self.pop_index = -1
    self.update_index = -1
    # self.downs = set()
    # self.ups = set()

  def draw_content(self):
    if hasattr(self.data, 'edges'):
      self.draw_all_edges()
    self.draw_all_cities()

    # self.draw_candidates()
    self.draw_right_pane()

  def draw_right_pane(self):
    bx = self.roots_x
    by = self.roots_y
    bw = self.roots_w
    bh = self.root_h

    for i in range(len(self.weights)):
      weight, ci = self.weights[i]
      tx, ty = bx, by + i * bh
      if self.wi_map:
        mv = self.wi_map[i]
        if mv == -10: # push
          tx += (1 - self.anim_progress) * bw
        elif mv == -20: # pop
          tx += self.anim_progress * bw
        else:
          # print(f'{mv=} vs {i=} - {self.fixing_index=}')
          if self.fixing_index >= 0:
            prog = self.anim_progress
          else:
            prog = 1 - self.anim_progress
          ty += prog * bh * (mv - i)
        # elif mv < i:
        #   print(f'{mv=} < {i=}')
        #   ty = by + mv * bh + (i-mv) * bh * (self.anim_progress)

      city = self.data.cities[ci]
      text = f'{weight} - {city.index}.{city.name}'
      if ci == self.update_index:
        ctx = self.bctx_updated
        pw, pi = self.prev_weight
        # pc = self.data.cities[pi]
        # text = f'{pc.index}.{pc.name} - {pw} > {text}'
        text = f'{pw} > {text}'

      elif ci == self.fixing_index:
        ctx = self.bctx_current
      else:
        ctx = { 'no_body': True }
      self.draw_box([tx,ty,bw,bh], text=text, **ctx)

    # horz_ci = -1
    # anim_ty = 0
    # wi = 0
    # end_wi = -1
    # for weight, ci in self.weights:
    #   city = self.data.cities[ci]
    #   text = f'{weight} - {city.index}.{city.name}'
    #   ctx = { 'no_body': True }#self.bctx_current
    #   x = bx
    #   if ci == self.push_index:
    #     x += (1 - self.anim_progress) * self.roots_w
    #     anim_ty = (1-self.anim_progress) * h
    #     horz_ci = self.push_index
    #   elif ci == self.pop_index:
    #     x += (self.anim_progress) * self.roots_w
    #     anim_ty = self.anim_progress * h
    #     horz_ci = self.pop_index
    #   elif ci == self.update_index:
    #     ctx = self.bctx_updated
    #     end_wi = wi + self.up_level
    #     anim_ty = -(1-self.anim_progress) * h * self.up_level
    #   elif ci == self.fixing_index:
    #     ctx = self.bctx_current

    #   if ci != self.update_index:
    #     if wi <= end_wi:
    #       anim_ty = (1-self.anim_progress) * h
    #     else:
    #       end_wi = -1
    #       anim_ty = 0

    #   ty = y
    #   if anim_ty != 0 and ci != horz_ci: ty -= anim_ty
    #   self.draw_box([x,ty,w,h], text=text, **ctx)
    #   y += h

    #   wi += 0

  def draw_city(self, city, **args):
    if city == self.current_index:
      radius = self.config.font_size
      c = self.data.cities[city]
      pg.draw.circle(self.screen, Color.line, self.city2s(c), radius, 1)
    super().draw_city(city, **args)

  # def get_edge_context(self, u,v):

  def append(self, weight, ci, c2=None):
    self.set_city_context(ci, self.candidate_city_context)
    if c2 != None:
      self.connections[ci] = c2
      self.set_edge_context(ci, c2, self.candidate_edge_context)

    self.wi_map = [ x for x in range(len(self.weights)) ]
    for i in range(len(self.weights)):
      w, c = self.weights[i]
      if weight < w:
        self.weights.insert(i, (weight, ci))
        self.wi_map.insert(i, -10)
        break
    else:
      self.weights.append((weight, ci))
      self.wi_map.append(-10)

    # self.push_index = ci
    # msec = 1000 if c2 == None else 500
    self.animate(1000)
    # self.push_index = -1
    # self.sort_weights()
    self.wi_map = []
    self.draw()

  def sort_weights(self):
    self.weights.sort(key=lambda e:e[0])

  def update(self, weight, ci, ci_from):
    # print('update', weight, ci)
    for i in range(len(self.weights)):
      w, c = self.weights[i]
      if c == ci:
        wi = i
        break
    else: 
      print('update', weight, ci)
      return

    ci_orig = self.connections[ci]
    self.connections[ci] = ci_from
    self.set_edge_context(ci, ci_from, self.candidate_edge_context)
    self.set_edge_context(ci, ci_orig, self.compare_edge_context)
    self.update_index = ci
    self.wi_map = [ x for x in range(len(self.weights)) ]
    pw, pci = self.weights.pop(wi)
    self.prev_weight = pw, ci_from
    self.wi_map.pop(wi)
    for i in range(len(self.weights)):
      w, c = self.weights[i]
      if weight < w:
        self.weights.insert(i, (weight, ci))
        self.wi_map.insert(i, wi)
        break
    else:
      self.wi_map.append(len(self.weights))
      self.weights.append((weight, ci))
    # print(f'>{self.wi_map=} {self.weights=}')
    self.animate(1000)
    self.update_index = -1
    # self.sort_weights()
    self.wi_map = []
    self.set_edge_context(ci, ci_orig, None)
    self.draw()

  def fix(self, ci, ci_from=None):
    self.current_index = ci
    self.connections[ci_from] = ci
    if ci != ci_from:
      self.fixing_index = ci
      self.set_edge_context(ci_from, ci, self.fixing_edge_context)
      self.draw()
      self.wait(300)
      self.set_edge_context(ci_from, ci, self.fixed_edge_context)
    self.set_city_context(ci, self.normal_city_context)
    # self.pop_index = ci
    found = 0
    self.wi_map = []
    for i in range(len(self.weights)):
      if self.weights[i][1] == ci:
        found = -1
        value = -20
      else:
        value = i + found
      self.wi_map.append(value)

    self.animate(1000)
    self.wi_map = []
    for cc in self.data.completed:
      if cc == ci_from: continue
      if self.get_edge_context(ci, cc) == None: continue
      self.set_edge_context(ci, cc, None)
    for i in range(len(self.weights)):
      if self.weights[i][1] == ci:
        self.weights.pop(i)
        break

    self.fixing_index = -1
    self.draw()

  def compare(self, ci, ci_from, value = 0, add=False):
    if add:
      if not ci in self.data.weights:
        return self.append(value, ci, ci_from)
      w = self.data.weights[ci]
      if value < w:
        return self.update(value, ci, ci_from)
    self.prev_weight = value, ci_from
    self.update_index = ci
    self.set_edge_context(ci_from, ci, self.compare_edge_context)
    self.draw()
    self.wait(1000)
    self.update_index = -1
    self.set_edge_context(ci_from, ci, None)
    self.draw()

  def finish(self):
    self.current_index = -1
    # print(self.weights)
    self.draw()

class DijkstraVisualizer(PrimVisualizer):
  cctx_start = {
    'city_body_color': Color.Crimson,
    'city_line_color': Color.line,
    'city_name_color': Color.text,
    'shows_city_index': True,
    # 'shows_city_coord': True,
  }

  def setup(self, data):
    super().setup(data)
    self.start_index = -1
    self.dists = dict()

  def set_start(self, index):
    self.start_index = index

  def append(self, weight, ci, c2=None):
    super().append(weight, ci, c2)
    self.dists[ci] = weight

  def update(self, weight, ci, ci_from):
    super().update(weight, ci, ci_from)
    self.dists[ci] = weight

  def get_city_context(self, index):
    if index == self.start_index:
      return self.cctx_start
    return super().get_city_context(index)

  def draw_city(self, city, **args):
    super().draw_city(city, **args)
    if isinstance(city, int):
      city_index = city
      city = self.data.cities[city]
    else:
      city_index = city.index

    if not city_index in self.dists:
      return

    text = str(self.dists[city_index])

    xy = self.xy2s([city.x, city.y])
    name_color = attr(args, 'city_name_color', Color.text)

    radius = self.city_radius
    xy[1] += self.config.font_size // 2 + radius

    self.draw_text(text, xy, text_color=name_color, **args)

class SetCoverVisualizer(Visualizer):
  bctx_removed = {
    'line_color': Color.LightSalmon,
    'text_color': Color.LightSalmon,
  }
  bctx_normal = {}
  bctx_fixing = {
    'line_color': Color.line,
    'text_color': Color.text,
    'body_color': Color.IndianRed,
    'width': 2,
  }
  bctx_fixing_without_body = {
    'line_color': Color.line,
    'text_color': Color.Crimson,
    'no_body': True,
    'width': 2,
  }
  bctx_comp = bctx_fixing
  bctx_fixed = {
    'line_color': Color.Teal,
    'text_color': Color.DarkGreen,
    'body_color': Color.LightBlue,
    'width': 2,
  }
  bctx_max_count = {
    'line_color': Color.Green,
    'no_body': True,
  }
  def setup(self, data):
    # super().setup(data)
    self.data = data
    self.counts = []
    self.current_idx = -1
    self.fixing_index = -1
    self.comp_el = None

  def draw(self, wait_msec=0):
    self.clear()
    self.calc_coords()
    self.draw_content()
    self.update_display()
    if wait_msec > 0:
      self.wait(wait_msec)

  def reset(self):
    self.f_idxs = [ i for i in range(len(self.data.f))]
    self.counts = [ 0 for _ in range(len(self.data.f))]

  def comp(self, fi, el=None, cnt=0):
    self.current_idx = self.f_idxs[fi]
    self.counts[self.current_idx] = cnt
    self.comp_el = el
    self.draw()
    self.wait(100)

  def fix(self, fidx):
    self.comp_el = None
    self.current_idx = -1
    self.fixing_index = self.f_idxs[fidx]
    self.draw()
    self.wait(1000)
    self.f_idxs.pop(fidx)
    self.fixing_index = -1
    self.counts = [ 0 for _ in range(len(self.data.f))]
    self.draw()
    self.wait(1000)

  def count_elements(self):
    for fi in self.f_idxs:
      self.counts[fi] = len(self.data.U & self.data.f[fi])
    self.draw()

  def calc_coords(self):
    self.table_x = self.config.screen_width // 2
    self.cell_w = self.config.font_size * 4
    self.cell_spacing = self.cell_w * 3 // 2
    self.cells_in_a_row = self.table_x // self.cell_spacing

    if not hasattr(self.data, 'f'): return
    subsets_h = self.config.screen_height - 2 * self.separator_size
    self.subset_h = subsets_h // len(self.data.f)

  def draw_content(self):
    # if not hasattr(self.data, 'U'): return
    self.draw_u_elements()
    self.draw_f_elements()

  def draw_u_elements(self):
    if not hasattr(self.data, 'u'): return
    sx = self.separator_size
    sy = self.separator_size
    x, y, w, h = sx, sy, self.cell_w, self.cell_w
    u = list(self.data.u)
    for i in range(len(u)):
      el = u[i]
      ctx = self.get_el_ctx(el)
      # print(f'{el=} {self.comp_el=} {ctx}')
      self.draw_box([x,y,w,h], f'{el}', border_radius=w//3, **ctx)
      x += self.cell_spacing
      if x + self.cell_spacing > self.table_x:
        x, y = sx, y + self.cell_spacing

  def get_el_ctx(self, el, compares=True):
    if not el in self.data.U:
      return self.bctx_removed
    if compares and el == self.comp_el:
      return self.bctx_comp
    return self.bctx_normal

  def get_fi_ctx(self, fi, el):
    # print(f'{fi=} {self.fixing_index=} {self.f_idxs=}')
    if fi == self.current_idx and el == self.comp_el:
      return self.bctx_comp
    if fi == self.fixing_index:
      if el in self.data.U:
        return self.bctx_fixing
      else:
        return self.bctx_fixing_without_body
    if fi in self.f_idxs:
      return self.get_el_ctx(el, False)
    else:
      return self.bctx_fixed

  def draw_f_elements(self):
    if not hasattr(self.data, 'f'): return
    y, w, h = self.separator_size, self.subset_h, self.subset_h
    w_10th = w // 10
    max_count = max(self.counts)
    for i in range(len(self.data.f)):
      x = self.table_x
      count = self.counts[i]
      self.draw_box([x,y,w,h], f'{count}', no_line=True)
      f_list = sorted(list(self.data.f[i]))
      if count != 0 and count == max_count:
        mw = self.subset_h * (len(f_list) + 1)
        self.draw_box([x,y,mw,h], None, **self.bctx_max_count)
      for e in f_list:
        ctx = self.get_fi_ctx(i, e)
        x += self.subset_h
        self.draw_box(rect_inflate([x,y,w,h], -w_10th), f'{e}', border_radius=w//3, **ctx)
      y += self.subset_h

class CitySetCoverVisualizer(PlanarVisualizer):
  grayed_city_context = PrimVisualizer.grayed_city_context
  def_edge_context = KruskalVisualizer.grayed_edge_context
  fixed_edge_context = {
    'edge_line_color': Color.Teal,
    'edge_value_color': Color.DarkGreen,
  }
  neighbor_city_context = {
    'city_body_color': Color.LightBlue,
    'city_line_color': Color.DeepSkyBlue,
    'city_name_color': Color.Gray,
    'shows_city_index': True,
    # 'shows_city_coord': True,
  }

  def_city_context = grayed_city_context
  normal_city_context = KruskalVisualizer.normal_city_context
  def setup(self, data):
    super().setup(data)
    self.current_idx = -1
    self.fixing_index = -1

  def fix(self, fidx):
    self.comp_el = None
    self.current_idx = -1
    self.fixing_index = fidx
    self.set_city_context(fidx, self.normal_city_context)
    for v in self.data.graph[fidx]:
      self.set_edge_context(fidx, v, self.fixed_edge_context)
      if not v in self.city_contexts:
        self.set_city_context(v, self.neighbor_city_context)
    self.draw()
    self.wait(1000)
    # self.f_idxs.pop(fidx)
    self.fixing_index = -1
    # self.counts = [ 0 for _ in range(len(self.data.f))]
    self.draw()
    # self.wait(1000)

  def calc_coords(self):
    self.legend_right = self.config.screen_width // 3
    self.legend_bottom = self.config.screen_height // 3
    self.table_x = self.config.screen_width - self.legend_right #- self.separator_size

    super().calc_coords()

    if not hasattr(self.data, 'f'): return
    subsets_h = self.config.screen_height - 2 * self.separator_size
    self.subset_h = subsets_h // (len(self.data.f) + 2)
    if self.subset_h < self.config.font_size:
      self.subset_h = self.config.font_size

    self.count_elements()

  def count_elements(self):
    self.counts = dict()
    len_f = len(self.data.f)
    for fi in range(len_f):
      if self.data.F[fi]:
        self.counts[fi] = len(self.data.U & self.data.f[fi])
      else:
        self.counts[fi] = 0

  def draw_content(self):
    super().draw_content()
    self.draw_f_elements()

  def get_el_ctx(self, el, compares=True):
    if not el in self.data.U:
      return SetCoverVisualizer.bctx_removed
    if compares and el == self.comp_el:
      return SetCoverVisualizer.bctx_comp
    return SetCoverVisualizer.bctx_normal

  def get_fi_ctx(self, fi, el):
    # print(f'{fi=} {self.fixing_index=} {self.f_idxs=}')
    if fi == self.current_idx and el == self.comp_el:
      return SetCoverVisualizer.bctx_comp
    if fi == self.fixing_index:
      if el in self.data.U:
        return SetCoverVisualizer.bctx_fixing
      else:
        return SetCoverVisualizer.bctx_fixing_without_body
    if self.data.F[fi]:
      return self.get_el_ctx(el, False)
    else:
      return SetCoverVisualizer.bctx_fixed

  def draw_f_elements(self):
    if not hasattr(self.data, 'f'): return

    y, w, h = self.separator_size, self.subset_h, self.subset_h
    w_10th = w // 10
    max_count = max(self.counts)
    for i in range(len(self.data.f)):
      x = self.table_x
      count = self.counts[i]
      self.draw_box([x,y,w,h], f'{count}', no_line=True)
      f_list = sorted(list(self.data.f[i]))
      if count != 0 and count == max_count:
        mw = self.subset_h * (len(f_list) + 1)
        self.draw_box([x,y,mw,h], None, **self.bctx_max_count)
      for e in f_list:
        ctx = self.get_fi_ctx(i, e)
        x += self.subset_h
        text = self.get_element_text(e)
        self.draw_box(rect_inflate([x,y,w,h], -w_10th), text, border_radius=w//3, **ctx)
      y += self.subset_h

  def get_element_text(self, e):
    return f'{e}'

class MstTspVisualizer(PrimVisualizer):
  PHASE_MST, PHASE_TSP, PHASE_SHORTCUT = range(3)
  cctx_start = {
    'city_body_color': Color.Crimson,
    'city_line_color': Color.line,
    'city_name_color': Color.text,
    'shows_city_index': True,
    # 'shows_city_coord': True,
  }
  cctx_update = {
    'city_body_color': Color.Black,
    'city_line_color': Color.line,
    'city_name_color': Color.text,
    'shows_city_index': True,
    # 'shows_city_coord': True,
  }
  ectx_mst = {
    'edge_line_color': Color.Lavender,
    'edge_line_width': 16,
    'edge_value_color': Color.Gray,
    'shows_edge_value': True,
  }
  ectx_tsp = {
    'edge_line_color': Color.Crimson,
    'edge_value_color': Color.DarkBlue,
    'shows_edge_value': True,
  }
  bctx_mst = {
    'line_color': Color.line,
    'text_color': Color.Crimson,
    'no_body': True,
    # 'width': 2,
  }
  bctx_current = {
    'line_color': Color.Silver,
    'body_color': Color.LemonChiffon,
    'text_color': Color.text,
    # 'width': 2,
  }
  bctx_seq_normal = {
    'line_color': Color.line,
    'text_color': Color.Crimson,
    'no_body': True,
    # 'width': 2,
  }
  bctx_seq_current = {
    'line_color': Color.DarkBlue,
    'body_color': Color.LightBlue,
    'text_color': Color.text,
  }
  bctx_seq_dup = {
    'line_color': Color.DarkBlue,
    'body_color': Color.LemonChiffon,
    'text_color': Color.Gray,
  }
  def setup(self, data):
    super().setup(data)
    self.phase = self.PHASE_MST
    self.start_index = -1
    self.current_index = -1

  def calc_coords(self):
    if self.phase == self.PHASE_MST:
      return super().calc_coords()

    self.bsize = self.separator_size * 2 // 3
    self.bdiff = self.bsize * 4 // 3

    self.legend_right = self.config.screen_width // 5
    self.legend_bottom = self.config.screen_height // 5

    PlanarVisualizer.calc_coords(self)

  def set_start(self, index):
    self.start_index = index

  def start_shortcut(self):
    self.phase = self.PHASE_SHORTCUT

  def get_city_context(self, index):
    if index == self.data.start_index:
      return self.cctx_start
    return super().get_city_context(index)

  def draw_right_pane(self):
    if self.phase == self.PHASE_MST:
      return super().draw_right_pane()
    if self.phase == self.PHASE_TSP:
      self.draw_adjacents()
    self.draw_sequences()

  def draw_adjacents(self):
    if not hasattr(self.data, 'mg'): return
    nc = len(self.data.cities)
    bx = self.config.screen_width - self.legend_right + self.separator_size
    bw = self.legend_right - self.separator_size * 3 // 2
    # print(f'{bx=} {self.config.screen_width=} {self.legend_right=}') #+ self.separator_size
    y = self.roots_y
    h = self.bsize
    # df = h // 8
    ctx = self.bctx_mst
    for i in range(nc):
      if not self.data.mg[i].keys(): continue
      if i == self.current_index:
        rect = rect_inflate([bx, y, bw, h], 4)
        self.draw_box(rect, **self.bctx_current)
      x = bx
      tx, ty = x + h // 2, y + h // 2
      self.draw_text(f'{i}', [tx,ty])
      for v in self.data.mg[i].keys():
        x += self.bdiff
        self.draw_box([x,y,h,h], f'{v}', border_radius=h//3, **ctx)
      y += self.bdiff

  def draw_sequences(self):
    if not hasattr(self.data, 'seq'): return

    bx = x = self.separator_size
    y = self.config.screen_height - self.legend_bottom + self.separator_size
    w = self.bsize #self.separator_size * 2 // 3
    dx = self.bdiff #w * 4 // 3
    maxx = self.config.screen_width - self.legend_right

    for i in range(len(self.data.seq)):
      n = self.data.seq[i]
      if n == self.current_index:
        ctx = self.bctx_seq_current
      elif self.data.seq[:i].count(n) > 0:
        ctx = self.bctx_seq_dup
      else:
        ctx = self.bctx_seq_normal
      self.draw_box([x,y,w,w], f'{n}', **ctx)
      x += dx
      if x >= maxx:
        x, y = bx, y + self.bdiff


  def finish_mst(self):
    self.phase = self.PHASE_TSP
    for u,v,w in self.data.mst_edges:
      self.set_edge_context(u, v, self.ectx_mst)

  def draw_all_edges(self):
    super().draw_all_edges()
    if self.phase == self.PHASE_MST:
      return
    if not hasattr(self.data, 'seq'): return
    prev = None
    for c in self.data.seq:
      if prev != None:
        self.draw_directed_edge(prev, c, **self.ectx_tsp)
      prev = c

  def add_seq(self, c1, c2):
    prev = self.city_contexts[c2] if c2 in self.city_contexts else None
    self.current_index = c2
    self.set_city_context(c2, self.cctx_update)
    self.draw()
    self.wait(1000)
    self.set_city_context(c2, prev)

  def update_shortcut(self, c):
    prev = self.city_contexts[c] if c in self.city_contexts else None
    self.current_index = c
    self.set_city_context(c, self.cctx_update)
    self.draw()
    self.wait(500)
    self.set_city_context(c, prev)

class VertexCoverVisualizer(CitySetCoverVisualizer):
  ectx_grayed = {
    'edge_line_color': Color.WhiteSmoke,
    'edge_value_color': Color.WhiteSmoke,
    'shows_edge_value': True,
  }
  ectx_matching = {
    'edge_line_color': Color.Maroon,
    'edge_line_width': 4,
    'shows_edge_value': False,
  }
  ectx_covered = {
    'edge_line_color': Color.Crimson,
    'edge_value_color': Color.DarkBlue,
    'shows_edge_value': True,
  }

  def setup(self, data):
    super().setup(data)

  def get_element_text(self, e):
    u,v,w = self.data.edges[e]
    return f'{u}/{v}'

  def calc_coords(self):
    if self.data.usingSetCover:
      super().calc_coords()
      return

    PlanarVisualizer.calc_coords(self)

  def matching(self, u, v):
    self.set_edge_context(u, v, self.ectx_matching)
    self.fix_matching(u, v)
    self.fix_matching(v, u)

  def fix_matching(self, fidx, other):
    self.comp_el = None
    self.current_idx = -1
    self.fixing_index = fidx
    self.set_city_context(fidx, self.normal_city_context)
    for v in self.data.graph[fidx]:
      if v != other:
        self.set_edge_context(fidx, v, self.fixed_edge_context)
      if not v in self.city_contexts:
        self.set_city_context(v, self.neighbor_city_context)
    self.draw()
    self.wait(1000)
    # self.f_idxs.pop(fidx)
    self.fixing_index = -1
    # self.counts = [ 0 for _ in range(len(self.data.f))]
    self.draw()
    # self.wait(1000)

  # def draw_content(self):
  #   if self.data.usingSetCover:
  #     super().draw_content()
  #     return

    

  # def draw_u_elements(self):
  #   n_cities = len(self.data.cities)
  #   n_edges = len(self.data.edges)
  #   for i in range(n_edges):
  #     u,v,w = self.data.edges[i]
  #     if u in self.data.U or v in self.data.U:
  #       ctx = self.ectx_grayed
  #     else:
  #       ctx = self.ectx_covered
  #     self.draw_edge(u,v,w,**ctx)

class ClusterVisualizer(PlanarVisualizer):
  CityColors = Color.set1 + Color.set2
  LineColors = Color.pastel1 + Color.pastel2
  def setup(self, data, uses_welzl=False):
    super().setup(data)
    self.uses_welzl = uses_welzl
  def compare(self, city, center, dist):
    self.draw()
    if dist > 0:
      self.draw_line_to_center(city, center, int(dist), 2)
    self.update_display()
    self.wait(100)
  def draw_content(self):
    if self.uses_welzl:
      self.draw_cluster_circles()
    self.draw_lines_to_center()
    self.draw_all_cities()
    self.draw_next_center()
  def draw_cluster_circles(self):
    subs = [ [] for center in self.data.centers ]
    for i in range(len(self.data.cities)):
      if not i in self.data.dists: continue
      dist, center = self.data.dists[i]
      ci = self.data.centers.index(center)
      subs[ci].append(self.data.cities[i])
    for ci in range(len(self.data.centers)):
      x, y, r = welzl(subs[ci])
      sx, sy = self.o2s(x, y)
      dx, _ = self.o2s(x+r, y)
      radius = dx - sx
      color = self.LineColors[ci % len(self.LineColors)]
      pg.draw.circle(self.screen, color, [sx, sy], radius, 1)
      pg.draw.circle(self.screen, color, [sx, sy], self.separator_size // 2, 1)
      self.draw_text(f'{round(r)}', [sx, sy])

  def draw_next_center(self):
    if not self.data.dists: return
    city, (dist, center) = self.data.dists.peekitem()
    xy = self.city2s(self.data.cities[city])
    radius = self.config.font_size
    pg.draw.circle(self.screen, Color.line, xy, radius, 1)

  def get_city_context(self, index):
    # if index in self.data.centers:
    #   ci = self.data.centers.index(index)
    #   return {
    #     'city_name_color': Color.DarkBlue,
    #     'city_body_color': self.CityColors[ci % len(self.CityColors)]
    #   }
    if not index in self.data.dists: return {}
    dist, center = self.data.dists[index]
    ci = self.data.centers.index(center)
    color = self.CityColors[ci % len(self.CityColors)]
    return {
      'city_name_color': color_darker(color),
      'city_body_color': color,
    }

  def draw_lines_to_center(self):
    n_cities = len(self.data.cities)
    for i in range(n_cities):
      if i in self.data.centers: continue
      if not i in self.data.dists: continue
      dist, center = self.data.dists[i]
      self.draw_line_to_center(i, center, int(-dist))

  def draw_line_to_center(self, city, center, dist, diff=1):
    ci = self.data.centers.index(center)
    color = self.LineColors[ci % len(self.LineColors)]
    self.draw_edge(city, center, edge_line_color=color)

    x, y = self.city2s(self.data.cities[city])
    y += diff * (self.config.font_size // 2 + self.city_radius)
    self.draw_text(f'{int(dist)}', [x, y], text_color=color)
