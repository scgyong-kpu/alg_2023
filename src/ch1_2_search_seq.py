from vis import SearchVisualizer as Visualizer
# from vis import Dummy as Visualizer

def search(array, to_find):
  for i in range(len(array)):
    vis.compare(i)
    if to_find == array[i]:
      at = i
      vis.update()
      return at
  vis.compare(-1)
  return -1

if __name__ == '__main__':
  vis = Visualizer('Find Max Value')
  while True:
    # array = [45,20,35,60,55,10,90,85,25,75]
    from random import randrange
    array = [ randrange(100) for _ in range(randrange(10, 30)) ]
    # to_find = 85
    to_find = randrange(100) if randrange(2) == 0 else array[randrange(len(array))]
    vis.setup(vis.get_main_module())
    at = search(array, to_find)
    print(f'Found {to_find} {at=}')
    again = vis.end()
    if not again: break


