from data_unsorted import numbers
# from data_unsorted_a_lot import numbers
from vis import SelectionSortVisualizer as Visualizer
# from vis import Dummy as Visualizer

from random import randint, seed, shuffle
from time import time

def main():
  print('before:', array)
  count = len(array)

  for a in range(count):
    min_value = array[a]
    min_at = a
    vis.selection(a)
    for b in range(a + 1, count):
      vis.compare(min_at, b)
      if min_value > array[b]:
        min_value = array[b]
        min_at = b
        vis.selection(b)
    vis.swap(a, min_at)
    array[a], array[min_at] = array[min_at], array[a]
    vis.mark_done(a)
    # print(f'{min_at=}. swap {a} <=> {min_at}')

  print('after :', array)

'''
Comparison: 45
Swap: 10
'''

if __name__ == '__main__':
  seed('Hello') # 'Hello' 를 seed 로 고정하여 randint 가 항상 같은 결과가 나오게 한다
  vis = Visualizer('Selection Sort')

  while True:
    count = randint(10, 30)
    array = numbers[:count]
    vis.setup(vis.get_main_module())
    main()
    vis.draw()

    again = vis.end()
    if not again: break
