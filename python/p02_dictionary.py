
# 중괄호와 : 을 사용하여 정의한다
d1 = {
  "hello": 10, "world": 20.5
}

print('-- Key 가 hello 인 항목의 value 는? --')
print(d1["hello"])

# 세 개의 key 에 대하여 그 값을 알아보자 가능한가?
keys = [ "hello", "are_you_there", "world" ]
for key in keys:
  print('-- Key:', key)

  value = d1[key] if key in d1 else '없는데요'
  # if key in d1:
  #   value = d1[key]
  # else:
  #   value = '없는데요'

  print('--- Value:', value)

# C/C++/Java 등에서 사용하는 3항연산자 a ? b : c 를
# python 에서는 b if a else c 형태로 사용한다
# 조금 더 영어문장스럽게 사용한다고 할 수 있다

