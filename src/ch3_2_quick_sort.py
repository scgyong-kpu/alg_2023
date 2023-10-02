from data_unsorted import numbers
# from data_unsorted_a_lot import numbers
from vis import QuickSortVisualizer as Visualizer
# from vis import Dummy as Visualizer
from time import time
from random import randint, seed, shuffle

def main():
  print('before:', array)

  count = len(array)
  quickSort(0, count-1)
  insertionSort(0, count-1)

  print('after :', array)

def quickSort(left, right): #q=inclusive
  if left == right: vis.fix(left)  # 정렬 대상이 하나뿐이라면 확정해도 좋다
  # if left >= right: return         # 정렬할 것이 없으면 할 일이 없다
  if right < left + 4:
    return
  vis.push(left, right)
  pivot = partition(left, right)   # pivot 위치를 결정해 온다
  vis.set_pivot(pivot)
  quickSort(left, pivot-1)  # pivot 보다 왼쪽 그룹을 다시 quickSort 한다
  quickSort(pivot+1, right) # pivot 보다 오른쪽 그룹을 다시 quickSort 한다
  vis.pop()

def insertionSort(left, right): #right=inclusive
  for i in range(left + 1, right + 1):
    v = array[i]
    vis.mark_end(i, v)
    j = i - 1
    while j >= left and array[j] > v:
      vis.shift(j)
      array[j+1] = array[j]
      j -= 1
    vis.insert(i, j+1)
    array[j+1] = v

def partition(left, right):

  pi = left               # pi = Pivot Index
  pivot = array[pi]       # pivot = value

  p, q = left, right + 1  # 후보선수들 출전준비

  while True:             # p 와 q 가 역전할때까지
    while True:           # 왼쪽에서 pivot 보다 큰 값을 찾을때까지
      p += 1
      vis.set_p(p)
      if q < p: break
      if p <= right: vis.compare(pi, p)
      if p > right or array[p] >= pivot: break 
      # 왼쪽에서 pivot 보다 큰 값을 찾았다

      if p <= right: vis.set_left(p)

    while True:           # 오른쪽에서 pivot 보다 작은 값을 찾을때까지
      q -= 1
      vis.set_q(q)
      if q < p: break
      if q >= left: vis.compare(pi, q)
      if q < left or array[q] <= pivot: break
      # 오른쪽에서 pivot 보다 작은 값을 찾았다

      if q >= left: vis.set_right(q)

    if p >= q: break      # p 와 q 가 만날때까지 계속 진행한다

    vis.set_left(p)
    vis.set_right(q)
    vis.swap(p, q)
    array[p], array[q] = array[q], array[p] 
    # 이제 p 이하에는 pivot 보다 작은 값만, q 이상에는 pivot 보다 큰 값만 있다

  # pivot 값의 위치를 확정시킨다
  # pivot 값은 왼쪽 그룹 중에 가장 큰 값이므로 q 위치로 옮긴다
  # left 가 q 와 같다면 pivot 보다 작은것이 하나도 없다는 뜻이므로 옮길 필요가 없다
  if left != q:
    vis.swap(left, q, True)
    array[left], array[q] = array[q], array[left]

  return q  # 결정된 pivot 의 위치를 리턴한다

''' 성능 측정
count=100     elapsed=0.000
count=1000    elapsed=0.002
count=2000    elapsed=0.004
count=3000    elapsed=0.006
count=4000    elapsed=0.009
count=5000    elapsed=0.010
count=6000    elapsed=0.012
count=7000    elapsed=0.014
count=8000    elapsed=0.016
count=9000    elapsed=0.018
count=10000   elapsed=0.022
count=15000   elapsed=0.034
count=20000   elapsed=0.048
count=30000   elapsed=0.081
count=40000   elapsed=0.104
count=50000   elapsed=0.124
count=100000  elapsed=0.267
count=200000  elapsed=0.617
count=300000  elapsed=0.936
count=400000  elapsed=1.256
count=500000  elapsed=1.792
count=1000000 elapsed=3.658
'''

if __name__ == '__main__':
  seed('Hello')
  vis = Visualizer('Quick Sort')
  while True:
    count = randint(20, 40)
    array = [ randint(1, 99) for _ in range(count) ]
    vis.setup(vis.get_main_module())
    main()
    vis.draw()
    again = vis.end()
    if not again: break

