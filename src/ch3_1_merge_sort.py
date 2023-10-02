# from vis import MergeSortVisualizer as Visualizer
# from vis import Dummy as Visualizer
from time import time
from random import randint, seed, shuffle
# from data_unsorted import numbers
from data_unsorted_a_lot import numbers

def main():
  # print('before:', array)
  count = len(array)
  mergeSort(0, count-1)       # 전체 팀을 정렬한다
  # print('after :', array)

def mergeSort(left, right): #right=inclusive
  if right <= left: return    # 정렬할 선수들이 없거나 한병뿐이면 할 필요가 없다
  if right == left + 1:
    # vis.compare(left, right)
    if array[left] > array[right]:
      # vis.swap(left, right)
      array[left], array[right] = array[right], array[left]
      return
  mid = (left + right) // 2   # 목록을 절반으로 나눈다
  # vis.push(left, mid, right)
  mergeSort(left, mid)        # 왼쪽 팀을 정렬한다
  mergeSort(mid+1, right)     # 오른쪽 팀을 정렬한다
  merge(left, mid+1, right)   # 두 팀을 합병한다
  # vis.pop()

def merge(left, right, end): # 왼쪽은 [left~right-1], 오른쪽은 [right~end] 이고 end 는 inclusive 이다
  merged = []                        # 임시 저장할 정렬 결과 목록을 준비한다. 
  # vis.start_merge(merged, False, left)
  l, r = left, right                 # 각 팀의 첫번째 선수가 입장한다
  while l < right and r <= end:      # 한 팀이라도 팀원이 소진되면 그만한다
    # vis.compare(l, r)
    if array[l] <= array[r]:         # 두 팀에서 출전한 선수끼리 겨룬다
      merged.append(array[l])        # 왼쪽팀 선수가 졌으므로 결과 목록에 추가된다
      # vis.add_to_merged(l, True)
      l += 1                         # 왼쪽팀은 다음 선수가 나온다
    else:
      merged.append(array[r])        # 오른쪽팀 선수가 졌으므로 결과 목록에 추가된다
      # vis.add_to_merged(r, False)
      r += 1                         # 오른쪽팀은 다음 선수가 나온다

  while l < right:                   # 왼쪽팀에 선수가 남아 있다면
    merged.append(array[l])          # 왼쪽팀 선수들은 모두 목록에 추가된다
    # vis.add_to_merged(l, True)
    l += 1
  while r <= end:                    # 오른쪽팀에 선수가 남아 있다면
    merged.append(array[r])          # 오른쪽팀 선수들은 모두 목록에 추가된다
    # vis.add_to_merged(r, False)
    r += 1

  # vis.end_merge()

  array[left:end+1] = merged # 임시 저장되어 있던 결과 목록에 있는 선수들을
                             # 원래의 배열에 옮겨 담는다
  # l = left
  # for n in merged:         # 임시 저장되어 있던 결과 목록에 있는 선수들을
  #   array[l] = n           # 원래의 배열에 옮겨 담는다
  #   l += 1

    # vis.erase_merged()

''' 성능 측정
count=100     elapsed=0.000 0.000 0.000
count=1000    elapsed=0.003 0.003 0.003
count=2000    elapsed=0.006 0.006 0.004
count=3000    elapsed=0.009 0.009 0.007
count=4000    elapsed=0.013 0.012 0.010
count=5000    elapsed=0.016 0.016 0.013
count=6000    elapsed=0.020 0.019 0.016
count=7000    elapsed=0.024 0.021 0.019
count=8000    elapsed=0.026 0.024 0.022
count=9000    elapsed=0.031 0.027 0.025
count=10000   elapsed=0.035 0.030 0.029
count=15000   elapsed=0.054 0.045 0.043
count=20000   elapsed=0.074 0.065 0.061
count=30000   elapsed=0.116 0.095 0.091
count=40000   elapsed=0.159 0.134 0.134
count=50000   elapsed=0.196 0.172 0.157
count=100000  elapsed=0.442 0.377 0.368
count=200000  elapsed=0.898 0.805 0.763
count=300000  elapsed=1.439 1.243 1.186
count=400000  elapsed=2.111 1.679 1.656
count=500000  elapsed=2.717 2.115 2.049
count=1000000 elapsed=5.684 4.362 4.287
count=100     elapsed=0.000
count=1000    elapsed=0.003
count=2000    elapsed=0.004
count=3000    elapsed=0.007
count=4000    elapsed=0.010
count=5000    elapsed=0.013
count=6000    elapsed=0.016
count=7000    elapsed=0.019
count=8000    elapsed=0.022
count=9000    elapsed=0.025
count=10000   elapsed=0.029
count=15000   elapsed=0.043
count=20000   elapsed=0.061
count=30000   elapsed=0.091
count=40000   elapsed=0.134
count=50000   elapsed=0.157
count=100000  elapsed=0.368
count=200000  elapsed=0.763
count=300000  elapsed=1.186
count=400000  elapsed=1.656
count=500000  elapsed=2.049
count=1000000 elapsed=4.287
'''
if __name__ == '__main__':
  seed('Hello')

  counts = [ 
    100, 1000, 2000, 3000, 4000, 5000, 
    6000, 7000, 8000, 9000, 10000, 15000, 
    20000, 30000, 40000, 50000,
    100000, 200000, 300000, 400000, 500000,
    1000000, 
  ]
  for count in counts:
    array = numbers[:count]
    shuffle(array)
    # print('before:', array)
    startedOn = time()
    main()
    elapsed = time() - startedOn
    # print('after: ', array)
    print(f'{count=:<7d} {elapsed=:.3f}')
  exit() 

  vis = Visualizer('Merge Sort')
  while True:
    count = randint(20, 40)
    array = [ randint(1, 99) for _ in range(count) ]
    vis.setup(vis.get_main_module())
    main()
    vis.draw()
    again = vis.end()
    if not again: break

