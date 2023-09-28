from vis import MergeSortVisualizer as Visualizer
# from vis import Dummy as Visualizer
from time import time
from random import randint, seed, shuffle

def main():
  print('before:', array)
  count = len(array)
  mid = count // 2
  array[0:mid] = sorted(array[0:mid]) # 왼쪽 팀 선수들이 약한 순서대로 정렬되어 있다고 가정한다
  array[mid:] = sorted(array[mid:])   # 오른쪽 팀 선수들도 약한 순서대로 정렬되어 있다고 가정한다

  vis.push(0, mid-1, count-1)
  merge(0, mid, count-1)
  print('after :', array)

def merge(left, right, end): # 왼쪽은 [left~right-1], 오른쪽은 [right~end] 이고 end 는 inclusive 이다
  merged = []                        # 임시 저장할 정렬 결과 목록을 준비한다. 
  vis.start_merge(merged, False, left)
  l, r = left, right                 # 각 팀의 첫번째 선수가 입장한다
  while l < right and r <= end:      # 한 팀이라도 팀원이 소진되면 그만한다
    vis.compare(l, r)
    if array[l] <= array[r]:         # 두 팀에서 출전한 선수끼리 겨룬다
      merged.append(array[l])        # 왼쪽팀 선수가 졌으므로 결과 목록에 추가된다
      vis.add_to_merged(l, True)
      l += 1                         # 왼쪽팀은 다음 선수가 나온다
    else:
      merged.append(array[r])        # 오른쪽팀 선수가 졌으므로 결과 목록에 추가된다
      vis.add_to_merged(r, False)
      r += 1                         # 오른쪽팀은 다음 선수가 나온다

  while l < right:                   # 왼쪽팀에 선수가 남아 있다면
    merged.append(array[l])          # 왼쪽팀 선수들은 모두 목록에 추가된다
    vis.add_to_merged(l, True)
    l += 1
  while r <= end:                    # 오른쪽팀에 선수가 남아 있다면
    merged.append(array[r])          # 오른쪽팀 선수들은 모두 목록에 추가된다
    vis.add_to_merged(r, False)
    r += 1

  vis.end_merge()

  l = left
  for n in merged:         # 임시 저장되어 있던 결과 목록에 있는 선수들을
    array[l] = n           # 원래의 배열에 옮겨 담는다
    l += 1
    # vis.erase_merged()

  vis.pop()

if __name__ == '__main__':
  seed('Hello')
  vis = Visualizer('Merge Sort')
  while True:
    count = randint(20, 40)
    array = [ randint(1, 99) for _ in range(count) ]
    vis.setup(vis.get_main_module())
    main()
    vis.draw()
    again = vis.end()
    if not again: break

