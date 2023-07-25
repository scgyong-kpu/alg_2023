class Hello:
  pass # Python 에서는 줄을 비워 두면 안될 때 pass 를 써야 한다.

print('-- 타입 이름에 괄호를 열고 닫으면 해당 타입의 객체를 생성하는 것이다')
print('   함수 호출과 문법이 동일하다 --')
h = Hello() # 함수 호출과 문법이 동일하다

def func():
  return 'This is a string'

flags = [ True, False, True ]
for flag in flags:
  todo = Hello if flag else func
  obj = todo() # 함수 호출과 객체 생성이 동일한 문법 구조에 의해 일어난다
  print('flag 값은:', flag, '이번에 얻은 것은:', obj)
