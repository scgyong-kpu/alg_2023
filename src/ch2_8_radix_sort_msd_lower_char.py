words = [
  'clean', 'prosy', 'rabbi', 'addle', 'smell', 'quite', 'lives', 'cross', 'synth', 'tweak', 
  'medic', 'glade', 'breve', 'hotel', 'toing', 'scorn', 'tweet', 'zilch', 'react', 'fiche', 
  'stunt', 'swing', 'merry', 'brine', 'miter', 'withy', 'brink', 'madly', 'spicy', 'cleft', 
  'cheep', 'grief', 'links', 'write', 'fixed', 'yobbo', 'grave', 'cress', 'ensue', 'imply', 
  'datum', 'quoit', 'twain', 'allow', 'kiosk', 'wheat', 'birch', 'flail', 'thong', 'bongo', 
  'quilt', 'satyr', 'alibi', 'auger', 'event', 'scowl', 'shelf', 'melon', 'scrap', 'drupe', 
  'nadir', 'kudos', 'pushy', 'bases', 'atone', 'knife', 'seise', 'odour', 'venom', 'filmy', 
  'barre', 'davit', 'smart', 'canon', 'dixie', 'pease', 'adorn', 'liver', 'druid', 'baked', 
  'tulip', 'unzip', 'nervy', 'hubby', 'sweat', 'scald', 'deity', 'nutty', 'mourn', 'unbar', 
  'logic', 'stage', 'sisal', 'curvy', 'issue', 'pilot', 'wrote', 'quiff', 'willy', 'plate', 
  'nobel', 'chubb', 'banjo', 'dirge', 'audit', 'rosin', 'scrag', 'papal', 'ducky', 'creed', 
  'thief', 'pinko', 'hairy', 'cobra', 'waken', 'chime', 'cower', 'whelp', 'milky', 'fauna', 
  'carob', 'locum', 'month', 'check', 'dicey', 'debit', 'women', 'calve', 'weepy', 'crash', 
  'durex', 'ovoid', 'aside', 'blame', 'stela', 'humph', 'amino', 'smash', 'sorry', 'muzzy', 
  'camel', 'sales', 'biddy', 'indue', 'jural', 'tress', 'egret', 'error', 'ogive', 'frizz', 
  'quern', 'divvy', 'style', 'silky', 'elver', 'strum', 'sweep', 'taste', 'largo', 'there', 
  'doric', 'slick', 'waive', 'rejig', 'comet', 'punch', 'frill', 'dolby', 'saver', 'brash', 
  'sepoy', 'nippy', 'batty', 'unite', 'promo', 'towel', 'facia', 'digit', 'ripen', 'sylph', 
  'softy', 'radio', 'aback', 'afore', 'sedan', 'ghyll', 'tying', 'mulch', 'caber', 'ghost', 
  'sheaf', 'elfin', 'squad', 'patch', 'ester', 'roger', 'newel', 'tokay', 'hydro', 'tutti', 
  'infer', 'widow', 'hives', 'inure', 'globe', 'cobol', 'annex', 'stout', 'ovary', 'wormy', 
  'pique', 'empty', 'snowy', 'oxbow', 'cinch', 'plumy', 'piety', 'craft', 'fetch', 'mosey', 
  'sense', 'tease', 'handy', 'gismo', 'ditty', 'coypu', 'lunch', 'screw', 'pager', 'ferry', 
  'kinky', 'owlet', 'guess', 'whisk', 'epoch', 'coney', 'flour', 'spout', 'awoke', 'gnash', 
  'dinky', 'manic', 'nacho', 'rerun', 'serge', 'flier', 'waltz', 'pubis', 'shove', 'bossa', 
  'swath', 'mousy', 'pivot', 'frock', 'muzak', 'bogie', 'tenet', 'impel', 'ahead', 'stuck', 
  'rural', 'judge', 'pommy', 'papaw', 'senna', 'testa', 'slash', 'unity', 'roost', 'dhoti', 
  'solid', 'dicky', 'crier', 'seven', 'stick', 'curse', 'haiku', 'laver', 'amuse', 'store', 
  'union', 'build', 'knurl', 'rough', 'anion', 'nappy', 'solve', 'halal', 'assay', 'stile', 
  'bunny', 'ember', 'baron', 'sauce', 'boost', 'spoof', 'ledge', 'jolly', 'swift', 'krone', 
  'fecal', 'badge', 'fusty', 'tumid', 'leger', 'waver', 'folly', 'islam', 'squid', 'fuzzy', 
  'hammy', 'ducks', 'tongs', 'final', 'foray', 'femme', 'groan', 'vapid', 'iliac', 'crest', 
  'skull', 'drive', 'melba', 'dingy', 'wrack', 'emery', 'lucky', 'savoy', 'trawl', 'zebra', 
  'tepid', 'thick', 'objet', 'gouda', 'sleep', 'downy', 'twine', 'penal', 'owner', 'tangy', 
]

BASE = ord('a') - 1 # ascii code of 'a' = 97

def radix_lower_char_msd(array, left, right, depth=0):
  counts = [0 for _ in range(27)] # 알파벳 'a' 이면 1, 'z' 면 26. 없으면 0. 총 27가지.
  for i in range(left, right+1):
    string = array[i]
    str_len = len(string)
    slot = (ord(string[depth]) - BASE) if str_len > depth else 0
    char = string[depth] if str_len>depth else ' '
    # print(' ' * depth, f'{depth=} {str_len=:<2d} {char=} {slot=:<2d} {string=}')
    counts[slot] += 1

  # print(' ' * depth, f'{counts=}')
  for i in range(26):
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

  for i in range(27):
    sub_l = left + counts[i]
    sub_r = left + counts[i+1] - 1 if i < 26 else right
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
