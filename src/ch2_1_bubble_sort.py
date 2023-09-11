from data_unsorted import numbers
# from data_unsorted_a_lot import numbers
# numbers = numbers[:1000]

from random import randint, seed
from vis import BubbleSortVisualizer as Visualizer
# from vis import Dummy as Visualizer

def main():
  print('before:', array)
  count = len(array)
  for end in range(count - 1, 0, -1):
    for i in range(end):
      vis.compare(i, i+1)
      if array[i] > array[i+1]:
        vis.swap(i, i+1)        
        array[i], array[i+1] = array[i+1], array[i]
    vis.bubble_end(end)
  vis.bubble_end(0)
  print('after :', array)

''' Bubble 을 2중루프로 돌아 보면, 다음과 같이 출력된다.
before: [71, 30, 18, 51, 77, 37, 3, 93, 90, 48]
after : [3, 18, 30, 37, 48, 51, 71, 77, 90, 93]
'''

if __name__ == '__main__':
  seed('Hello') # 'Hello' 를 seed 로 고정하여 randint 가 항상 같은 결과가 나오게 한다
  vis = Visualizer('Bubble Sort')
  while True:
    count = randint(10, 30)
    array = numbers[:count]
    vis.setup(vis.get_main_module())
    main()
    vis.draw()

    # R key 를 누르면 다음 case 가 실행된다
    again = vis.end()
    if not again: break