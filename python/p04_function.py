def func():
  print('This is a function')

print('\n--함수는 한번 정의해 놓고 여러 번 호출하기 위해서도 쓴다--')
func()
func()

print('\n--비슷한 것을 여러번 할거라면 공통적인 것을 함수로 정의하고')
print('--달라지는 것은 함수의 인자로 전달한다. 이것을 인수분해 라고 부르기로 한다--')

def function(arg):
  print(' = function with (', arg, ')')

function('hello')
function('world')

print('\n--함수 안에서 처음 사용한 변수는 local 이므로 함수의 종료와 함께 소멸한다--')

value = 123 # 외부 (global) 변수의 선언 및 대입이다.

def some():
  value = 456 # 이 값은 some() 내부에서만 사용하는 변수 value 에다 대입한 것이다
  print('in some(), value=', value) # 쓴 다음 읽으면 내부 변수를 참조한다.
  # some() 내부에서 선언한 value 는 함수의 종료와 함께 소멸한다

def other():
  print('in other(), value=', value) # 읽기만 하면 외부에서 정의한 변수 value 를 참조한다

some()
other()

# 아래 코드를 풀고 실행해 보면 에러가 난다. 외부 변수를 읽은 다음 쓰는 것은 안 된다
# def another():
#   print(value)
#   value = 10
# another()

def yet_another():
  global value
  print('in yet_another(), reading global:', value)
  value += 20
  print('in yet_another(), after writing global:', value)

print('\n-- 함수 내에서 외부정의 변수를 읽고 쓰려면 global 로 선언해야 한다 --')
yet_another()

