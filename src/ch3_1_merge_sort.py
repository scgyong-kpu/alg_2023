from vis import MergeSortVisualizer as Visualizer
# from vis import Dummy as Visualizer
from time import time
from random import randint, seed, shuffle

def main():
  print('before:', array)
  count = len(array)
  mergeSort(0, count-1)       # 전체 팀을 정렬한다
  print('after :', array)

def mergeSort(left, right): #right=inclusive
  if right <= left: return    # 정렬할 선수들이 없거나 한병뿐이면 할 필요가 없다
  mid = (left + right) // 2   # 목록을 절반으로 나눈다
  vis.push(left, mid, right)
  mergeSort(left, mid)        # 왼쪽 팀을 정렬한다
  mergeSort(mid+1, right)     # 오른쪽 팀을 정렬한다
  merge(left, mid+1, right)   # 두 팀을 합병한다
  vis.pop()

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

