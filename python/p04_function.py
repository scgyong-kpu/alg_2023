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

print('\n-- 함수의 인자를 전달하는 방법은 여러가지가 있다. tuple/list 사용가능 --')

def func_with_arg(x, y):
  print('point=', x, y)

func_with_arg(10, 20) # 직접 여러 개로 전달
arg_tuple = 12, 23
func_with_arg(*arg_tuple) # 그냥 (arg_tuple) 로 쓰면 첫번째 인자로 tuple 을 넘긴 것이 된다
arg_list = [34, 45]
func_with_arg(*arg_list) # tuple 또는 list 에 담은 다음 * 로 내용물을 펼쳐서 전달할 수 있다

print('\n-- Default Argument & Keyword Argument --')
def func_with_def_arg(name, age, score=0, method=None, msg=''):
  if method == None:
    method = 'the-default-method'
  print('name=', name, 'age=', age, 'I got:', score, method, f"[{msg}]") # f-string 은 뒤에 다룹니다

func_with_def_arg('hello', 20)
func_with_def_arg('world', 22, 4.5, 'get')
func_with_def_arg('world', 22, 'get')
func_with_def_arg('world', 22, method='get')

arg_dict = { 'name': 'KKY', 'score': 123, 'msg': 'Hello,world', 'age':30 }
func_with_def_arg(**arg_dict) # dict 형태로 함수 인자로 전달 가능

print('\n-- 임의로 전달 후 받는 쪽에서 list 나 dict 로 받는 것도 가능 --')
def func_list(*args):
  print('I got', len(args), 'arguments. first is', args[0])

func_list(10)
func_list(20, 10)
func_list(30, 20, 10)
func_list(40, 30, 20, 10)

def func_dict(**hash):
  print('Got the dictionary argument:', hash)

func_dict(name='john', age=20, score=4.5, msg='Hello,world')

print('\n-- 리턴타입을 tuple 로 하면 두개이상의 값을 리턴하는 것이 가능하다 --')

def func_returning_two(a, b):
  sum = a + b
  mul = a * b
  return sum, mul # return [sum, mul] 로 해도 결과는 동일하다. list 를 tuple 에 대입하는 셈이므로.

sum, mul = func_returning_two(12, 5)
print(f'{sum=} {mul=}') # f-string 의 위력은 곧 알아봅시다
