print('-- comma 로 연결하면 tuple 이 된다. () 를 써야 하는 경우가 많다--')
t1 = 1,2,'hello',3.5
t2 = (10, 20)
print(t1, t2)

print()
print('-- tuple 형태를 대입의 좌변에 사용하는 것도 가능하다--')
num,index,name,score = t1
print(index, score)

