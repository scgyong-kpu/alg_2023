words = [
  "flagrant",
  "lawmaker",
  "allow",
  "alumina",
  "concern",
  "kiosk",
  "incursion",
  "offhand",
  "especially",
  "wanton",
  "delectation",
  "hebraic",
  "inbred",
  "agitate", # 마지막 원소에 , 를 써도 된다 (trailing comma)
]

print('-- index 3 번째에 있는 것 --')
print(words[3])

print('-- index 3 번째 이후에 있는 것 --')
print(words[3:])

print('-- index 3 번째 직전까지 있는 것 --')
print(words[:3])

print('-- index 3 번째 이후, 4번째 직전까지 있는 것 --')
print(words[3:4])
# python 에서 범위를 지정할 때는 대부분 [inclusive, exclusive) 형태를 사용한다.
# (거의)유일하게 random.randinit(10, 15) 의 경우만 [inclusive, inclusive] 형태이다
# random.randrange(10, 15) 를 쓰면 [10, 15) 가 되기도 한다

word = "especially"
print(word[3:8], word[2:])
# slicing 은 문자열에 대해서도 적용된다
# string 역시 collection 으로 인식되기 때문

