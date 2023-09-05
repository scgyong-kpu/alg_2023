from vis.base import *

class BinsVisualizer(Visualizer):
  fit_texts = [
    'First Fit', 'Next Fit', 'Best Fit', 'Worst Fit',
  ]
  bctx_normal = {}
  bctx_curr = {
    'line_color': Color.Indigo,
    # 'body_color': Color.SkyBlue,
    'width': 5,
  }
  def setup(self, data):
    self.data = data
    self.last_bin = None
    self.anims = False
    self.anim_box = None
  def add(self, bin):
    self.last_bin = bin
    if bin != None:
      self.anims = True
      self.animate(900)
      self.anims = False
      self.wait(100)
    else:
      self.draw(1000)
  def draw(self, wait_msec=0):
    self.clear()
    self.calc_coords()
    self.draw_content()
    self.update_display()
    if wait_msec > 0:
      self.wait(wait_msec)
  def calc_coords(self):
    self.table_x, self.table_y = self.separator_size, 3 * self.separator_size // 2
    self.bin_h = (self.config.screen_height - self.table_y - 2 * self.separator_size) // 2
    self.bin_dx = self.separator_size * 2 // 3
    self.bin_w = self.bin_dx * 3 // 4
    self.bin_dy = self.bin_h + self.separator_size
    self.max_x = self.config.screen_width - self.separator_size - self.bin_w
  def get_rect(self, i):
    bx, y, w, h = self.table_x, self.table_y, self.bin_w, self.bin_h
    x = bx
    for _ in range(i):
      x += self.bin_dx
      if x >= self.max_x:
        x, y = bx, y + self.bin_dy
    return [x, y, w, h]

  def draw_content(self):
    tx, ty = self.separator_size, self.separator_size // 3
    self.draw_text(self.fit_texts[self.data.strategy], [tx,ty], center=False)
    # bx, y, w, h = self.table_x, self.table_y, self.bin_w, self.bin_h
    # x = bx
    binSize = 100
    l_bins = len(self.data.bins)
    self.anim_box = None
    for i in range(l_bins):
      bin = self.data.bins[i]
      binSize = bin.Size
      x, y, w, h = self.get_rect(i)
      self.draw_bin(i+1, bin, x, y, w, h)

    n = l_bins + 3
    for i in range(len(self.data.objs)):
      s = self.data.objs[i] 
      x, y, w, h = self.get_rect(n)
      if self.anims:
        x += (1-self.anim_progress) * self.bin_dx
      oh = s * self.bin_h // binSize
      color = Color.pastel1[s % len(Color.pastel1)]
      self.draw_box([x-2, y, w-4, oh], f'{s}', body_color=color)
      n += 1

    if self.anim_box != None:
      rect, text, color = self.anim_box
      self.anim_box = None
      self.draw_box(rect, text, body_color=color)

  def draw_bin(self, idx, bin, x, y, w, h):
    tx = x + w // 2
    ty = y - self.config.font_size // 2
    self.draw_text(f'{idx}', [tx, ty], text_color=Color.Blue)
    ctx = self.bctx_curr if bin == self.last_bin else self.bctx_normal
    # print(f'{ctx} {bin == self.last_bin}')
    self.draw_box([x,y,w,h], **ctx)
    x += 2
    w -= 4
    top = y
    btm = y + h
    l_bins = len(bin.objs)
    for i in range(l_bins):
      s = bin.objs[i]
      oh = s * self.bin_h // bin.Size
      y = btm - oh
      btm = y
      oh -= 1
      color = Color.pastel1[s % len(Color.pastel1)]
      anims = bin == self.last_bin and i == l_bins - 1 and self.anims
      if anims:
        n = len(self.data.bins) + 3
        ax,ay,aw,ah = self.get_rect(n)
        dx, dy = x - ax, y - ay
        ax += dx * self.anim_progress
        ay += dy * self.anim_progress
        self.anim_box = ([ax,ay,w,oh], f'{s}', color)
        # self.draw_box([ax,ay,w,oh], f'{s}', body_color=color)
      else:
        self.draw_box([x,y,w,oh], f'{s}', body_color=color)
    oh = bin.free * self.bin_h // bin.Size
    ty = top + oh // 2
    self.draw_text(f'{bin.free}', [tx, ty], text_color=Color.LightGray)



