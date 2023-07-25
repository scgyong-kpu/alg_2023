words = [
  "flagrant",
  "lawmaker",
  "allow",
  "alumina",
  "foxglove",
  "fiche",
  "concern",
  "kiosk",
  "clean",
  "especially",
  "wanton",
  "addle",
  "agitate",
  "whinchat",
]

print()
print('-- 각 글자별로 시작하는 단어가 몇개 있는제 세는 프로그램 --')
counts = dict() # Dictionary 를 초기화한다
for word in words: # 모든 단어들에 대하여
  first_ch = word[0] # 단어의 첫글자를 알아낸 뒤
  if not first_ch in counts: # Dictionary 에 해당 Key 가 없으면 
    counts[first_ch] = 0      # 만들고 0 으로 초기값을 준다
  counts[first_ch] += 1      # 해당 Key 의 Value 를 1 증가시킨다 

for ch in counts.keys():
  print(ch, counts[ch])

'''
-- 각 글자별로 시작하는 단어가 몇개 있는제 세는 프로그램 --
f 3
l 1
a 4
c 2
k 1
e 1
w 2
'''

print()
print('-- 보통 Dictionary 는 빨리 찾는 게 가장 중요한 구조라서 Key 들이 정렬되어 있지 않다 --')
print('-- Python 의 Dictionary 는 저장 순서를 보장해 준다 --')
print('-- Key 들을 정렬한 뒤에 루프를 돌아도 좋지만, 보통 그럴 일은 잘 없다 --')
for ch in sorted(counts.keys()):
  print(ch, counts[ch])