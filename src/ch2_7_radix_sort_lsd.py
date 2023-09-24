# from data_unsorted import numbers
from data_unsorted_a_lot import numbers
from vis import RadixSortLsdVisualizer as Visualizer
# from vis import Dummy as Visualizer
from time import time
from random import randint, seed, shuffle
from math import log10, ceil

def main():
  global array              # result 를 다시 array 에 복사하므로 global 선언이 필요하다
  print('before:', array)
  count = len(array)

  global counts
  max_value = max(array)                       # 제일 큰 수가 몇인지
  radix_count = ceil(log10(max_value + 1))     # 제일 큰 수는 몇자리 수인지
  print(f'{max_value=} {log10(max_value)=} {radix_count=}')

  global result
  result = []

  div = 1                         # div 는 1, 10, 100 등으로 증가한다
  for pos in range(radix_count):  # radix_count 만큼 진행한다
    counts = [0] * 10             # 10개짜리 배열 생성 - 자리수마다 초기화해야 한다
    for i in range(count):
      v = array[i] // div % 10    # div 의 자리 숫자를 구하면 v 는 0~9 의 숫자가 된다
      counts[v] += 1
      vis.set_inc_index(div, i)

    print(f'counts= {counts}') 
    vis.set_inc_index(div, -1)
    for i in range(9):            # 10진수는 숫자가 0~9 까지 10개가 있으므로 합산은 0~8 까지만 하면 된다
      counts[i+1] += counts[i]
      vis.draw()
      vis.wait(1000)

    print(f'indices={counts}') 

    result = [None] * count

    for i in range(count-1, -1, -1):  # 거꾸로 진행
      v = array[i] // div % 10    # div 의 자리 숫자를 구하면 v 는 0~9 의 숫자가 된다
      at = counts[v] - 1              # 어디에 넣어야 하는지 구한다. counts[v] 는 v 가 들어가야 할 index+1 을 담고 있다
      counts[v] -= 1                  # index 는 1 빼준다
      vis.set_inc_index(div, i, False)
      result[at] = array[i]                  # 구한 인덱스에 해당 값을 넣는다
      # print(f'{i=:2d} {v=:2d} {result=}')

    vis.result_to_array()
    array = result                # 결과를 다시 array 에 넣고 다음 자리수 정렬을 한다
    result = []                   # 결과는 비어 있는 배열로 초기화한다
    div *= 10                     # 1 다음은 10, 그 다음은 100 이 되도록 해야 하니 10배가 되도록 한다

  print('after :', array)
'''성능측정
count=100    elapsed=0.000
count=1000   elapsed=0.003
count=2000   elapsed=0.005
count=3000   elapsed=0.009
count=4000   elapsed=0.011
count=5000   elapsed=0.013
count=6000   elapsed=0.018
count=7000   elapsed=0.019
count=8000   elapsed=0.022
count=9000   elapsed=0.024
count=10000  elapsed=0.027
count=15000  elapsed=0.039
count=20000  elapsed=0.053
count=30000  elapsed=0.082
count=40000  elapsed=0.104
count=50000  elapsed=0.139
count=100000 elapsed=0.281
count=200000 elapsed=0.594
count=300000 elapsed=0.957
count=400000 elapsed=1.366
count=500000 elapsed=1.700
count=1000000 elapsed=  3.170
count=2000000 elapsed=  7.663
count=3000000 elapsed= 11.760
count=4000000 elapsed= 15.379
count=5000000 elapsed= 18.720
count=10000000 elapsed=45.267
'''

if __name__ == '__main__':
  seed('HelloCountSort')
  vis = Visualizer('Radix Sort: LSD')
  while True:
    kind = 100000                           # 0~99999사이의 수 생성
    count = randint(30, 80)                 # 30개~80개 를 생성
    print(f'Creating data: {kind=} {count=}')
    array = list(map(lambda x: randint(1, kind), range(count)))
    vis.setup(vis.get_main_module())
    main()
    vis.draw()
    again = vis.end()
    if not again: break
