class City:
  def __init__(self, name, x, y):
    self.name = name
    self.x, self.y = x, y
  def __repr__(self):
    return '%s(%3d,%3d)' % (self.name, self.x, self.y)

cities = [
  City("Clean", 1336, 536),  City("Prosy", 977, 860),
  City("Rabbi", 6, 758),     City("Addle", 222, 261),
  City("Smell", 1494, 836),  City("Quite", 905, 345),
  City("Lives", 72, 714),    City("Cross", 23, 680),
  City("Synth", 1529, 785),  City("Tweak", 1046, 426),
  City("Medic", 1485, 514),  City("Glade", 660, 476),
  City("Breve", 1586, 448),  City("Hotel", 1269, 576),
  City("Toing", 398, 561),   City("Scorn", 617, 373),
  City("Tweet", 1253, 403),  City("Zilch", 1289, 29),
  City("React", 296, 659),   City("Fiche", 787, 278),
]

print("--- Original Data ---")
print(cities)

# sort here by name
print("--- By Name ---")
print(cities)

# sort here by x
print("--- By X Coordinate ---")
print(cities)