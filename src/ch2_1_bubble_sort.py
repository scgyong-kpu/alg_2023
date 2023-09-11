from data_unsorted import numbers
# from data_unsorted_a_lot import numbers
# numbers = numbers[:1000]

from random import randint, seed

def main():
  print(array)

if __name__ == '__main__':
  seed('Hello') # 'Hello' 를 seed 로 고정하여 randint 가 항상 같은 결과가 나오게 한다
  count = randint(10, 30)
  array = numbers[:count]
  main()
