words = [
  'hut', 'apostle', 'equipment', 'fop', 'refined', 'parapet', 'mog', 'amputate', 'covetous', 'somebody', 
  'all', 'lobbyist', 'remark', 'subscriber', 'quorum', 'steppe', 'clean', 'cu', 'commend', 'prosy',
  'supererogation', 'indignation', 'wolverine', 'emporium', 'intersect', 'constitution', 'miscast', 'rabbi', 'enmity', 'loft',
  'temporize', 'speedboat', 'agenda', 'delusion', 'addle', 'idolize', 'romance', 'overestimate', 'revive', 'smell', 
  'quite', 'seminar', 'bloomers', 'lives', 'innocuous', 'effluent', 'cross', 'recidivist', 'wet', 'synth', 
  'mantilla', 'tweak', 'lowbrow', 'aviation', 'quadruped', 'capable', 'graphic', 'barman', 'intemperate', 'mastermind', 
  'submit', 'considering', 'riddance', 'polyethene', 'jim', 'varicolored', 'medic', 'ferric', 'minaret', 'capacitor', 
  'pusher', 'gingerbread', 'grizzled', 'upsilon', 'km', 'glade', 'ribbon', 'parascending', 'shinty', 'breve', 
  'hotel', 'similitude', 'fuddle', 'secretariat', 'silicate', 'whinchat', 'abstention', 'untrue', 'toing', 'cnd', 
  'ramification', 'scorn', 'apricot', 'arnica', 'militate', 'muslim', 'homicide', 'overfeed', 'shooting', 'growth',
  ''
]

BASE = ord('a') - 1 # ascii code of 'a' = 97

def radix_lower_char_msd(array, left, right, depth=0):
  counts = [0 for _ in range(27)] # 알파벳 'a' 이면 1, 'z' 면 26. 없으면 0. 총 27가지.
  for i in range(left, right+1):
    string = array[i]
    str_len = len(string)
    slot = (ord(string[depth]) - BASE) if str_len > depth else 0
    char = string[depth] if str_len>depth else ' '
    print(' ' * depth, f'{depth=} {str_len=:<2d} {char=} {slot=:<2d} {string=}')
    counts[slot] += 1

  print(' ' * depth, f'{counts=}')
  for i in range(26):
    counts[i+1] += counts[i]
  print(' ' * depth, f'index={counts}')

word_count = len(words)
temp = [0 for _ in range(word_count)]
radix_lower_char_msd(words, 0, word_count-1)
# print(words)
