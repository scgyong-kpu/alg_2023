import pygame as pg
import json

CONFIG_FILE = 'config.json'
INITIAL_SCREEN_SIZE = [ 960, 540 ]
INITIAL_FONT_SIZE = 12

def color_argb(value): 
  value = value.lstrip('#')
  lv = len(value)
  return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def color_argb_array(array): 
  return [ color_argb(value) for value in array ]

def rect_center(rect):
  x,y,w,h = rect
  return [x+w//2, y+h//2]

def rect_inflate(rect, amount):
  x,y,w,h = rect
  return [x-amount, y-amount, w+2*amount, h+2*amount]

class Color:
  # from D3.js colors
  pair = color_argb_array(["#a6cee3","#1f78b4","#b2df8a","#33a02c","#fb9a99","#e31a1c","#fdbf6f","#ff7f00","#cab2d6","#6a3d9a","#ffff99","#b15928"])
  pastel1 = color_argb_array(["#fbb4ae","#b3cde3","#ccebc5","#decbe4","#fed9a6","#ffffcc","#e5d8bd","#fddaec","#f2f2f2"])
  pastel2 = color_argb_array(["#b3e2cd","#fdcdac","#cbd5e8","#f4cae4","#e6f5c9","#fff2ae","#f1e2cc","#cccccc"])
  set1 = color_argb_array(["#e41a1c","#377eb8","#4daf4a","#984ea3","#ff7f00","#ffff33","#a65628","#f781bf","#999999"])
  set2 = color_argb_array(["#66c2a5","#fc8d62","#8da0cb","#e78ac3","#a6d854","#ffd92f","#e5c494","#b3b3b3"])
  set3 = color_argb_array(["#8dd3c7","#ffffb3","#bebada","#fb8072","#80b1d3","#fdb462","#b3de69","#fccde5","#d9d9d9","#bc80bd","#ccebc5","#ffed6f"])
  dark = color_argb_array(["#1b9e77","#d95f02","#7570b3","#e7298a","#66a61e","#e6ab02","#a6761d","#666666"])
  gray = color_argb_array(['#f0f0f0', '#dbdbdb', '#c1c1c1', '#9f9f9f', '#7d7d7d', '#5d5d5d', '#383838', '#121212'])
  back = color_argb('#ffffff')
  text = color_argb('#00001f')
  line = dark[0]

WAIT_ONE_FRAME_MILLIS = 15
screen = None

class Visualizer:
  class Config: pass
  class Context: pass
  SPEEDS = [ 200, 1, 2, 3, 4, 5, 10, 20, 50, 100 ]

  def __init__(self, window_title):
    pg.init()

    self.speed = 1

    self.config = Visualizer.Config()
    self.ctx = Visualizer.Context()
    self.load_config()
    self.apply_config()
    pg.display.set_caption(window_title)

  def apply_config(self):
    global screen
    screen_size = [ self.config.screen_width, self.config.screen_height ]
    screen = pg.display.set_mode(screen_size)
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

  def set_screen_size(self, d):
    self.config.screen_width += d * 80
    self.config.screen_height += d * 45
    self.config.font_size += d

    self.apply_config()
    self.save_config()
    self.draw()

  def draw(self):
    self.clear()
    self.update_display()

  def clear(self, color = Color.back):
    screen.fill(color)

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
        elif e.type == pg.KEYUP and e.key == pg.K_SPACE:
          self.loop = False

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
    elif e.type == pg.MOUSEMOTION:
      return self.on_mouse_motion()
    return False

  def on_mouse_motion(self): 
    return True

  def wait_for_keydown(self):
    self.loop = True
    while self.loop:
      for e in pg.event.get():
        if self.handle_event(e):
          continue
        if e.type == pg.KEYDOWN:
          self.loop = False

  def end(self):
    self.loop = True
    while self.loop:
      for e in pg.event.get():
        self.handle_event(e)
    pg.quit()

  def update_display(self):
    pg.display.flip()

  def screen(self):
    return screen

  def clip(self, rect):
    screen.set_clip(rect)

  def draw_text(self, text, xy, color=Color.text, horz_center=True, font=None):
    if font == None: font = self.small_font
    img = font.render(text, True, color)
    if (horz_center):
      rect = img.get_rect(center = xy)
      screen.blit(img, rect)
    else:
      screen.blit(img, xy)

  def draw_box(self, box, body_color=None, line_color=None, width=1, radius=0):
    if body_color != None:
      pg.draw.rect(screen, body_color, box, border_radius=radius)
    if line_color != None:
      pg.draw.rect(screen, line_color, box, width, border_radius=radius)


if __name__ == '__main__':
  vis = Visualizer('Visualizer Test')
  vis.draw()
  vis.end()
