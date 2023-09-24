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
  for n in range(last_parent_index, last_parent_index - 2, -1):
    vis.set_root(n)
    heapify(n, count)

  print('after :', array)


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
