from vis.planar import *
from copy import deepcopy

class ClosestPairVisualizer(PlanarVisualizer):
  cctx_compare = {
    'city_body_color': Color.FireBrick,
    'city_line_color': Color.DarkRed,
    'city_name_color': Color.DarkGreen,
  }
  cctx_strip = {
    'city_body_color': Color.Yellow,
    'city_line_color': Color.MediumVioletRed,
    'city_name_color': Color.Purple,
  }
  ectx_comp1 = {
    'edge_line_color': Color.PaleGreen,
    'edge_value_color': Color.DarkOliveGreen,
    'edge_line_width': 5,
    'shows_edge_value': True,
  }
  ectx_comp2 = {
    'edge_line_color': Color.LightSkyBlue,
    'edge_value_color': Color.PowderBlue,
    'shows_edge_value': True,
  }
  ectx_closest = {
    'edge_line_color': Color.Indigo,
    'edge_value_color': Color.text,
    'edge_line_width': 2,
    'shows_edge_value': True,
  }
  def setup(self, data):
    super().setup(data)
    self.comp_a1 = [-1, -1, 0]
    self.closest = [-1, -1, float('inf')]
    self.compare_count = 0
    self.stack = []
    self.pushing = 0
    self.closests = dict()
    self.strip = []
    self.cx1, self.cx2 = -1, -1
    self.phase_str = ''
  def push(self, s=-1, e=-1, m=-1):
    self.stack.append([self.closest, [s,e,m]])
    self.phase_str = f'push:{len(self.stack)}'
    self.closest = [-1, -1, float('inf')]
    self.pushing = 1
    self.animate(1000)
    self.pushing = False
  def pop(self):
    self.phase_str = f'pop:{len(self.stack)}'
    self.pushing = -1
    self.animate(1000)
    self.pushing = False
    self.closest = self.stack.pop()[0]
  def compare(self, i1, i2, dist):
    # print(f'compare: {i1=} {i2=}')
    self.compare_count += 1
    self.comp_a1 = [i1, i2, dist]
    if dist < self.closest[2]:
      self.comp_a1, self.closest = self.closest, self.comp_a1
    self.set_comp_context(self.comp_a1, self.cctx_compare)
    self.set_comp_context(self.closest, self.cctx_compare)
    self.draw()
    self.wait(1000)
    self.set_comp_context(self.comp_a1, None)
    self.set_comp_context(self.closest, None)
    self.comp_a1 = [-1, -1, 0]
  def set_comp_context(self, a, context):
    if a[0] >= 0: 
      if context == None and self.in_strip(a[0]):
        context = self.cctx_strip
      self.set_city_context(a[0], context)
    if a[1] >= 0: 
      if context == None and self.in_strip(a[1]):
        context = self.cctx_strip
      self.set_city_context(a[1], context)
  def in_strip(self, idx):
    for c in self.strip:
      if c.index == idx: return True
    return False
  def set_phase(self, phase=''):
    self.phase_str = phase
  def set_strip(self, strip=[], cx1=-1, cx2=-1):
    if strip:
      for c in strip:
        self.set_city_context(c.index, self.cctx_strip)
    elif self.strip:
      for c in self.strip:
        self.set_city_context(c.index, None)
    self.strip = strip
    if strip:
      self.phase_str = 'Comparing cities in strip'
    self.cx1, _ = self.o2s(cx1, 0)
    self.cx2, _ = self.o2s(cx2, 0)
  def set_closest(self, left, right=-1, s=-1, e=-1, d=-1):
    if right < 0:
      if left in self.closests: 
        # print(f'removing {left}= {self.closests[left]}')
        del self.closests[left]
      return
    self.closests[left] = [right, s, e, d]
    # print(f'adding {left}: {[right, s, e, d]}')
    for i in range(left+1, right+1):
      if i in self.closests:
        # print(f'removing {i}: {self.closests[i]}')
        del self.closests[i]
    s,e,d = self.closest
    if s in range(left, right+1) and e in range(left, right+1):
      self.closest = [-1, -1, float('inf')]
  # def finish(self, s,e,d):
  #   self.closests = dict()
  #   self.closests[0] = [0, s, e, d]
  def draw_content(self):
    self.draw_stack()
    self.draw_strip()
    self.draw_closests()
    self.draw_compare_edges()
    self.draw_all_cities()
    self.draw_closest_info()
  def draw_stack(self):
    n_stack = len(self.stack)
    base = Color.White
    for i in range(n_stack):
      a, (s,e,m) = self.stack[i]
      if s < 0: return
      r1 = rect_inflate(self.get_division_rect(s, m), 2 * self.city_radius)
      r2 = rect_inflate(self.get_division_rect(m+1,e), 2 * self.city_radius)
      r1, r2 = self.adj_divisions(r1, r2)
      if i > 0:
        base = color_2 if s > prev_m else color_1
      color_1 = self.draw_division_box(r1, i, Color.BrownGroup, base)
      color_2 = self.draw_division_box(r2, i, Color.GrayGroup, base)
      prev_m = m
  def draw_division_box(self, rect, level, color_group, base_color):
    color = color_group[level]
    line_color = Color.line
    if self.pushing != 0 and level == len(self.stack) - 1:
      r1,g1,b1 = base_color
      r2,g2,b2 = color_group[level]
      prog = self.anim_progress if self.pushing > 0 else 1 - self.anim_progress
      color = r1 + (r2-r1)*prog, g1 + (g2-g1) * prog, b1 + (b2-b1) * prog

      r2,g2,b2 = line_color
      prog = self.anim_progress if self.pushing > 0 else 1 - self.anim_progress
      line_color = r1 + (r2-r1)*prog, g1 + (g2-g1) * prog, b1 + (b2-b1) * prog
    self.draw_box(rect, body_color=color, line_color=line_color)
    return color
  def get_division_rect(self, start, end):
    x1, y1 = self.city2s(self.data.cities[start])
    x2, y2 = x1, y1
    for i in range(start+1, end+1):
      x, y = self.city2s(self.data.cities[i])
      x1 = min(x1, x)
      y1 = min(y1, y)
      x2 = max(x2, x)
      y2 = max(y2, y)
    rect = [x1,y1,x2-x1,y2-y1]
    return rect
  def draw_strip(self):
    n_strip = len(self.strip)
    if n_strip == 0: return
    x1, x2 = self.cx1, self.cx2
    _, y1 = self.city2s(self.strip[0])
    y2 = y1
    for i in range(1, n_strip):
      x, y = self.city2s(self.strip[i])
      # x1 = min(x1, x)
      y1 = min(y1, y)
      # x2 = max(x2, x)
      y2 = max(y2, y)
    rect = rect_inflate([x1,y1,x2-x1,y2-y1], 2 * self.city_radius)
    pg.draw.rect(self.screen, Color.line, rect, 5)
  def adj_divisions(self, rect1, rect2):
    x1,y1,w1,h1 = rect1
    x2,y2,w2,h2 = rect2
    r1,b1 = x1+w1,y1+h1
    r2,b2 = x2+w2,y2+h2
    t = min(y1,y2)
    b = max(b1,b2)
    m2 = (r1+x2+self.city_radius) // 2
    m1 = m2 - self.city_radius
    return [x1,t,m1-x1,b-t], [m2,t,r2-m2,b-t]
  def draw_closests(self):
    for start in self.closests:
      end,s,e,d = self.closests[start]
      self.draw_edge(s,e,f'{d:.1f}', **self.ectx_closest)
  def draw_compare_edges(self):
    self.draw_compare_edge(*self.closest, self.ectx_comp1)
    self.draw_compare_edge(*self.comp_a1, self.ectx_comp2)
  def draw_compare_edge(self, i1, i2, dist, ectx):
    if i1 < 0: return
    self.draw_edge(i1, i2, f'{dist:.1f}', **ectx)
  def draw_closest_info(self):
    i1, i2, dist = self.closest
    if i1 < 0:
      if self.closests:
        left = (list(self.closests.keys()))[0]
        right, i1, i2, dist = self.closests[left]

    if i1 >= 0:
      c1, c2 = self.data.cities[i1], self.data.cities[i2]
      text = f'{len(self.data.cities)} cities, {self.compare_count} comparisons'
      text += f' [{c1.name} ~ {c2.name}] {dist:.1f}'
    else:
      text = ''
    text += '\n'+self.phase_str
    xy = 1,1 #self.separator_size, self.separator_size
    self.draw_text(text, xy, center=False)


