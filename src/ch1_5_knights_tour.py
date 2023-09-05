from vis import KnightsTourVisualizer as Visualizer
# from vis import Dummy as Visualizer

from random import choice

start_x, start_y = 0, 0
offsets = [
  [ 1, -2 ], [ 2, -1 ], [  2,  1 ], [  1,  2 ],
  [ -1, 2 ], [ -2, 1 ], [ -2, -1 ], [ -1, -2 ],
]

walks = 0
step = 0
candidates = [ -1 for _ in range(8) ]

def brute_force():
  global walks, step
  x,y = start_x, start_y
  step, end = 1, cx * cy
  board[y][x] = [step, -1, -1]
  walks = 0

  while step < cx * cy:
    w = board[y][x][1] + 1
    if w == 8: 
      # back to origin
      o = board[y][x][2]
      if o == -1:
        return # no origin = start position
      dx,dy = offsets[o]
      board[y][x] = [0,-1,-1]
      x -= dx
      y -= dy
      step -= 1
      walks += 1
      vis.step_back()
      continue
    board[y][x][1] = w
    walks += 1
    vis.try_dir(w)
    dx, dy = offsets[w]
    nx, ny = x+dx, y+dy
    # print(f'{step=} {x=} {y=} {w=} {dx=} {dy=} {nx=} {ny=}')
    if nx < 0 or nx >= cx or ny < 0 or ny >= cy: continue
    if board[ny][nx][0] > 0: continue
    x,y = nx,ny
    step += 1
    board[y][x] = [step, -1, w]
    vis.step_forward()

def warnsdorff():
  global walks, step, candidates
  x,y = start_x, start_y
  step, end = 1, cx * cy
  # board[y][x] = [step, -1, -1]
  walks = 0

  while step < cx * cy:
    board[y][x][0] = step
    candidates = [ -1 for _ in range(8) ]
    smallest, at = 9, -1
    for w in range(8):
      dx,dy = offsets[w]
      nx,ny = x+dx, y+dy
      walks += 1
      if nx < 0 or nx >= cx or ny < 0 or ny >= cy: continue
      if board[ny][nx][0] > 0: continue
      board[y][x][1] = w
      count = 0
      for w2 in range(8):
        dx2,dy2 = offsets[w2]
        nx2,ny2 = nx+dx2, ny+dy2
        if nx2 < 0 or nx2 >= cx or ny2 < 0 or ny2 >= cy: continue
        if board[ny2][nx2][0] > 0: continue
        count += 1
        walks += 1
      candidates[w] = count
      if smallest > count:
        smallest = count
        at = w
      elif smallest == count:
        if choice([0,1]) == 1:
          at = w
      vis.show_candidates(candidates, x, y, w, at, count)
    if at < 0: return # no way to go

    board[y][x][1] = at

    step += 1
    dx,dy = offsets[at]
    x,y = x+dx, y+dy
    board[y][x] = [step, -1, -1]

    vis.step_forward()

  vis.draw()

def print_board():
  print(f'After {walks} walks:')
  for y in range(cy):
    for x in range(cx):
      s = board[y][x][0]
      t = f'{s:4d}' if s > 0 else '   '
      print(t, end='')
    print()

uses_warnsdorff = True
# uses_warnsdorff = False
# warnsdorff 를 사용하지 않으면
# 5x5 는 walks = 252 까지
# 6x6 은 walks = 48616 까지
# 8x8 은 walks = 29178254 까지
# 진행해야 끝나므로 5x5 를 제외하면 Dummy Visualizer 를 사용할 것을 권장한다

if __name__ == '__main__':
  vis = Visualizer('Find Max Value')
  if uses_warnsdorff:
    sizes = [8,10,12,14,16,18,20]
  else:
    sizes = [5,6,8]

  sz_idx = -1
  # 252, 48616, 29178254

  while True:
    sz_idx = (sz_idx + 1) % len(sizes)
    cx = sizes[sz_idx]
    cy = cx
    board = [[ [0,-1,-1] for _ in range(cx) ] for _ in range(cy)]
    print(f'{cx=} {cy=}')
    # print(board)
    vis.setup(vis.get_main_module())
    if uses_warnsdorff:
      warnsdorff()
    else:
      brute_force()
    print_board()
    vis.draw()
    again = vis.end()
    if not again: break


