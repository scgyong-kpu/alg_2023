from vis import BinarySearchVisualizer as Visualizer
# from vis import Dummy as Visualizer

def search(array, to_find):
  left, right = 0, len(array) - 1
  vis.mark(left, right)
  while left <= right:
    mid = (left + right) // 2
    vis.compare(mid)
    if array[mid] == to_find:
      vis.update()
      return mid
    if array[mid] < to_find:
      left = mid + 1
    else:
      right = mid - 1
    vis.mark(left, right)

  vis.compare(-1)
  return -1

if __name__ == '__main__':
  vis = Visualizer('Find Max Value')
  while True:
    # array = [10, 20, 25, 35, 45, 55, 60, 75, 85, 90]
    from random import randrange
    array = sorted([ randrange(100) for _ in range(randrange(10, 30)) ])
    # to_find = 85
    to_find = randrange(100) if randrange(2) == 0 else array[randrange(len(array))]
    vis.setup(vis.get_main_module())
    at = search(array, to_find)
    if at >= 0:
      print(f'Found {to_find} {at=}')
    else:
      print(f'{to_find} Not Found')
    again = vis.end()
    if not again: break


