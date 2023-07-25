# print('-- % 연산자를 사용하여 C printf 스타일의 포매팅을 할 수 있다 --')
# print('-- format() 을 이용한 포매팅을 할 수 있다 --')
print('-- f-string 을 이용한 포매팅을 할 수 있다 --')
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
  # print('{:>15} : {:4} : {:05.2f}'.format(name, age, score))
  # print('{:^15} : {:4} : {:05.2}'.format(name, age, score))
  # > 는 오른쪽 정렬 < 는 왼쪽 정렬, ^ 는 가운데 정렬
  print(f'{name:^15} : {age:4} : {score:05.2f}')
  # 앞에서 f-string 을 볼 기회가 여럿 있었죠?

print('\n-- 그 외에도 여러가지 포매팅 --')
david = {'name':'David', 'age':22, 'score':3.866666}
print('%(name)-15s : %(age)4s : %(score)05.2f' % david)
# % 와 dict 를 이용한 포매팅.

# Python 에서는 Class 정의를 간단히 할 수 있다. 
# 멤버변수는 자유롭게 추가되므로 클래스 이름만 등록하는 수준으로도 가능하다
class Student: pass 

student = Student()
student.name = 'David'
student.age = 22
student.score = 3.866666

# 객체 속성을 출력하고자 할 때. 두 가지 방법이 장단점이 있다
print('{p.name:^15s} : {p.age:4} : {p.score:.2f}'.format(p=student))
print(f'{student.name:^15s} : {student.age:4} : {student.score:.2f}')

