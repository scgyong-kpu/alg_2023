# from data_unsorted import numbers
from data_unsorted_a_lot import numbers
from vis import RadixSortLsdVisualizer as Visualizer
# from vis import Dummy as Visualizer
from time import time
from random import randint, seed, shuffle
from math import log10, ceil

def main():
  print('before:', array)
  count = len(array)

  global counts
  max_value = max(array)                       # 제일 큰 수가 몇인지
  radix_count = ceil(log10(max_value))         # 제일 큰 수는 몇자리 수인지
  print(f'{max_value=} {log10(max_value)=} {radix_count=}')
  counts = [0] * 10                            # 10진수 기준으로 셀 예정이므로 10개짜리 배열 생성

  global result
  result = []

  div = 1                         # div 는 1, 10, 100 등으로 증가할 예정이다
  for pos in range(1):            # 임시로 div=1 일 때만 시도한다
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


  # print('after :', array)

if __name__ == '__main__':
  seed('HelloCountSort')
  vis = Visualizer('Radix Sort: LSD')
  while True:
    kind = 1000                                # 0~999 사이의 수 생성
    count = randint(30, 150)                   # 30개~150개 를 생성
    print(f'Creating data: {kind=} {count=}')
    begin = 500 + randint(1, 1000)             # 시작위치 랜덤하게 결정
    array = list(map(lambda x: x%kind, numbers[begin:begin+count]))
    vis.setup(vis.get_main_module())
    main()
    vis.draw()
    again = vis.end()
    if not again: break
