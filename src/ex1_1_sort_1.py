array = [
       46,      82,      21,      58,      22,      54,      71,     215,      99,     227, 
       73,      24,      17,      44,     244,      78,      25,      66,      47,       3, 
       87,      33,     312,     242,      42,      61,     348,     346,      98,      92, 
       83,     100,      94,      40,       5,     458,     364,      26,      64,      35, 
       90,     489,      72,     504,      88,      97,     226,     218,     186,      68, 
]

def sort_bubble(arr):
  print('-' * 60)
  print(f'before: {arr}')
  print(f'after : {arr}')

def sort_select(arr):
  print('-' * 60)
  print(f'before: {arr}')
  print(f'after : {arr}')

def sort_insert(arr):
  print('-' * 60)
  print(f'before: {arr}')
  print(f'after : {arr}')

def sort_shell(arr):
  print('-' * 60)
  print(f'before: {arr}')
  print(f'after : {arr}')

def main():
  sort_bubble(array[:])
  sort_insert(array[:])
  sort_select(array[:])
  sort_shell(array[:])

if __name__ == '__main__':
  main()

