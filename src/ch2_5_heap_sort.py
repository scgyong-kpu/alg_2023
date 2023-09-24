from data_unsorted import numbers
# from data_unsorted_a_lot import numbers
from random import randint, seed, shuffle
from vis import HeapSortVisualizer as Visualizer
# from vis import Dummy as Visualizer
from time import time

def main():
  print('before:', array)
  count = len(array)
  print('after :', array)
  vis.build_tree()


if __name__ == '__main__':
  seed('Hello')
  vis = Visualizer('Heap Sort')
  while True:
    array = numbers[:randint(10, 30)]
    vis.setup(vis.get_main_module())
    startedOn = time()
    main()
    elapsed = time() - startedOn
    print(f'Elapsed time = {elapsed:.3f}s')
    again = vis.end()
    if not again: break
