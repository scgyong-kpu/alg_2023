print('-- comma 로 연결하면 tuple 이 된다. () 를 써야 하는 경우가 많다--')
t1 = 1,2,'hello',3.5
t2 = (10, 20)
print(t1, t2)

print()
print('-- tuple 형태를 대입의 좌변에 사용하는 것도 가능하다--')
num,index,name,score = t1
print(index, score)

print()
print('-- 대입에서 배열을 우변으로, tuple 을 좌변으로 놓는 것도 가능하다--')
arr = [100, 200]
first, last = arr
print(first, last)

print()
print('-- tuple 은 readonly 이므로 tuple 이 필요할 때에도 배열을 사용하는 것이 편리할 때가 많다--')
xy1 = 123, 456
# xy1[1] += 10 # 이것은 할 수 없다
print('tuple 의 경우:', xy1[0], xy1[1])
xy2 = [234, 567]
print('list 의 경우 before:', xy2[0], xy2[1])
xy2[1] += 10
print('list 의 경우  after:', xy2[0], xy2[1])
# tuple 은 함수호출과 함께 많이 사용하니 함수 이후의 예제에도 주목하자
