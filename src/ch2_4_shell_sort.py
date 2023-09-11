from data_unsorted import numbers
# from data_unsorted_a_lot import numbers
from vis import ShellSortVisualizer as Visualizer
# from vis import Dummy as Visualizer

from random import randint, seed, shuffle
from time import time

GAPS = [1750, 701, 301, 141, 63, 31, 15, 7, 3, 1, 0]
def next_gap(gap):
  for g in GAPS: 
    if gap > g: return g

def main_level_1():
  print('before:', array)
  count = len(array)
  gap = next_gap(count / 2.5)
  print(f'{count=} first_gap={gap}')
  while True:
    vis.set_gap(gap)
    for offset in range(gap):
      start = offset + gap
      while start < count:
        vis.mark_end(start, True)
        v = array[start]
        i = start
        while i >= gap:
          vis.compare(i-gap, i)
          if array[i - gap] > v:
            vis.shift(i-gap, i)
            array[i] = array[i - gap]
            vis.draw()
            i -= gap
          else:
            break
        vis.shift(start, i, True)
        array[i] = v
        vis.draw()
        start += gap
    gap = next_gap(gap)
    if gap < 1: break
  print('after :', array)

def main():
  print('before:', array)
  count = len(array)

  gap = next_gap(count / 2.5)
  print(f'{count=} first_gap={gap}')
  while True:
    vis.set_gap(gap)
    for offset in range(gap):
      start = offset + gap
      while start < count:
        vis.mark_end(start, True)
        v = array[start]
        i = start
        while i >= gap:
          vis.compare(i-gap, i)
          if array[i - gap] > v:
            vis.shift(i-gap, i)
            array[i] = array[i - gap]
            vis.draw()
            i -= gap
          else:
            break
        vis.shift(start, i, True)
        array[i] = v
        vis.draw()
        start += gap
    gap = next_gap(gap)
    if gap < 1: break

  print('after :', array)

if __name__ == '__main__':
  seed('Hello') # 'Hello' 를 seed 로 고정하여 randint 가 항상 같은 결과가 나오게 한다
  vis = Visualizer('Selection Sort')

  while True:
    count = randint(10, 30)
    array = numbers[:count]
    vis.setup(vis.get_main_module())
    main()
    # vis.set_gap(1)
    vis.mark_end(0)
    # vis.draw()

    again = vis.end()
    if not again: break

