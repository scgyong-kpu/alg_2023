from ch1_4_1_oxford_words import five_letters
from random import randint
from math import sqrt

count = 500           # 몇 개의 도시를 만들건지
coord_start = 1       # 랜덤 적용할 x및 y좌표 시작점
coord_end_x = 1599    # 랜덤 적용할 x좌표 끝점
coord_end_y = 899     # 랜덤 적용할 y좌표 끝점
MIN_DIST = 30         # 최소거리. 생성된 도시들 중 이 거리 이내의 도시가 있으면 다시 만든다

fives = five_letters[:count] # 5글자 이름 단어들 중 일부만 추린다
coords = []           # 최소거리 판단을 위해 생성된 좌표들을 모두 기록한다

def distance(c1, c2):
  dx, dy = c1[0] - c2[0], c1[1] - c2[1]
  return sqrt(dx ** 2 + dy ** 2)

def make_coord():
  while True:
    close_coord_found = False
    x, y = randint(coord_start, coord_end_x), randint(coord_start, coord_end_y)
    for co in coords: # 기존 생성된 좌표들 중 최소거리 이내인 것이 있는지 찾는다
      dist = distance((x, y), co)
      # print(dist)
      if dist < MIN_DIST:
        # print(dist)
        close_coord_found = True   # 찾았으면 다시 생성하러 간다
        break
    if not close_coord_found:
      break
  return x, y


for word in fives:
  name = word.capitalize()
  x, y = make_coord()
  coords.append((x, y))
  print(f'  City("{name}", {x}, {y}),')
