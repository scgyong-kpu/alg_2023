from data_unsorted import numbers
# from data_unsorted_a_lot import numbers
from vis import SelectionVisualizer as Visualizer
# from vis import Dummy as Visualizer
from time import time
from random import randint, seed, shuffle

def main():
  print('before:', array)
  count = len(array)

if __name__ == '__main__':
  seed('none')
  vis = Visualizer('Selection')
  while True:
    count = randint(20, 40)
    array = numbers[:count]
    shuffle(array)
    n_th = randint(1, count)
    # array=[4,8,10,2,1,3]
    vis.setup(vis.get_main_module())
    main()
    vis.draw()
    again = vis.end()
    if not again: break