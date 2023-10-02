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
  pi = qs.partition(left, right)
  vis.set_pivot(pi)

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