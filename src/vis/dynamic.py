import math
from vis.base import *
from itertools import permutations
from random import shuffle

class DictObject: 
  def __init__(self, **entries): 
    self.__dict__.update(entries)

class MatrixVisualizer(Visualizer):
  bctx_a = {
    'body_color': Color.pastel1[0],
    'line_color': Color.set1[0],
    'text_color': Color.text,
  }
  bctx_b = {
    'body_color': Color.pastel1[1],
    'line_color': Color.set1[1],
    'text_color': Color.text,
  }
  bctx_c = {
    'body_color': Color.pastel1[2],
    'line_color': Color.set1[2],
    'text_color': Color.text,
  }
  box_ctxs = [ bctx_a, bctx_b, bctx_c ]
  bctx_ha = {
    'body_color': Color.pastel2[0],
    'line_color': Color.set2[0],
    'text_color': Color.text,
  }
  bctx_hb = {
    'body_color': Color.pastel2[0],
    'line_color': Color.set2[1],
    'text_color': Color.text,
  }
  bctx_hc = {
    'body_color': Color.pastel2[2],
    'line_color': Color.set2[2],
    'text_color': Color.text,
  }
  hilight_ctxs = [ bctx_ha, bctx_hb, bctx_hc ]
  operator_color = Color.dark[0]
  operand_color = Color.dark[2]

  def setup(self, data):
    self.data = data

  def start(self, a, b, c):
    self.times = 0
    self.a, self.b, self.c = a, b, c
    self.matrixes = [a, b, c]
    self.idxs = [ 1, a.cols + 3, a.cols + b.cols + 5]
    self.cols = self.a.cols + self.b.cols + self.c.cols + 6
    self.rows = max(self.a.rows, self.b.rows, self.c.rows) + 2

  def update(self, row, col, idx):
    self.current_row = row
    self.current_col = col
    self.current_idx = idx
    self.times += 1
    self.draw(1000)

  def draw(self, wait_msec=0):
    self.clear()
    self.calc_coords()
    self.draw_content()
    self.update_display()
    if wait_msec > 0:
      self.wait(wait_msec)

  def calc_coords(self):
    self.cell_w = self.config.screen_width // self.cols
    self.cell_h = self.config.screen_height // self.rows

  def draw_content(self):
    for i in range(3):
      self.draw_matrix(self.matrixes[i], self.idxs[i], self.box_ctxs[i])
    self.draw_hilights()
    self.draw_others()

  def draw_hilights(self):
    self.draw_cell(0, self.current_row, self.current_idx)
    self.draw_cell(1, self.current_idx, self.current_col)
    self.draw_result_cell()

  def draw_cell(self, idx, row, col, shows_value=True):
    sx = int(self.idxs[idx] * self.cell_w)
    m = self.matrixes[idx]
    sy = (self.rows - m.rows) * self.cell_h // 2
    rect = [ 
      sx + col * self.cell_w, sy + row * self.cell_h,
      self.cell_w, self.cell_h
    ]
    text = str(self.matrixes[idx].data[row][col]) if shows_value else None
    ctx = self.hilight_ctxs[idx]
    self.draw_box(rect, text, **ctx)
    return rect

  def draw_result_cell(self):
    row, idx, col = self.current_row, self.current_idx, self.current_col
    x, y, w, h = self.draw_cell(2, row, col, False)
    x += w // 2
    y += (h - 3 * self.config.font_size) // 2
    mult_value = self.a.data[row][idx] * self.b.data[idx][col]
    sum_value = self.c.data[row][col]
    prev_value = sum_value - mult_value
    line_gap = self.config.font_size * 3 // 4

    self.draw_text(f'{prev_value}', [x, y], text_color=self.operand_color)
    y += line_gap
    self.draw_text('+', [x, y], text_color=self.operator_color)
    y += line_gap
    self.draw_text(f'{mult_value}', [x, y], text_color=self.operand_color)
    y += line_gap
    self.draw_text('=', [x, y], text_color=self.operator_color)
    y += line_gap
    self.draw_text(f'{sum_value}', [x, y])

  def draw_others(self):
    x = int((self.idxs[1] - 1) * self.cell_w)
    y = self.config.screen_height // 2
    self.draw_text('x', [x, y], Color.text, font=self.big_font)
    x = int((self.idxs[2] - 1) * self.cell_w)
    self.draw_text('=', [x, y], Color.text, font=self.big_font)

    xy = [self.cell_w, self.config.screen_height - 2 * self.config.font_size]
    self.draw_text('mult times = %d' % self.times, xy, center=False)

  def draw_matrix(self, m, xi, ctx):
    sx = int(xi * self.cell_w)
    sy = (self.rows - m.rows) * self.cell_h // 2

    mg = self.cell_w // 5
    box = [
      sx - mg, sy - mg, 
      m.cols * self.cell_w + 2 * mg,
      m.rows * self.cell_h + 2 * mg
    ]
    self.draw_box(box, **ctx)

    text = f'{m.rows} x {m.cols}'
    txy = [
      sx + m.cols * self.cell_w // 2, 
      sy - mg - self.config.font_size
    ]
    self.draw_text(text, txy, Color.text, font=self.big_font)

    sx += self.cell_w // 2
    y = sy + self.cell_h // 2
    for row in m.data:
      x = sx
      for v in row:
        self.draw_text(f'{v}', [x, y], Color.text)
        x += self.cell_w
      y += self.cell_h

