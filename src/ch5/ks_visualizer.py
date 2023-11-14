from visualizer import *
import math

class KnapsackVisualizer(Visualizer):
  def __init__(self, title):
    super().__init__(title)
    self.data = None
    self.ctx.i, self.ctx.c = -1, -1
    self.ctx.marks_i = False
    self.ctx.compares = False
    self.animation = None

  def setup(self, ks):
    self.data = ks

  def prepare(self, i=-1, c=-1, short=False):
    self.ctx.i, self.ctx.c = i, c
    self.ctx.marks_i = not short
    self.draw()
    # print('prepare')
    msec = 100 if short else 1000
    self.wait(msec)
  def compare(self):
    self.ctx.marks_i = False
    self.ctx.compares = True
    self.draw()
    # print('compare')
    self.wait(1000)
  def copy_from(self, fi, fc, append=-1):
    self.ctx.marks_i = False
    self.ctx.compares = False
    rect_beg = self.cell_rect(fi, fc)
    rect_end = self.cell_rect(self.ctx.i, self.ctx.c)
    dx, dy = rect_end[0] - rect_beg[0], rect_end[1] - rect_beg[1]
    duration = 1000 // self.speed
    frames = duration // WAIT_ONE_FRAME_MILLIS
    if frames < 2: frames = 2
    wait = duration // frames
    if wait < WAIT_ONE_FRAME_MILLIS: wait = WAIT_ONE_FRAME_MILLIS
    for i in range(1, frames+1):
      self.draw(False)
      ox, oy = dx * i // frames, dy * i // frames
      if append >= 0:
        self.animation = (i/frames, append)
      self.draw_cell(fi, fc, (ox,oy))
      self.animation = None
      self.update_display()
      self.wait(wait)
  # def append(self):
  #   self.ctx.compares = False
  #   self.draw()
  #   print('append')
  #   self.wait(1000)
  def draw(self, updates=True):
    self.clear()
    self.calc_coords()
    self.draw_legends()
    self.draw_table()
    self.draw_items()
    if updates:
      self.update_display()

  def calc_coords(self): 
    N = self.data.N
    cap = self.data.capacity
    sw, sh = self.config.screen_width, self.config.screen_height
    self.table_x = sw * 3 // (cap + 4)
    self.table_y = self.separator_size
    self.table_w = (sw - self.table_x - self.separator_size) # // (cap + 1)
    self.table_h = (sh - 2 * self.separator_size) #// (N + 2)

    self.cell_w = self.table_w // (cap + 1)
    self.cell_h = self.table_h // (N + 1)

  def draw_legends(self): 
    xy = rect_center(self.cell_rect(0, -3))
    self.draw_text('weight', xy, Color.set2[0])
    xy = rect_center(self.cell_rect(0, -2))
    self.draw_text('value', xy, Color.set2[1])
    for i in range(1, self.data.N):
      rect = self.cell_rect(i, -1)
      # rect[0] -= rect[2] // 4
      rect = rect_inflate(rect, -4)
      radius = rect[2] // 4
      if i <= self.ctx.i:
        body, line, tc = Color.pastel2[i%len(Color.pastel2)], Color.set2[i%len(Color.set2)], Color.text
      else:
        body, line, tc = Color.gray[0], Color.gray[1], Color.gray[1]
      self.draw_box(rect, body, line, radius=radius)
      xy = rect_center(rect)
      self.draw_text(str(self.data.W[i]), xy, tc, font=self.big_font)

      rect = self.cell_rect(i, -3)
      if self.ctx.marks_i and self.ctx.i == i:
        self.draw_box(rect, None, Color.set1[0])
      xy = rect_center(rect)
      self.draw_text(str(self.data.W[i]), xy, Color.set2[0], font=self.big_font)

      rect = self.cell_rect(i, -2)
      if self.ctx.compares and self.ctx.i == i:
        self.draw_box(rect, Color.pastel1[1])
      xy = rect_center(rect)
      self.draw_text(str(self.data.V[i]), xy, Color.set2[1], font=self.big_font)

  def draw_table(self): 
    N = self.data.N
    cap = self.data.capacity
    for i in range(-1, N):
      for c in range(cap + 1):
        self.draw_cell(i, c)

  def draw_cell(self, i, c, oxy=None):
    if i < 0:
      text = str(c)
      body, line = None, None
      if self.ctx.marks_i and self.ctx.c == c: line = Color.set1[0]
    else:
      # print('draw_cell:', i, c, self.data.N)
      value = self.data.K[i][c]
      text = str(value) if value >= 0 else ''
      body, line = Color.back, Color.line
      # compares: K[i-1][w] > K[i-1][w - W[i]] + V[i]
      if self.ctx.compares:
        if i+1 == self.ctx.i and c == self.ctx.c:
          body = Color.pastel1[0]
        elif i+1 == self.ctx.i and c + self.data.W[self.ctx.i] == self.ctx.c:
          body = Color.pastel1[1]
      if (i, c) == (self.ctx.i, self.ctx.c):
        body = Color.set1[0]
    rect = self.cell_rect(i, c)
    if oxy != None:
      rect[0] += oxy[0]
      rect[1] += oxy[1]
    self.draw_box(rect, body_color=body, line_color=line)
    x,y,w,h = rect
    x += w // 2
    y += h * 4 // 5
    self.draw_text(text, [x, y])

    if i >= 0:
      self.draw_knapsack_content(rect, self.data.P[i][c])

  def draw_knapsack_content(self, rect, items):
    for i in range(len(items)):
      r = self.content_rect(rect, i)
      item = items[i]
      cr = r[2] // 4
      if cr < 1: cr = 1
      self.draw_box(r, Color.pastel2[item%len(Color.pastel2)], Color.set2[item%len(Color.set2)], radius=cr)
      self.draw_text(str(self.data.W[item]), rect_center(r))

    if self.animation != None:
      ratio, item = self.animation
      # print('r/i=', ratio, item)
      r = self.content_rect(rect, len(items))
      cr = r[2] // 4
      if cr < 1: cr = 1
      self.clip(r)
      r[0] -= (1.0 - ratio) * r[2]
      self.draw_box(r, Color.pastel2[item%len(Color.pastel2)], Color.set2[item%len(Color.set2)], radius=cr)
      self.draw_text(str(self.data.W[item]), rect_center(r))
      self.clip(None)

  def content_rect(self, rect, i):
    content_in_a_row = math.ceil(math.sqrt(self.data.N-1))
    x, y, w, h = rect
    xi, yi = i % content_in_a_row, i // content_in_a_row
    sw, sh = w // content_in_a_row, h * 3 // 4 // content_in_a_row
    return rect_inflate([x + sw * xi, y + sh * yi, sw, sh], -2)

  def cell_rect(self, i, c):
    x = self.table_x + self.cell_w * c
    y = self.table_y + self.cell_h * (i + 1)
    return [x, y, self.cell_w, self.cell_h]

  def on_mouse_motion(self):
    if self.data == None: return
    x, y = pg.mouse.get_pos()

    i = (y - self.table_y) // self.cell_h - 1
    c = (x - self.table_x) // self.cell_w
    if (i > 0 and i < self.data.N and 
        c > 0 and c <= self.data.capacity):
      # v = self.data.E[i][j]
      self.ctx.i, self.ctx.c = (i, c)
      if c < self.data.W[i]:
        self.ctx.marks_i = True
        self.ctx.compares = False
      else:
        self.ctx.marks_i = False
        self.ctx.compares = True
    else:
      self.ctx.i, self.ctx.c = -1,-1
    self.draw()

  def draw_items(self): pass

if __name__ == '__main__':
  vis = KnapsackVisualizer('Knapsack Visualizer')
  vis.draw()
  vis.end()
