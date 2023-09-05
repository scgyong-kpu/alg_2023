from vis.base import *
from vis.color import *

clr = Color()
clr_compare = Color.Moccasin
clr_max = Color.Crimson

class ArrayVisualizer(Visualizer):
  def setup(self, data):
    self.data = data
    self.draw()

  def draw(self):
    self.clear()
    self.calc_coords()
    self.draw_content()
    self.update_display()

  def draw_content(self):
    self.draw_table()

  def calc_coords(self):
    self.cell_w = (self.config.screen_width - 2 * self.separator_size) // len(self.data.array)
    if self.cell_w > 150: self.cell_w = 150

    self.table_y = self.config.screen_height * 2 // 5

  def draw_table(self):
    for i in range(len(self.data.array)):
      self.draw_cell(i)

  def draw_cell(self, index):
    rect = self.get_rect(index)
    self.draw_box(rect, text=str(self.data.array[index]))

  def get_rect(self, index):
    x = self.separator_size + index * self.cell_w 
    return [x, self.table_y, self.cell_w, self.cell_w]

class FindMaxVisualizer(ArrayVisualizer):
  def setup(self, data):
    self.max_index = -1
    self.compare_index = -1
    super().setup(data)

  def compare(self, index):
    self.compare_index = index
    self.draw()
    self.wait(1000)

  def update(self):
    self.max_index = self.compare_index
    self.draw()
    self.wait(1000)

  def draw_content(self):
    super().draw_content()
    if self.max_index >= 0:
      rect = self.get_rect(self.max_index)
      rect[1] -= self.separator_size
      rect[3] = self.separator_size
      self.draw_box(rect, f'@{self.max_index}', no_line=True, no_body=True, font=self.big_font)
    if self.compare_index >= 0:
      rect = self.get_rect(self.compare_index)
      rect[1] += rect[3]
      rect[3] = self.separator_size

      value = self.data.array[self.compare_index]
      max = self.data.array[self.max_index] if self.max_index >= 0 else float('-inf')
      if value > max:
        text = f'{value} > {max}'
        font = self.big_font
      elif value < max:
        text = f'{value} < {max}'
        font = self.small_font
      else:
        text = f'{value} == {max}'
        font = self.small_font
      self.draw_box(rect, text, no_line=True, no_body=True, font=font)

  def draw_cell(self, index):
    rect = self.get_rect(index)
    if index == self.max_index:
      color = clr_max
    elif index == self.compare_index:
      color = clr_compare
    else:
      color = Color.back
    self.draw_box(rect, text=str(self.data.array[index]), body_color=color)

class SearchVisualizer(ArrayVisualizer):
  def setup(self, data):
    self.found_index = -1
    self.compare_index = -1
    self.lt_gt = False
    super().setup(data)

  def compare(self, index):
    self.compare_index = index
    self.draw()
    self.wait(1000)

  def update(self):
    self.found_index = self.compare_index
    self.draw()
    self.wait(1000)

  def draw_content(self):
    super().draw_content()
    self.draw_upper_text()
    self.draw_lower_text()

  def draw_upper_text(self):
    if self.found_index >= 0:
      rect = self.get_rect(self.found_index)
      rect[1] -= self.separator_size
      rect[3] = self.separator_size
      self.draw_box(rect, f'@{self.found_index}', no_line=True, no_body=True, font=self.big_font)
    else:
      xy = self.separator_size, self.separator_size
      self.draw_text(f'{self.data.to_find} Not Found', xy, center=False, font=self.big_font)

  def draw_lower_text(self):
    # print(f'draw_lower_text: {self.compare_index=}')
    if self.compare_index >= 0:
      rect = self.get_rect(self.compare_index)
      rect[1] += rect[3]
      rect[3] = self.separator_size

      value = self.data.array[self.compare_index]
      if value == self.data.to_find:
        op = '=='
        font = self.big_font
      else:
        if self.lt_gt:
          if value > self.data.to_find:
            op = '>'
          else:
            op = '<'
        else:
          op = '!='
        font = self.small_font
      text = f'{value} {op} {self.data.to_find}'
      self.draw_box(rect, text, no_line=True, no_body=True, font=font)

  def draw_cell(self, index):
    rect = self.get_rect(index)
    if index == self.found_index:
      color = clr_max
    elif index == self.compare_index:
      color = clr_compare
    else:
      color = Color.back
    self.draw_box(rect, text=str(self.data.array[index]), body_color=color)

class BinarySearchVisualizer(SearchVisualizer):
  def setup(self, data):
    self.mark_left = -1
    self.mark_right = -1
    super().setup(data)
    self.lt_gt = True

  def mark(self, left, right):
    self.mark_left = left
    self.mark_right = right
    self.draw()
    self.wait(1000)

  def calc_coords(self):
    super().calc_coords()
    self.mark_y = self.table_y - self.config.font_size // 2

  def draw_upper_text(self):
    super().draw_upper_text()
    if self.found_index >= 0:
      return
    valid_range = self.mark_left >= 0 and self.mark_left <= self.mark_right
    lr_color = Color.Indigo
    mid_color = Color.DarkOliveGreen
    if self.mark_left >= 0:
      x,_,_,_ = self.get_rect(self.mark_left)
      text = f'[{self.mark_left}' if valid_range else ']['
      self.draw_text(text, [x, self.mark_y], text_color=lr_color)
    if self.mark_right >= 0 and valid_range:
      x,_,w,_ = self.get_rect(self.mark_right)
      x += w
      self.draw_text(f'{self.mark_right}]', [x, self.mark_y], text_color=lr_color)

    mid = (self.mark_left + self.mark_right) // 2
    if mid >= 0 and valid_range: # and mid == self.compare_index:
      x,_,w,_ = self.get_rect(mid)
      x += w // 2
      self.draw_text(f'{mid}', [x, self.mark_y], text_color=mid_color)

  def draw_cell(self, index):
    rect = self.get_rect(index)
    if index == self.found_index:
      color = Color.Crimson
    elif index == self.compare_index:
      color = Color.OrangeRed
    elif self.mark_left <= index and index <= self.mark_right:
      color = Color.Cornsilk
    else:
      color = Color.back
    self.draw_box(rect, text=str(self.data.array[index]), body_color=color)

