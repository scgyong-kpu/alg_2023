import random
from math import sqrt
# import cluster_visualizer as vis

# def draw_circle(c):
#   x, y, r = c
#   vis.draw_circle(x, y, r, 0)

def welzl(pts):
  # points = list(map(lambda pt: (pt.x, pt.y), pts))
  points = pts.copy()
  random.shuffle(points)
  # print('input=', points)
  return welzl_helper(points, [], len(points))

depth = 0
def welzl_helper(P, R, n):
  global depth

  depth += 1

  # print(' ' * depth, 'a n=', n, 'P=', len(P), 'R=', len(R), P)
  if n == 0 or len(R) == 3:
    circle = min_circle_trivial(R)
    # print(' ' * depth, circle)
    depth -= 1
    return circle
  idx = random.randrange(n)
  p = P[idx]

  P[idx], P[n-1] = P[n-1], P[idx]
  # print(' ' * depth, 'b idx=', idx)

  circle = welzl_helper(P, R, n - 1)
  # draw_circle(circle)
  if is_inside(circle, p):
    # print(' ' * depth, circle)
    depth -= 1
    return circle

  R2 = R.copy()
  R2.append(p)
  # print(' ' * depth, 'R2=', R2)
  circle = welzl_helper(P, R2, n - 1)
  # print(' ' * depth, circle)
  depth -= 1
  return circle

def min_circle_trivial(P):
  np = len(P)
  if np == 0:
    return (0, 0, 0)
  if np == 1:
    return (P[0].x, P[0].y, 0)
  if np == 2:
    return circle_from_2(P[0], P[1])

  for i in range(3):
    for j in range(i+1, 3):
      c = circle_from_2(P[i], P[j])
      if is_valid_circle(c, P):
        return c

  return circle_from_3(P[0], P[1], P[2])

def is_valid_circle(c, P):
  for p in P:
    if not is_inside(c, p):
      return False
  return True

def circle_from_2(a, b):
  x = (a.x + b.x) / 2
  y = (a.y + b.y) / 2
  r = dist(a, b) / 2
  return x, y, r

def circle_from_3(a, b, c):
  x, y = get_circle_center( \
    b.x - a.x, b.y - a.y,   \
    c.x - a.x, c.y - a.y)
  x += a.x
  y += a.y
  return x, y, dist_tuple((x, y), (a.x, a.y))

def get_circle_center(bx, by, cx, cy):
  b = bx * bx + by * by
  c = cx * cx + cy * cy
  d = bx * cy - by * cx
  x = (cy * b - by * c) / (2 * d)
  y = (bx * c - cx * b) / (2 * d)
  return x, y

def is_inside(circle, p):
  x,y,r = circle
  inside = dist_tuple((x, y), (p.x, p.y)) < r
  # print(' ' * depth, 'is_inside(', circle, p, ')', inside)
  return inside

def dist(a, b):
  return sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)

def dist_tuple(a, b):
  ax,ay = a
  bx,by = b
  return sqrt((ax - bx) ** 2 + (ay - by) ** 2)


if __name__ == '__main__':
  pts = []
  class Point: 
    def __repr__(self): return '(%.1f,%1.f)' % (self.x, self.y)
  for i in range(10):
    o = Point()
    o.x = random.randint(1, 100)
    o.y = random.randint(1, 100)
    pts.append(o)
  print(pts)
  circle = welzl(pts)
  print(circle)