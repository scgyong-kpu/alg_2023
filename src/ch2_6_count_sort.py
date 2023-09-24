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

  vis.set_inc_index(-1)
  for i in range(max_value):
    counts[i+1] += counts[i]
    vis.draw()
    vis.wait(1000)

  global result
  result = [None] * count

  for i in range(count-1, -1, -1):  # 거꾸로 진행
    v = array[i]                    # 값을 가져다가
    at = counts[v] - 1              # 어디에 넣어야 하는지 구한다. counts[v] 는 v 가 들어가야 할 index+1 을 담고 있다
    counts[v] -= 1                  # index 는 1 빼준다
    vis.set_inc_index(i, False)
    result[at] = v                  # 구한 인덱스에 해당 값을 넣는다
    # print(f'{i=:2d} {v=:2d} {result=}')

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
