import pygame as pg
import json
from vis.color import *

CONFIG_FILE = '_config.json'
INITIAL_SCREEN_SIZE = [ 960, 540 ]
INITIAL_FONT_SIZE = 12

def rect_center(rect):
  x,y,w,h = rect
  return [x+w//2, y+h//2]

def rect_inflate(rect, amount):
  x,y,w,h = rect
  return [x-amount, y-amount, w+2*amount, h+2*amount]

def attr(dict, key, def_value):
  return dict[key] if key in dict else def_value

WAIT_ONE_FRAME_MILLIS = 15

class DrawContext:
  def kwarg(self): return self.__dict__

class Visualizer:
  class Config: pass
  SPEEDS = [ 200, 1, 2, 3, 4, 5, 10, 20, 50, 100 ]

  def __init__(self, window_title):
    pg.init()

    self.speed = 1

    self.config = Visualizer.Config()
    self.load_config()
    self.apply_config()
    pg.display.set_caption(window_title)
    self.ctx = DrawContext()
    self.paused = False

  def apply_config(self):
    screen_size = [ self.config.screen_width, self.config.screen_height ]
    self.screen = pg.display.set_mode(screen_size)
    self.small_font = pg.font.SysFont("arial", self.config.font_size) 
    self.big_font = pg.font.SysFont("arial", self.config.font_size * 2)
    self.separator_size = self.config.font_size * 3

  def load_config(self):
    loaded = False
    try:
      f = open(CONFIG_FILE, 'r')
      data = json.load(f)
      f.close()
      self.config.__dict__.update(data)
      loaded = True
      print(config.__dict__)
    except: pass

    if not loaded:
      self.config.screen_width, self.config.screen_height = INITIAL_SCREEN_SIZE
      self.config.font_size = INITIAL_FONT_SIZE

  def save_config(self):
    try:
      f = open(CONFIG_FILE, 'w')
      json.dump(self.config.__dict__, f)
      f.close()
    except:
      print('Could not write config to:', CONFIG_FILE)

  def get_main_module(self):
    import sys
    main_module = sys.modules['__main__']
    return main_module

  def set_screen_size(self, d):
    self.config.screen_width += d * 80
    self.config.screen_height += d * 45
    self.config.font_size += d

    self.apply_config()
    self.save_config()
    self.draw()

  def draw(self):
    self.clear()
    self.draw_content()
    self.update_display()

  def draw_content(self):
    pass

  def clear(self, color = Color.back):
    self.screen.fill(color)

  def wait(self, millis):
    millis = int(millis / self.speed)
    if millis < WAIT_ONE_FRAME_MILLIS: millis = WAIT_ONE_FRAME_MILLIS

    pg.time.wait(millis)
    self.loop, first = True, True
    while self.loop:
      if first:
        self.loop, first = False, False
      for e in pg.event.get():
        if self.handle_event(e):
          continue
        if e.type == pg.KEYDOWN and e.key == pg.K_SPACE:
          self.loop = True
          self.paused = True
        elif e.type == pg.KEYUP and e.key == pg.K_SPACE:
          if pg.key.get_mods() & pg.KMOD_LSHIFT == 0:
            self.loop = False
            self.paused = False

  def handle_event(self, e):
    if e.type == pg.QUIT:
      pg.quit()
      self.loop = False
      return True
    elif e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
      pg.quit()
      self.loop = False
      return True
    elif e.type == pg.KEYDOWN and e.key >= pg.K_0 and e.key <= pg.K_9:
      self.speed = self.SPEEDS[e.key - pg.K_0]
    elif e.type == pg.KEYDOWN and e.key == pg.K_COMMA:
      self.set_screen_size(-1)
    elif e.type == pg.KEYDOWN and e.key == pg.K_PERIOD:
      self.set_screen_size(1)
    elif e.type == pg.MOUSEMOTION and self.paused:
      return self.on_mouse_motion()
    return False

  def on_mouse_motion(self): 
    return True

  def wait_for_keydown(self):
    self.loop = True
    self.paused = True
    while self.loop:
      for e in pg.event.get():
        if self.handle_event(e):
          continue
        if e.type == pg.KEYDOWN:
          self.loop = False
    self.paused = False

  def end(self):
    self.loop = True
    self.paused = True
    while self.loop:
      for e in pg.event.get():
        if e.type == pg.KEYDOWN and e.key == pg.K_r:
          self.speed = 1
          self.loop = self.paused = False
          mods = pg.key.get_mods()
          self.restart_lshift = mods & pg.KMOD_LSHIFT != 0
          self.restart_rshift = mods & pg.KMOD_RSHIFT != 0
          return True
        self.handle_event(e)
    pg.quit()
    return False

  def update_display(self):
    pg.display.flip()

  def animate(self, duration):
    duration //= self.speed
    frames = duration // WAIT_ONE_FRAME_MILLIS
    if frames < 2: frames = 2
    for i in range(1, frames+1):
      self.anim_progress = i / frames
      self.draw()
      self.wait(WAIT_ONE_FRAME_MILLIS)

  def clip(self, rect):
    self.screen.set_clip(rect)

  def draw_box(self, box, text=None, **args):
    border_radius = attr(args, 'border_radius', 0)
    if not attr(args, 'no_body', False):
      body_color = attr(args, 'body_color', Color.back)
      pg.draw.rect(self.screen, body_color, box, border_radius=border_radius)
    if not attr(args, 'no_line', False):
      line_color = attr(args, 'line_color', Color.line)
      width = attr(args, 'width', 1)
      pg.draw.rect(self.screen, line_color, box, width, border_radius=border_radius)
    if text != None:
      self.draw_text(text, pg.Rect(box).center, **args, center=True)

  def draw_circle(self, xy, radius, text=None, **args):
    if not attr(args, 'no_body', False):
      body_color = attr(args, 'body_color', Color.back)
      pg.draw.circle(self.screen, body_color, xy, radius)
    if not attr(args, 'no_line', False):
      line_color = attr(args, 'line_color', Color.line)
      width = attr(args, 'width', 1)
      pg.draw.circle(self.screen, line_color, xy, radius, width)
    if text != None:
      self.draw_text(text, xy, **args, center=True)

  def draw_text(self, text, xy, center=True, **args):
    font = attr(args, 'font', self.small_font)
    color = attr(args, 'text_color', Color.text)
    if '\n' in text:
      lines = text.split('\n')
      x, y = xy
      if center:
        y -= (len(lines) - 1) * self.config.font_size // 2
      for line in lines:
        img = font.render(line, True, color)
        if center:
          rect = img.get_rect(center=[x,y])
          self.screen.blit(img, rect)
        else:
          self.screen.blit(img, [x, y])
        y += self.config.font_size
    else:
      img = font.render(text, True, color)
      if center:
        rect = img.get_rect(center=xy)
        self.screen.blit(img, rect)
      else:
        self.screen.blit(img, xy)

    return img.get_size()

class TestVisualizer(Visualizer):
  def draw(self):
    self.clear()
    self.draw_box([10, 10, 100, 100], text='Hello')
    self.draw_box([10, 210, 100, 100], 
      text='Hello\nworld\nGood\nBoy', 
      body_color=Color.pastel2[0],
      line_color=Color.set2[0],
    )
    self.draw_text('Hello\nworld\nGood\nBoy', [120, 10], center=False)
    self.update_display()

if __name__ == '__main__':
  vis = TestVisualizer('Visualizer Test')
  vis.draw()
  vis.update_display()
  vis.end()

