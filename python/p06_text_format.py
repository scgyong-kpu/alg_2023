#print('-- % 연산자를 사용하여 C printf 스타일의 포매팅을 할 수 있다 --')
print('-- format() 을 이용한 포매팅을 할 수 있다 --')
students = [
  ( 'David', 22, (4.3 + 4.0 + 3.3) / 3 ),
  ( 'John Abdul', 25, (2.3 + 2.3 + 3.3) / 3 ),
  ( 'Chuck Norris', 124, (1.3 + 1.0 + 3.0) / 3 ),
  ( 'Karl Marx', 21, (3.3 + 2.0 + 4.3) / 3 ),
]
# name, age, score = students[0]
# print(name, age, score)

for st in students:
  name, age, score = st
  # print('%-15s : %4d : %05.2f' % (name, age, score))
  print('{:>15} : {:4} : {:05.2f}'.format(name, age, score))
  # print('{:^15} : {:4} : {:05.2}'.format(name, age, score))
  # > 는 오른쪽 정렬 < 는 왼쪽 정렬, ^ 는 가운데 정렬


