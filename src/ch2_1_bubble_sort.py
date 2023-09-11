# from data_unsorted import numbers
from data_unsorted_a_lot import numbers
# numbers = numbers[:1000]

from random import randint, seed, shuffle
from time import time

# from vis import BubbleSortVisualizer as Visualizer
from vis import Dummy as Visualizer

def main():
  print('before:', array)
  count = len(array)
  end = count - 1
  while end > 0:
    last = 1
    for i in range(end):
      vis.compare(i, i+1)
      if array[i] > array[i+1]:
        vis.swap(i, i+1)        
        array[i], array[i+1] = array[i+1], array[i]
        last = i + 1
    end = last - 1
    vis.bubble_end(last)
  vis.bubble_end(0)
  print('after :', array)

''' 
Dummy Visualizer 를 썼을 때
count=100 elapsed=0.005
count=1000 elapsed=0.437
count=2000 elapsed=1.794
count=3000 elapsed=4.001
count=4000 elapsed=7.062
'''

if __name__ == '__main__':
  seed('Hello') # 'Hello' 를 seed 로 고정하여 randint 가 항상 같은 결과가 나오게 한다
  vis = Visualizer('Bubble Sort')

  result = dict()
  counts = [ 100, 1000, 2000, 3000, 4000 ] #, 5000, 6000, 7000, 8000, 9000, 10000, 15000, 20000 ]
  for count in counts:
    array = numbers[:count]
    shuffle(array)
    startedOn = time()
    main()
    elapsed = time() - startedOn
    print(f'{count=} {elapsed=:.3f}')
    result[count] = elapsed

  for count in result.keys():
    elapsed = result[count]
    print(f'{count=} {elapsed=:.3f}')

  exit() 

  while True:
    count = randint(10, 30)
    array = numbers[:count]
    vis.setup(vis.get_main_module())
    main()
    vis.draw()

    # R key 를 누르면 다음 case 가 실행된다
    again = vis.end()
    if not again: break
