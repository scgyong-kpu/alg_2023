squares_1 = []
for i in range(10):
  squares_1.append(i ** 2)

print('-- 빈 배열을 준비하고 루프를 돌면서 초기화하기 --')
print(f'{squares_1=}')

squares_2 = [ i ** 2 for i in range(10) ]

print('\n-- List Comprehension 이용하기 --')
print(f'{squares_2=}')

def func(n): return n ** 2

squares_3 = map(func, range(10))
print('\n-- map 이용하기 --')
print(f'{squares_3=}')

for sq in squares_3:
  print(sq, end=', ')
print()

squares_4 = list(map(func, range(10)))
print('\n-- map 결과는 실제 배열과는 다르다 (배열을 위한 메모리가 할당되지 않으므로 ')
print('   꼭 list 형태가 필요할 경우 변환해서 사용한다.) --')
print(f'{squares_4=}')

squares_5 = list(map(lambda x: x**2, range(10)))
print('\n-- map 에 전달할 함수는 lambda 키워드를 써서 인라인으로 작성 가능하다 ')
print(f'{squares_5=}')

from random import randrange
dim3 = [[[] for _ in range(3)] for _ in range(4)] # 3열x4행 의 12개의 빈 배열 준비
print(f'\nbefore: {dim3=}')
for i in range(26):
  ch = chr(ord('a')+i)
  x, y = randrange(3), randrange(4)  # 12개 배열 중 하나를 랜덤하게 고름
  dim3[y][x].append(ch) # 고른 배열에다가 이번 글자를 추가함
print(f' after: {dim3=}')