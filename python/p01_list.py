#
a = [0, 1,2,3,4,5,6,7,8,9]
b = range(10)

# list 와 # range 는 내부적으로는 다른 것이지만 비슷한 용도로 사용된다
print('-- list vs range --')
print(a)
print(b)
'''
-- list vs range --
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
range(0, 10)
'''

# for loop 를 돌아보면 결과가 같다. 하지만 range 를 쓰는 편이 효율적이다
print('-- for loop over list / range --')
for i in a:
  print(i, end=' - ')
print('//')
for i in b:
  print(i, end=' - ')
print('//')
'''
-- for loop over list / range --
0 - 1 - 2 - 3 - 4 - 5 - 6 - 7 - 8 - 9 - //
0 - 1 - 2 - 3 - 4 - 5 - 6 - 7 - 8 - 9 - //
'''

# print 할 때 end= 를 전달해주면 끝에 newline 을 붙이는 대신 사용한다


# len() 으로 크기를 구해 보면 결과는 동일하다
print('-- len of list / range --')
print(len(a)) # 10
print(len(b)) # 10

# range 를 꼭 list 형태로 나타내야 한다면 list 생성자를 이용한다
print('-- range to list --')
print(list(b))
'''
-- range to list --
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
'''


