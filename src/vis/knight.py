# import math
from vis.base import *

class KnightsTourVisualizer(Visualizer):
  ctx_normal = {
    # 'body_color': Color.back,
    'line_color': Color.line,
  }
  ctx_cand = {
    'no_line': True,
    'body_color': Color.PowderBlue,
    'text_color': Color.MidnightBlue,
  }
  ctx_current = {
    'no_line': True,
    'body_color': Color.DodgerBlue,
    'text_color': Color.MidnightBlue,
  }
  ctx_smallest = {
    'no_line': True,
    'body_color': Color.SaddleBrown,
    'text_color': Color.MidnightBlue,
  }
  def setup(self, data):
    self.data = data

  def try_dir(self, w):
    self.draw()
    self.wait(100)

  def step_forward(self):
    self.draw()
    self.wait(100)
    
  def step_back(self):
    self.draw()
    self.wait(100)
    
  def show_candidates(self, candidates, x, y, way, at, count):
    self.draw()
    for w in range(8):
      c = candidates[w]
      if c < 0: continue
      if w == way:
        ctx = self.ctx_current
      elif w == at:
        ctx = self.ctx_smallest
      else:
        ctx = self.ctx_cand

      dx, dy = self.data.offsets[w]
      rect = self.get_rect(x+dx,y+dy)
      rect = rect_inflate(rect, -rect[2] // 4)
      self.draw_box(rect, str(c), **ctx)
    self.update_display()
    self.wait(1000)

  def draw(self):
    self.clear()
    self.calc_coords()
    self.draw_content()
    self.update_display()

  def calc_coords(self):
    self.board_x = self.separator_size
    self.board_y = self.separator_size
    self.board_h = self.config.screen_height - 2 * self.separator_size
    self.board_w = self.board_h
    self.cell_w = self.board_w // self.data.cx
    self.cell_h = self.board_h // self.data.cy
    # print(f'{self.config.font_size=} {self.cell_w=}')

  def draw_content(self):
    for y in range(self.data.cy):
      for x in range(self.data.cx):
        self.draw_cell(x, y)
    self.draw_walks()
    self.draw_numbers()

  def draw_cell(self, x, y):
    rect = self.get_rect(x, y)
    value, way, origin = self.data.board[y][x]
    text = None if value == 0 else str(value)
    diff = self.data.step - value
    if diff > 6: diff = 6
    color = Color.BrownGroup[6-diff] if value > 0 else Color.back
    font = self.big_font if self.cell_w > 3 * self.config.font_size else self.small_font
    self.draw_box(rect, text, font=font, body_color=color, **self.ctx_normal)

  def get_rect(self, x, y):
    return [
      self.board_x + x * self.cell_w,
      self.board_y + y * self.cell_h,
      self.cell_w, self.cell_h
    ]

  def draw_walks(self):
    for y in range(self.data.cy):
      for x in range(self.data.cx):
        w = self.data.board[y][x][1]
        if w < 0: continue
        dx,dy = self.data.offsets[w]
        rect = self.get_rect(x, y)
        cx,cy = rect_center(rect)
        tx = cx + dx * self.cell_w // 5
        ty = cy + dy * self.cell_h // 5
        pg.draw.aaline(self.screen, Color.Crimson, [cx,cy], [tx,ty])

  def draw_numbers(self):
    x = self.board_x + self.board_w + self.separator_size
    y = self.board_y

    walks, step = self.data.walks, self.data.step

    text = f'walks = {walks}\n\nstep = {step}'
    self.draw_text(text, [x,y], center=False)




