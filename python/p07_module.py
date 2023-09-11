#python 에는 많은 내장 모듈이 있다
import math
pt1, pt2 = [ -150, -100 ], [ 150, 300 ]
distance = math.sqrt((pt1[0]-pt2[0])**2 + (pt1[1]-pt2[1])**2)
print(f'두 점 {pt1} 과 {pt2} 사이의 거리는 {distance:.2f} 이다')

# 두 점이 이루는 각도를 구하려면 atan(y/x) 을 사용해야 한다
# 하지만 부호도 신경써야 하므로 atan2(y, x) 를 쓰면 알아서 해 준다
angle_radian = math.atan2((pt2[1]-pt1[1]), (pt2[0]-pt1[0]))

# Computer Graphics 는 대부분 radian 단위를 사용한다. 사람이 이해할 때는 Degree 가 편할때가 많다
angle_degree = 180 * angle_radian / math.pi

print(f'두 점 사이의 선이 만드는 각도는 Radian 으로는 {angle_radian:.2f}, Degree 로는 {angle_degree:.2f}° 이다')

# 길이를 알 때 각도만큼 회전했을 때의 좌표를 알려면 x 좌표는 cos, y 좌표는 sin 을 쓴다
dx = distance * math.cos(2 * angle_radian)
dy = distance * math.sin(2 * angle_radian)

pt3 = [pt1[0] + dx, pt1[1] + dy]
print(f'pt1 을 기준으로 {angle_degree:.2f}° 만큼 더 회전한 점은 [{pt3[0]:.2f}, {pt3[1]:.2f}] 이다')

import pygame as pg
RED, GREEN, BLUE = (255,0,0),(0,255,0),(0,0,255)
BLACK, WHITE = (0,0,0), (255,255,255)
pg.init()
screen = pg.display.set_mode([900, 900])
font = pg.font.SysFont("arial", 16)
pg.display.set_caption('Test')
screen.fill(WHITE)

def m2s(pt): # pt 가 수학 좌표계이므로 pygame 의 좌표계로 변경해 준다
  return [pt[0]+450,450 - pt[1]]

def d_line(pt1, pt2, color=BLACK):
  pg.draw.line(screen, color, m2s(pt1), m2s(pt2))

def d_pt(pt,color=BLACK,name=None): # 점은 원그리기 함수를 활용하여 표현한다
  xy = m2s(pt)
  pg.draw.circle(screen, color, xy, 5, 1)
  if name != None:
    img = font.render(name, True, color)
    screen.blit(img, xy)

# x축과 y 축을 그려준다
d_line([-450, 0], [450, 0]) 
d_line([0, -450], [0, 450])

# 세 개의 점을 그려 준다
d_pt(pt1, RED, 'pt1')
d_pt(pt2, GREEN, 'pt2')
d_pt(pt3, BLUE, 'pt3')

# Line 세 개를 그려서 각도가 보이도록 해 본다
d_line(pt1, [pt1[0]+distance,pt1[1]], (251,180,174))
d_line(pt1, pt2, (204,235,197))
d_line(pt1, pt3, (179,205,227))

pg.display.flip()

loop = True
while loop:
  for e in pg.event.get():
    if e.type == pg.QUIT:
      pg.quit()
      loop = False
      break
    elif e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
      pg.quit()
      loop = False
      break

pg.quit()
