# from data_unsorted import numbers
# from data_unsorted_a_lot import numbers
from vis import QuickSortVisualizer as Visualizer
# from vis import Dummy as Visualizer
from time import time
from random import randint, seed, shuffle

def main():
  print('before:', array)
  count = len(array)
  vis.push(0, count-1)
  pivot = partition(0, count-1)
  vis.set_pivot(pivot)
  print('after :', array)

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

    if p >= q: break      # p 와 q 가 만났다면 더이상 swap 은 없다

    vis.set_left(p)
    vis.set_right(q)
    vis.swap(p, q)

    array[p], array[q] = array[q], array[p] 
    # p 는 pivot 보다 큰 값의 위치, q 는 pivot 보다 작은 값의 위치이므로 둘을 바꾼다
  
  if left != q: # pivot 값보다 작은 것이 하나도 없다면 left 는 q 와 같다.
    vis.swap(left, q, True)
    array[left], array[q] = array[q], array[left] # pivot 값의 위치를 확정시킨다

  return q  # 결정된 pivot 의 위치를 리턴한다

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