class ChainedMatrixVisualizer(Visualizer):
  def __init__(self, *args):
    super().__init__(*args)
    self.current_body_vis = -1
    self.select_next_body_visualizer()

  def setup(self, data):
    self.data = data
    self.emp = False

  def select_next_body_visualizer(self):
    bv_classes = [
      TableCmmBody, PyramidCmmBody
    ]
    self.current_body_vis = (self.current_body_vis + 1) % len(bv_classes)
    self.body_vis = bv_classes[self.current_body_vis](self)

  def start(self):
    self.max = max(self.data.sizes)
    self.m_count = len(self.data.sizes) - 1
    self.sub_mult_count = self.i_start = self.i_end = self.i_k = -1

  def start_all_candidates(self):
    self.start()
    self.candidates = []
    self.draw_body = self.draw_candidates

    self.start_index = 0
    orders = list(range(len(self.data.sizes) - 2))
    perms = list(permutations(orders))
    self.perms_count = len(perms)
    for order in perms:
      self.candidates.append(order)
      self.draw(1000)

  def sub(self, sub_mult_count):
    self.sub_mult_count = sub_mult_count

  def range(self, start, end):
    self.i_start, self.i_end = start, end
    self.i_k = -1

  def compare(self, k, will_update=False):
    self.i_k = k
    self.emp = will_update
    self.update()
    self.emp = False

  def update(self):
    self.draw()
    self.wait(1000)

  def finish(self):
    self.sub_mult_count = self.i_start = self.i_end = self.i_k = -1
    self.draw()

  def draw(self, wait_msec=0):
    self.clear()
    self.calc_coords()
    self.draw_content()
    self.update_display()
    if wait_msec > 0:
      self.wait(wait_msec)

  def draw_candidates(self):
    x = self.separator_size
    y = self.table_y

    max_w = 0
    index = self.start_index
    line_gap = self.config.font_size * 3 // 2
    for order in self.candidates:
      index += 1
      text = self.build_order_text(order)
      text = f'{index} / {self.perms_count}. {order} {text}'
      tw, th = self.draw_text(text, [x,y], center=False)
      if max_w < tw: max_w = tw
      y += line_gap
      if y + self.separator_size > self.config.screen_height:
        x += max_w + self.separator_size
        y = self.table_y
        if x + max_w > self.config.screen_width:
          self.start_index += 1
          self.candidates.pop(0)
          break

  def build_order_text(self, order):
    texts = [ f'A{i}' for i in range(1, len(order) + 2) ]
    nums = [ self.data.sizes[i] for i in range(1, len(order) + 2) ]
    sum = 0
    for i in order:
      at = i
      text = texts[at]
      while isinstance(text, int):
        at = text
        text = texts[text]
      text = f'({text} x {texts[i+1]})'
      texts[at] = text
      texts[i+1] = i
      # sum += self.data.sizes[at] * self.data.sizes[i+2]
      # print(f'{sum=}, {self.data.sizes[at]} x {self.data.sizes[i+2]}')
    # print(order, sum, text)
    return text


  def calc_coords(self):
    div = max(5, self.m_count - 1)
    self.header_height = self.config.screen_height // div
    self.header_cell_w = self.config.screen_width // self.m_count
    self.msize = min(self.header_height * 4 // 5, self.header_cell_w)
    self.table_y = self.header_height + self.separator_size + 2 * self.config.font_size
    self.table_h = self.config.screen_height - self.table_y - self.separator_size

  def draw_content(self):
    self.draw_header()
    self.draw_body()

  def draw_header(self):
    for i in range(self.m_count):
      self.draw_mini(i)
      if i > 0:
        self.draw_adj_mult(i)

  def draw_body(self):
    count = self.data.matrix_count
    for start in range(1, count + 1):
      for end in range(start + 1, count + 1):
        self.draw_c(start, end)
      #   print(self.data.C[y][x], end=' ')
      # print()

    if self.i_start >= 0:
      self.draw_update_info(self.i_start, self.i_end, self.i_k)

    self.draw_axis()

  def draw_update_info(self, start, end, k=-1):
    x = self.header_cell_w * (start - 1)
    w = self.header_cell_w * (end - start + 1)
    rect = [x, 2, w, self.header_height - 4]
    self.draw_box(rect, no_body=True)

    if k < 0: return
    mx = self.header_cell_w * k
    my = self.header_height // 2
    self.draw_text('×', [mx, my], Color.text, font=self.big_font)

    font_size = self.config.font_size
    xy = [self.config.screen_width // 2, self.header_height + 3 * font_size]
    sizes, C = self.data.sizes, self.data.C
    total = C[start][k] + C[k+1][end] + sizes[start-1]*sizes[k]*sizes[end]
    text = (
      f'{self.result(start, k)} x {self.result(k+1, end)} = ' +
      f'C[{start}][{k}] + C[{k}+1][{end}] + d[{start}-1] × d[{k}] × d[{end}] = ' +
      f'{self.result(start, k)} + {self.result(k+1, end)} + ' +
      f'{sizes[start-1]} × {sizes[k]} × {sizes[end]} = ' +
      f'{C[start][k]} + {C[k+1][end]} + ' +
      f'{sizes[start-1] * sizes[k] * sizes[end]} = {total}'
    )
    self.draw_text(text, xy, Color.text)
    # print(f'{start=} {k=} {end=}')
    if start == k:
      rect = self.body_vis.get_rect(start, start)
      self.draw_box(rect, body_color=Color.pastel2[1])
    if end == k+1:
      rect = self.body_vis.get_rect(end, end)
      self.draw_box(rect, body_color=Color.pastel2[2])
    if total < C[start][end]:
      rect = self.body_vis.get_rect(start, end)
      rect_inflate(rect, -4)
      self.draw_box(rect, no_body=True)
      # pg.draw.rect(screen, Color.set1[0], [sx+4, sy+4, sw-8,sh-8], 1)

    x = 3 * self.separator_size
    y = self.config.screen_height - 3 * self.separator_size - 2 * font_size
    self.draw_text('L=%d' % (self.sub_mult_count), [x, y], text_color=Color.set2[4], center=False, font=self.big_font)
    y += 2 * font_size
    self.draw_text('s=%d e=%d' % (start, end), [x, y], text_color=Color.dark[4], center=False, font=self.big_font)
    if k >= 0:
      y += 2 * font_size
      self.draw_text('k=%d' % k, [x, y], text_color=Color.set2[4], center=False, font=self.big_font)

  def draw_axis(self):
    sx, sy, sw, sh = self.body_vis.get_rect(1, 2)
    x, y = sx - self.separator_size // 2, sy + sh // 2
    for index in range(1, self.data.matrix_count):
      self.draw_text(str(index), [x, y], text_color=Color.Gray)
      y += sh

    # sx, sy, sw, sh = self.body_vis.get_rect(1, 2)
    # print(f'{sx=}, {sy=}, {sw=}, {sh=}')
    # x, y = sx + sw // 2, sy - self.config.font_size
    row, col = self.body_vis.initial_col()
    for index in range(1, self.data.matrix_count + 1):
      x, y, w, h = self.body_vis.get_rect(row, col)
      b = y + h
      y = b - self.config.font_size
      h = b - y
      xy = rect_center([x, y, w, h])
      self.draw_text(f'{index}', xy, text_color=Color.Gray)
      row, col = self.body_vis.next_col(row, col)

  def result(self, i, j):
    P = self.data.P
    if i == j:
      return 'A' + str(i)
    if P[i][j] == 0:
      return ''
    # print('result():', i, j, P[i][j])
    return '(' + self.result(i, P[i][j]) + '×' + self.result(P[i][j]+1, j) + ')'

  def on_mouse_motion(self):
    x, y = pg.mouse.get_pos()
    start, end = self.body_vis.convert(x, y)
    if (1 <= start and start <= self.m_count and 
        2 <= end and end <= self.m_count):
      self.i_start, self.i_end = start, end
      self.i_k = self.data.P[start][end]
      if self.i_k == 0: self.i_k = -1
    else:
      self.i_start, self.i_end = -1, -1
      self.i_k = -1
    self.draw()

  def draw_c(self, start, end):
    sx, sy, sw, sh  = self.body_vis.get_rect(start, end)
    # temp = self.C[start][k] + self.C[k+1][end] + self.sizes[start-1]*self.sizes[k]*self.sizes[end]
    pair = start, end
    emp = False
    if pair == (self.i_start, self.i_end):
      color = Color.pastel2[0]
      emp = self.emp
    elif pair == (self.i_start, self.i_k):
      color = Color.pastel2[1]
    elif pair == (self.i_k+1, self.i_end):
      color = Color.pastel2[2]
    else:
      color = Color.back

    fs = self.config.font_size
    rect = [sx, sy, sw, sh]
    self.draw_box(rect, body_color=color)
    self.draw_text(str(self.data.C[start][end]), [sx+sw//2, sy+sh//2-fs//2], Color.text)
    self.draw_text(self.result(start, end), [sx+sw//2, sy+sh//2+fs//2], text_color=Color.dark[0])

    if emp:
      mg = self.config.font_size // 2
      rect = rect_inflate(rect, -mg)
      self.draw_box(rect, no_body=True, line_color=Color.Crimson, border_radius=2*mg)

  def draw_mini(self, index):
    y = self.header_height // 2
    w = self.m_count
    x = self.header_cell_w // 2 + index * self.header_cell_w
    row,col = self.data.sizes[index], self.data.sizes[index+1]
    rect = self.mini_rect(x, y, row, col)
    self.draw_box(rect, 
      body_color=Color.pastel1[index], 
      line_color=Color.set1[index])

    y = self.header_height * 4 // 5 + self.config.font_size
    self.draw_text('%dx%d' % (row, col), [x, y], Color.text)
    self.draw_text('A%d' % (index+1), [x, self.config.font_size], Color.text)

  def mini_rect(self, center_x, center_y, row, col):
    rw = col * self.msize // self.max
    rh = row * self.msize // self.max
    return [ center_x - rw // 2, center_y - rh // 2, rw, rh]

  def draw_adj_mult(self, index):
    x = index * self.header_cell_w
    y = self.header_height + self.config.font_size
    row,common,col = self.data.sizes[index-1], self.data.sizes[index], self.data.sizes[index+1]
    text = f'{row}x{common}x{col}={row*common*col}'
    self.draw_text(text, [x, y], text_color=Color.Gray)

  def handle_event(self, e):
    if e.type == pg.KEYDOWN and e.key == pg.K_v:
      self.select_next_body_visualizer()
      self.draw()
    super().handle_event(e)

class TableCmmBody:
  def __init__(self, vis):
    self.vis = vis

  def get_rect(self, start, end):
    vis = self.vis
    sw = (vis.config.screen_width - 2 * vis.separator_size) // (vis.m_count - 1)
    sh = int((vis.config.screen_height - vis.header_height - vis.separator_size - 3 * vis.config.font_size) / (vis.m_count - 0.7))
    sx = vis.separator_size + (end - 2) * sw
    sy = vis.header_height + vis.separator_size + 3 * vis.config.font_size + (start - 1) * sh
    return sx, sy, sw, sh

  def convert(self, x, y):
    vis = self.vis
    cw, ch = vis.config.screen_width, vis.config.screen_height
    sep, fs = vis.separator_size, vis.config.font_size
    sw = (cw - 2 * sep) // (vis.data.matrix_count - 1)
    sh = int((ch - vis.header_height - sep - 3 * fs) / (vis.m_count - 0.7))
    start = (y - vis.header_height - sep - 3 * fs) // sh + 1
    end = (x - sep) // (sw) + 2
    level = -start + end
    # print(f'{start=} {end=} {level=}')
    return start, end

  def next_col(self, row, col):
    return row, col + 1

  def initial_col(self):
    return 0, 1

class PyramidCmmBody(TableCmmBody):
  def get_rect(self, start, end):
    vis = self.vis
    level = end - start - 1
    lvl_cnt = vis.m_count - level - 1
    h = vis.table_h // vis.m_count
    table_w = vis.config.screen_width - 2 * vis.separator_size
    div = lvl_cnt if (level <= 0) else (lvl_cnt + 1)
    if level > 0:
      a = vis.m_count - 1
      div = (lvl_cnt  - 1) * (a - 3) / (a - 1) + 3
    # print(f'{start=} {end=} {level=} {lvl_cnt=} {div=} {vis.m_count=}')
    w = table_w // div
    x = vis.separator_size + (start - 1) * w
    # if level > 0: x += w // 2
    if level > 0:
      x = (vis.config.screen_width - lvl_cnt * w) // 2 + (start - 1) * w
    y = vis.table_y + (level + 1) * h
    return [x, y, w, h]

  def convert(self, x, y):
    vis = self.vis
    cw, ch = vis.config.screen_width, vis.config.screen_height
    sep, fs = vis.separator_size, vis.config.font_size
    if y < vis.table_y: return -1, -1
    h = vis.table_h // vis.m_count
    level = (y - vis.table_y) // h - 1
    lvl_cnt = vis.m_count - level - 1
    div = lvl_cnt if (level <= 0) else (lvl_cnt + 1)
    if level > 0:
      a = vis.m_count - 1
      div = (lvl_cnt  - 1) * (a - 3) / (a - 1) + 3

    table_w = vis.config.screen_width - 2 * vis.separator_size
    w = table_w // div

    if level > 0:
      sx = (vis.config.screen_width - lvl_cnt * w) // 2
    else:
      sx = vis.separator_size

    col = int((x - sx) // w)
    start, end = 1 + col, 2 + level + col

    # print(f'{level=} {col=} {start=} {end=}')
    return start, end


  def next_col(self, row, col):
    return row + 1, col + 1

  def initial_col(self):
    return 1, 1
