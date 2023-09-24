# from data_unsorted import numbers
from data_unsorted_a_lot import numbers
from vis import CountSortVisualizer as Visualizer
# from vis import Dummy as Visualizer
from time import time
from random import randint, seed

def main():
  print('before:', array)
  count = len(array)

  global counts
  max_value = max(array)
  counts = [0] * (max_value + 1)
  print(f'init  - {counts=}') 

  for i in range(count):
    v = array[i]
    counts[v] += 1
    vis.set_inc_index(i)

  vis.set_inc_index(-1, False)
  print('after :', array)

if __name__ == '__main__':
  seed('HelloCountSort')
  vis = Visualizer('Count Sort')
  while True:
    kind = randint(6, 30)
    count = randint(30, 150)
    print(f'Creating data: {kind=} {count=}')
    array = list(map(lambda x: x%kind, numbers[1000:1000+count]))
    vis.setup(vis.get_main_module())
    main()
    vis.draw()
    again = vis.end()
    if not again: break
