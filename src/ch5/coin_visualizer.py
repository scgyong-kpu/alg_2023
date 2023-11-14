from visualizer import *
import math

INF = float('inf')

class CoinChangeVisualizer(Visualizer):
  def __init__(self, title):
    super().__init__(title)
    self.data = None
    self.animates = False
    self.ctx.money, self.ctx.coin = -1, -1

  def setup(self, data):
    self.data = data

  def money(self, money):
    self.ctx.money = money
    self.draw()
    # self.wait(1000)
  def coin(self, coin):
    self.ctx.coin = coin
    self.draw()
    self.wait(1000)
  def copy_from(self, m):
    rect_beg = self.cell_rect(m)
    rect_end = self.cell_rect(self.ctx.money)
    dx, dy = rect_end[0] - rect_beg[0], rect_end[1] - rect_beg[1]
    duration = 1000 // self.speed
    frames = duration // WAIT_ONE_FRAME_MILLIS
    if frames < 2: frames = 2
    wait = duration // frames
    if wait < WAIT_ONE_FRAME_MILLIS: wait = WAIT_ONE_FRAME_MILLIS
    for i in range(1, frames+1):
      self.draw(False)
      ox, oy = dx * i // frames, dy * i // frames
      self.draw_cell(m, (ox,oy), add=(i/frames, self.ctx.coin))
      self.update_display()
      self.wait(wait)

  def draw(self, updates=True):
    self.clear()
    self.calc_coords()
    self.draw_legends()
    self.draw_comparison()
    self.draw_table()
    # self.draw_items()
    if updates:
      self.update_display()

  def calc_coords(self): 
    sw, sh = self.config.screen_width, self.config.screen_height

    self.header_height = sh // 8
    n_coin = len(self.data.coins)
    money = self.data.money

    self.table_x = self.separator_size
    self.table_y = 3 * self.separator_size + self.header_height
    self.table_w = (sw - 2 * self.separator_size)
    self.table_h = (sh - self.separator_size - self.table_y)

    self.cell_w = self.table_w // (money + 1)
    self.cell_1_h = min(self.cell_w, self.header_height)
    self.cell_2_h = self.table_h - self.cell_1_h

  def draw_legends(self): 
    n_coin = len(self.data.coins)
    x, y = self.table_x, self.separator_size
    s = self.header_height
    self.draw_box([x, y, n_coin * s, s], Color.gray[0], Color.line)
    rect = [x,y,s,s]
    rect = rect_inflate(rect, -s//5)
    for i in range(n_coin):
      self.draw_coin(rect, i, self.ctx.coin == i)
      rect[0] += s

  def draw_coin(self, rect, i, enabled):
    if enabled:
      body = Color.pastel2[i%len(Color.pastel2)]
      line = Color.set2[i%len(Color.set2)]
      tc = Color.text
    else:
      body = Color.gray[1]
      line = Color.gray[2]
      tc = Color.gray[3]
    radius = rect[2]//2
    self.draw_box(rect, body, line, radius=radius)
    xy = rect_center(rect)
    value = self.data.coins[i]
    value = '' if value == INF else str(value)
    self.draw_text(value, xy, tc)

  def draw_comparison(self):
    coin = self.data.coins[self.ctx.coin]
    j = self.ctx.money
    copies = coin <= j and self.data.C[j-coin] + 1 < self.data.C[j]
    expr = '%d <= %d' % (coin, j)
    if coin <= j:
      expr += ' and C[%d-%d]+1 < C[%d]' % (j, coin, j)
    x = len(self.data.coins) * self.header_height + 2 * self.separator_size
    y = self.separator_size
    w = self.config.screen_width - x - self.separator_size
    h = self.header_height
    body = Color.pastel1[0] if copies else Color.back
    line = Color.set1[0] if copies else None
    self.draw_box([x,y,w,h], body, line)
    tx = x + self.separator_size
    ty = y + h // 2 - self.config.font_size
    self.draw_text(expr, [tx,ty], Color.dark[0], horz_center=False, font=self.big_font)

  def draw_table(self): 
    for m in range(self.data.money + 1):
      self.draw_table_header(m)
      self.draw_cell(m)

  def draw_table_header(self, m):
    x, y, w, _ = self.cell_rect(m)
    sep = self.separator_size
    rect = [x, y-sep, w, sep]
    # if self.ctx.money == m:
    #   self.draw_box(rect, None, Color.set1[0])
    xy = rect_center(rect)
    self.draw_text(str(m), xy, Color.dark[0])

  def draw_cell(self, m, oxy=None, add=None):
    body, line = Color.back, Color.line
    if m == self.ctx.money:
      body = Color.pastel1[0]
    elif m + self.data.coins[self.ctx.coin] == self.ctx.money:
      body = Color.pastel1[1]
    rect = self.cell_rect(m)
    if oxy != None:
      rect[0] += oxy[0]
      rect[1] += oxy[1]
    self.draw_box(rect, body_color=body, line_color=line)

    text_rect = rect_inflate(self.upper_rect(rect, 0), -2)
    value = self.data.C[m]
    value = '∞' if value == INF else str(value)
    self.draw_text(value, rect_center(text_rect), Color.text)

    coin_rect = self.coin_rect(rect, 0)
    for i, coin in self.data.P[m]:
      self.draw_coin(rect_inflate(coin_rect, -2), i, True)
      coin_rect[1] += coin_rect[3]

    if add != None:
      coin_rect = rect_inflate(coin_rect, -2)
      self.clip(coin_rect)
      coin_rect[0] -= (1.0 - add[0]) * rect[2]
      self.draw_coin(coin_rect, add[1], True)
      self.clip(None)

    # if i > 0:
    #   self.draw_knapsack_content(rect, self.data.P[i][c])

  # def draw_knapsack_content(self, rect, items):
  #   for i in range(len(items)):
  #     r = self.content_rect(rect, i)
  #     item = items[i]
  #     cr = r[2] // 4
  #     if cr < 1: cr = 1
  #     self.draw_box(r, Color.pastel2[item%len(Color.pastel2)], Color.set2[item%len(Color.set2)], radius=cr)
  #     self.draw_text(str(self.data.W[item]), rect_center(r))

  def cell_rect(self, m):
    x = self.table_x + self.cell_w * m
    y = self.table_y
    return [x, y, self.cell_w, self.table_h]
  def upper_rect(self, rect, row=0):
    x, y, w, h = rect
    c1h = self.cell_1_h
    return [x, y, w, c1h]
  def coin_rect(self, rect, row):
    x, y, w, h = rect
    c1h = self.cell_1_h
    return [ x, y + c1h * (row + 1), c1h, c1h ]

  def on_mouse_motion(self):
    if self.data == None: return
    x, y = pg.mouse.get_pos()

    return

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
  vis = CoinChangeVisualizer('Coin Change Visualizer')
  # vis.draw()
  vis.end()
