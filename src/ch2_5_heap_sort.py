from data_unsorted import numbers
# from data_unsorted_a_lot import numbers
from random import randint, seed, shuffle
from vis import HeapSortVisualizer as Visualizer
# from vis import Dummy as Visualizer
from time import time

def heapify(root, size):
  lc = root * 2 + 1      # lc = Left Child 
  if lc >= size: return  # child 가 없다는 의미이다
  child = lc
  rc = root * 2 + 2      # rc = Right Child
  if rc < size:          # lc 만 있을 수도 있지만, rc 도 있다면
    vis.compare(rc, lc)
    if array[rc] > array[lc]: # lc 와 rc 중 큰 것을 비교하여
      child = rc              # child 에 담는다

  vis.compare(root, child)
  if array[root] < array[child]:  # parent 와 child 중에 어느것이 큰지 비교하여
    vis.swap(root, child)
    array[root], array[child] = array[child], array[root] # 필요시 교체한다
    heapify(child, size) # 교체되어 내려간 child 를 새로운 parent 로 하여 재귀 호출한다

def main():
  print('before:', array)
  count = len(array)
  vis.build_tree()

  last_parent_index = count // 2 - 1
  for n in range(last_parent_index, -1, -1):
    vis.set_root(n)
    heapify(n, count)

  last_sort_index = count - 1
  while last_sort_index > 0:
    vis.compare(0, last_sort_index)
    vis.swap(0, last_sort_index)
    # 첫번째와 마지막의 원소를 교환한다
    array[0], array[last_sort_index] = array[last_sort_index], array[0] 
    vis.set_tree_size(last_sort_index)
    heapify(0, last_sort_index) # Root 에 새로운 녀석이 들어왔으므로 Heap 이 되기 위해 내린다
    last_sort_index -= 1

  vis.set_tree_size(0)
  print('after :', array)

''' 성능측정
count=   100 elapsed=  0.000
count=  1000 elapsed=  0.004
count=  2000 elapsed=  0.008
count=  3000 elapsed=  0.014
count=  4000 elapsed=  0.019
count=  5000 elapsed=  0.024
count=  6000 elapsed=  0.030
count=  7000 elapsed=  0.035
count=  8000 elapsed=  0.041
count=  9000 elapsed=  0.051
count= 10000 elapsed=  0.056
count= 15000 elapsed=  0.081
count= 20000 elapsed=  0.128
count= 30000 elapsed=  0.173
count= 40000 elapsed=  0.246
count= 50000 elapsed=  0.326
count=100000 elapsed=  0.695
count=200000 elapsed=  1.599
count=300000 elapsed=  2.575
count=400000 elapsed=  3.371
count=500000 elapsed=  4.321
nlogn vs n^1.5
y = 3xlog(2,x),  y=x^1.5 , x from 1 to 1000
https://www.wolframalpha.com/input?i=y+%3D+3xlog%282%2Cx%29%2C++y%3Dx%5E1.5+%2C+x+from+1+to+1000
'''

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
