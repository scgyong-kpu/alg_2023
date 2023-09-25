# from data_unsorted import numbers
from data_unsorted_a_lot import numbers
from vis import CountSortVisualizer as Visualizer
# from vis import Dummy as Visualizer
from time import time
from random import randint, seed, shuffle

def main():
  print('before:', array)
  count = len(array)

  global counts
  max_value = max(array)
  counts = [0] * (max_value + 1)
  # print(f'init  - {counts=}') 

  global result
  result = []

  for i in range(count):
    v = array[i]
    counts[v] += 1
    vis.set_inc_index(i)

  vis.set_inc_index(-1)
  for i in range(max_value):
    counts[i+1] += counts[i]
    vis.draw()
    vis.wait(1000)

  # global result
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

''' 성능측청
count=100    kind=291 elapsed=0.000
count=1000   kind=261 elapsed=0.001
count=2000   kind=270 elapsed=0.001
count=3000   kind=296 elapsed=0.001
count=4000   kind=182 elapsed=0.001
count=5000   kind=44  elapsed=0.001
count=6000   kind=33  elapsed=0.002
count=7000   kind=172 elapsed=0.001
count=8000   kind=57  elapsed=0.006
count=9000   kind=58  elapsed=0.002
count=10000  kind=45  elapsed=0.002
count=15000  kind=289 elapsed=0.004
count=20000  kind=293 elapsed=0.005
count=30000  kind=173 elapsed=0.008
count=40000  kind=153 elapsed=0.010
count=50000  kind=53  elapsed=0.013
count=100000 kind=13  elapsed=0.030
count=200000 kind=128 elapsed=0.053
count=300000 kind=293 elapsed=0.083
count=400000 kind=208 elapsed=0.107
count=500000 kind=14  elapsed=0.123

Creating List: count=1000000 elapsed=0.768
count=1000000 kind=291 elapsed=0.292
Creating List: count=10000000 elapsed=6.655
count=10000000 kind=212 elapsed=2.973
Creating List: count=100000000 elapsed=68.944
count=100000000 kind=142 elapsed=27.270
'''

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
