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

