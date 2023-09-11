squares_1 = []
for i in range(10):
  squares_1.append(i ** 2)

print('-- 빈 배열을 준비하고 루프를 돌면서 초기화하기 --')
print(f'{squares_1=}')

squares_2 = [ i ** 2 for i in range(10) ]

print('\n-- List Comprehension 이용하기 --')
print(f'{squares_2=}')
