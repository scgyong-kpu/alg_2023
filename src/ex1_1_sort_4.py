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
  print(f'after : {arr}')

def select_sort(arr):
  print('-' * 60)
  print('Selection Sort')
  print(f'before: {arr}')
  print(f'after : {arr}')

def insert_sort(arr):
  print('-' * 60)
  print('Insertion Sort')
  print(f'before: {arr}')
  print(f'after : {arr}')

def shell_sort(arr):
  print('-' * 60)
  print('Shell Sort')
  print(f'before: {arr}')
  print(f'after : {arr}')

def main():
  bubble_sort(array[:])
  insert_sort(array[:])
  select_sort(array[:])
  shell_sort(array[:])

if __name__ == '__main__':
  main()

