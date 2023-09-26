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
    print(f'{min_at=}. swap {a} <=> {min_at}')

  print('after :', array)

'''

성능측정:
count=100 elapsed=0.001
count=1000 elapsed=0.026
count=2000 elapsed=0.107
count=3000 elapsed=0.237
count=4000 elapsed=0.324
count=5000 elapsed=0.490
count=6000 elapsed=0.677
count=7000 elapsed=0.986
count=8000 elapsed=1.256
count=9000 elapsed=1.614
count=10000 elapsed=1.897
count=15000 elapsed=4.837
count=20000 elapsed=8.258
count=30000 elapsed=19.132
count=40000 elapsed=35.200
count=50000 elapsed=53.683

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
