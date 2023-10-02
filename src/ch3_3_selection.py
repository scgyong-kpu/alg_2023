from data_unsorted import numbers
# from data_unsorted_a_lot import numbers
from vis import SelectionVisualizer as Visualizer
# from vis import Dummy as Visualizer
from time import time
from random import randint, seed, shuffle

import ch3_2_quick_sort as qs

def main():
  qs.array = array
  qs.vis = vis
  print('before:', array)
  count = len(array)
  value = selection(0, count-1, n_th)

def selection(left, right, k): #right=inclusive
  print(f'{left=} {right=} {k=}')
  vis.push(left, right, k)
  pi = qs.partition(left, right) # pivot 의 위치를 구한다 (Pivot Index)
  vis.set_pivot(pi)
  small_group_size = pi - left   # pi 를 기준으로 왼쪽 그룹의 크기를 구해둔다
  if k == small_group_size + 1:  # pi 의 왼쪽 그룹의 크기가 sgs 인데 sgs+1번째를 찾는다면
    return array[pi]             # pi 가 찾으려는 값의 위치이다
  if k <= small_group_size:            # 왼쪽 그룹의 수보다 k 가 작으면
    return selection(left, pi - 1, k)  # 왼쪽 그룹에서 k 번째를 다시 찾는다
  else:
    return selection(pi + 1, right, k - small_group_size - 1) # 오른쪽 그룹에서 k-sgs-1 번째를 찾는다

if __name__ == '__main__':
  seed('none')
  vis = Visualizer('Selection')
  while True:
    count = randint(20, 40)
    array = numbers[:count]
    shuffle(array)
    n_th = randint(1, count)
    # array=[4,8,10,2,1,3]
    vis.setup(qs)    
    main()
    vis.draw()
    again = vis.end()
    if not again: break