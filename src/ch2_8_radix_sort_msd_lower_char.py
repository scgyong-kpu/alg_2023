words = [
  'mog', 'jim', 'km', 'lining', 'mingle', 'ell', 'folk', 'melon', 'ln', 'link', 
  'knife', 'fennel', 'loon', 'john', 'ff', 'felloe', 'liking', 'lino', 'om', 'keg', 
  'joke', 'no', 'hog', 'jell', 'fino', 'elfin', 'gin', 'lone', 'oh', 'gong', 
  'ogee', 'oi', 'jig', 'filling', 'g', 'ge', 'mn', 'femme', 'fen', 'kj', 
  'gene', 'online', 'mg', 'goggle', 'emf', 'loll', 'meek', 'l', 'gem', 'filing', 
  'infill', 'hello', 'ink', 'monk', 'kg', 'ghillie', 'elf', 'gm', 'leo', 'genie', 
  'hoe', 'he', 'eke', 'moll', 'gnomon', 'fm', 'lei', 'million', 'going', 'feminine', 
  'infilling', 'liege', 'mo', 'o', 'goon', 'hg', 'legging', 'holm', 'enjoin', 'e', 
  'mini', 'logging', 'kin', 'hen', 'logo', 'flee', 'inf', 'fog', 'knee', 'limn', 
  'jingo', 'lf', 'log', 'non', 'lj', 'goo', 'hmg', 'joe', 'knell', 'minim', 
  'menfolk', 'feel', 'mlle', 'ken', 'home', 'if', 'linen', 'ne', 'lo', 'knoll', 
  'mime', 'ooh', 'nomen', 'hill', 'kohl', 'efl', 'offline', 'lee', 'king', 'legion', 
  'one', 'hike', 'genome', 'neigh', 'lifelong', 'him', 'gigolo', 'fo', 'fe', 'ego', 
  'mom', 'hi', 'fine', 'ni', 'ongoing', 'ho', 'noh', 'jog', 'lion', 'loin', 
  'fill', 'm', 'nee', 'join', 'noggin', 'neon', 'none', 'hm', 'gi', 'hook', 
  'ion', 'in', 'gen', 'mono', 'feign', 'look', 'hinge', 'moonie', 'nil', 'ginkgo', 
  'kilo', 'fief', 'ikon', 'moon', 'long', 'hf', 'lifeline', 'lingo', 'mink', 'nigh', 
  'k', 'killing', 'hoi', 'mongol', 'nikkei', 'ime', 'hoof', 'me', 'floe', 'omen', 
  'jiff', 'mike', 'foe', 'ingoing', 'leg', 'kiln', 'fin', 'noel', 'niff', 'minion', 
  'gnome', 'ill', 'ogle', 'info', 'igloo', 'fife', 'milk', 'loo', 'en', 'high', 
  'f', 'kook', 'miff', 'hele', 'hmi', 'longing', 'kink', 'n', 'fee', 'mm', 
  'hole', 'hellene', 'mien', 'moo', 'homing', 'jiggle', 'inkling', 'll', 'off', 'goof', 
  'lifelike', 'feline', 'lie', 'jingle', 'eel', 'filo', 'nook', 'eeg', 'gillie', 'leonine', 
  'ko', 'elk', 'honk', 'lien', 'mme', 'feeling', 'kneel', 'fleming', 'em', 'glee', 
  'mil', 'homo', 'offing', 'engine', 'limekiln', 'film', 'giggle', 'folio', 'ming', 'men', 
  'gone', 'oho', 'hone', 'lemming', 'iom', 'line', 'elm', 'liken', 'mile', 'henge', 
  'leek', 'golf', 'gloom', 'eon', 'kill', 'kimono', 'ok', 'inglenook', 'ilk', 'limo', 
  'lilo', 'ohm', 'melee', 'imf', 'hh', 'milfoil', 'kl', 'megohm', 'molehill', 'gel', 
  'kennel', 'ml', 'noon', 'mf', 'inn', 'felon', 'ghee', 'helm', 'keel', 'memo', 
  'nne', 'jinnee', 'on', 'hemline', 'nine', 'joie', 'glen', 'of', 'niggle', 'oil', 
  'nom', 'mill', 'nominee', 'fling', 'hell', 'lego', 'gemini', 'finn', 'eh', 'fie', 
  'onion', 'lemon', 'li', 'life', 'flog', 'jink', 'joggle', 'ofghijklmno', 'ofghijklmni', 'ofghijklmok'
]

# 단어에 사용된 글자는 e~o 의 11글자 뿐이다
FIRST_CHAR = 'e'
LAST_CHAR = 'o'
BASE = ord(FIRST_CHAR) - 1
char_count = ord(LAST_CHAR) - ord(FIRST_CHAR) + 1

def radix_lower_char_msd(array, left, right, depth=0):
  counts = [0 for _ in range(char_count + 1)]
  for i in range(left, right+1):
    string = array[i]
    str_len = len(string)
    slot = (ord(string[depth]) - BASE) if str_len > depth else 0
    char = string[depth] if str_len>depth else ' '
    # print(' ' * depth, f'{depth=} {str_len=:<2d} {char=} {slot=:<2d} {string=}')
    counts[slot] += 1

  # print(' ' * depth, f'{counts=}')
  for i in range(char_count):
    counts[i+1] += counts[i]
  # print(' ' * depth, f'index={counts}')

  for i in range(right, left-1, -1):
    string = array[i]
    str_len = len(string)
    slot = (ord(string[depth]) - BASE) if str_len > depth else 0 # slot 은 [0~26] 의 값을 가진다 (26 포함)
    # print(f'{depth=} {str_len=:<2d} {slot=:<2d} {string=}')
    counts[slot] -= 1         # slot 번째 인덱스를 하나 사용할 것이므로 1 줄인다
    at = left + counts[slot]  # temp 에 저장할 위치는 left 로부터 counts 만큼 떨어져 있다
    temp[at] = array[i]       # temp 내에 정렬된 결과가 들어가게 한다

  if depth > 0: print(' ' * depth, f'{depth=} {left=}, {right=}', array[left:right+1])
  array[left:right+1] = temp[left:right+1] # [left~right] 까지의 정렬된 결과를 array 로 복사한다
  if depth > 0: print(' ' * depth, f'{depth=} {left=}, {right=}', array[left:right+1])
  if depth > 0: print(' ' * depth, '-' * 30)

  for i in range(char_count + 1):
    sub_l = left + counts[i]
    sub_r = left + counts[i+1] - 1 if i < char_count else right
    # char = chr(i+BASE) if i > 0 else ' '
    # needs_recursion = 'Needs Recursion' if sub_l < sub_r else '-'
    # sub_arr = array[sub_l:sub_r+1]
    # print(' ' * depth, f'{char=} {sub_l=} {sub_r=} {needs_recursion} {sub_arr}')
    if sub_l < sub_r:
      radix_lower_char_msd(array, sub_l, sub_r, depth+1)
word_count = len(words)
temp = [0 for _ in range(word_count)]
radix_lower_char_msd(words, 0, word_count-1)
print(words)
