from vis import BinsVisualizer as Visualizer
from random import randint

class Bin:                                     # Bin 자료구조를 정의하는 클래스
  Size = 100                                   # Bin 의 크기는 100 이다
  def __init__(self):
    self.free = Bin.Size                       # 생성시 빈 공간
    self.objs = []                             # 채운 물건들
  def hasSize(self, size):                     # size 만한 물건이 들어갈 수 있는지 확인한다
    return self.free >= size
  def add(self, size):                         # size 만한 물건을 넣는다
    if not self.hasSize(size): return False
    self.objs.append(size)                     # 물건 배열에 추가하고
    self.free -= size                          # 빈공간을 줄인다
    return True
  def __repr__(self):                          # 문자열로 변환될 필요가 있을 때에는
    return f'{self.objs}({self.free})'         # 물건들의 내용과 빈 공간을 출력한다

class BinPacking:                              # Bin Packing 알고리즘을 구현하는 클래스
  FIRST_FIT, NEXT_FIT, BEST_FIT, WORST_FIT, FIT_COUNT = range(5)
  def __init__(self, strategy, objs):
    self.strategy = strategy                   # 어떤 핏인지 저장
    self.bins = []                             # Bin 들의 배열
    self.objs = objs[:]   # 입력된 물건들을 복사해서 저장해 둔다. 하나씩 뽑아 쓸 예정이므로 대입하지 않고 복사한다.

  def main(self):
    vis.add(None)
    bin = Bin()              # 새로운 Bin 을 만들고
    obj = self.objs.pop(0)   # 하나를 뽑아서
    bin.add(obj)             # bin 에 넣은뒤
    self.bins.append(bin)    # bins 에 추가한다
    vis.add(bin)
    vis.draw()

vis = Visualizer('Bin Packing')
fit = BinPacking.FIRST_FIT
gen = True
while True:
  if gen:
    objs = [ randint(1, 75) for _ in range(100) ] # 1~75 까지의 랜덤한 숫자 100 개를 만들어둔다
    print(objs)
    gen = False
  print(f'Fit = {fit}')
  bp = BinPacking(fit, objs)                      # 선택된 fit 과 숫자들을 가지고 알고리즘 객체 생성한다
  vis.setup(bp)
  bp.main()                                       # 알고리즘을 진행한다
  again = vis.end()
  if not again: break
  if vis.restart_lshift:                          # LShift+R 이면 새로운 물건들로 동일 fit
    gen = True
  else:                                           # 그냥 R 이면 다음 fit 으로 진행
    fit = (fit + 1) % BinPacking.FIT_COUNT
