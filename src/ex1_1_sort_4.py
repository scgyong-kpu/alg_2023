array = [
       46,      82,      21,      58,      22,      54,      71,     215,      99,     227, 
       73,      24,      17,      44,     244,      78,      25,      66,      47,       3, 
       87,      33,     312,     242,      42,      61,     348,     346,      98,      92, 
       83,     100,      94,      40,       5,     458,     364,      26,      64,      35, 
       90,     489,      72,     504,      88,      97,     226,     218,     186,      68, 
]

def bubble_sort(arr):
  print('-' * 60)
  print('Bubble Sort')
  print(f'before: {arr}')
  count = len(arr)
  for a in range(count - 1):
    for b in range(count - 1 - a):
      if ??: ???

  print(f'after : {arr}')

def select_sort(arr):
  print('-' * 60)
  print('Selection Sort')
  print(f'before: {arr}')
  while ???: # N 개의 최소값을 찾는다
    while ???: # 최소값이 어디 있는지 알아낸다
      pass
    #바꾼다

  print(f'after : {arr}')

def insert_sort(arr):
  print('-' * 60)
  print('Insertion Sort')
  print(f'before: {arr}')
  while ???: # 1st loop: 1(두번째)부터 끝까지 주인공 시켜준다
    while ???: # 2nd loop: 주인공을 가능한곳까지 왼쪽으로 보낸다
  print(f'after : {arr}')

def shell_sort(arr):
  print('-' * 60)
  print('Shell Sort')
  print(f'before: {arr}')
  while ???: # 1st loop: 갭을 점점 줄여서 1까지 돌린다
    while ???: # 2nd loop: 갭부터 끝까지 주인공 시켜준다
      while ???: # 주인공을 가능한곳까지 왼쪽으로 보낸다
  print(f'after : {arr}')

def main():
  bubble_sort(array[:])
  insert_sort(array[:])
  select_sort(array[:])
  shell_sort(array[:25])

if __name__ == '__main__':
  main()

