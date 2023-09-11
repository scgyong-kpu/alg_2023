from data_unsorted import numbers
# from data_unsorted_a_lot import numbers
# numbers = numbers[:1000]

from random import randint, seed, shuffle
from time import time

from vis import BubbleSortVisualizer as Visualizer
# from vis import Dummy as Visualizer

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
* Dummy Visualizer 를 썼을 때
count=100 elapsed=0.005
count=1000 elapsed=0.437
count=2000 elapsed=1.794
count=3000 elapsed=4.001
count=4000 elapsed=7.062

* Visualizer 코드를 완전히 제거했을 때
count=100 elapsed=0.001
count=1000 elapsed=0.094
count=2000 elapsed=0.375
count=3000 elapsed=0.827
count=4000 elapsed=1.552
count=5000 elapsed=2.413
count=6000 elapsed=3.427
count=7000 elapsed=4.731
count=8000 elapsed=5.967
count=9000 elapsed=7.760
count=10000 elapsed=9.621
count=15000 elapsed=21.400
count=20000 elapsed=39.334
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
