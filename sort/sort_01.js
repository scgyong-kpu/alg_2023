// https://replit.com/languages/nodejs

class City {
  constructor(name, x, y) {
    this.name = name;
    this.x = x;
    this.y = y;
  }
}

let cities = [
  new City("Clean", 1336, 536),  new City("Prosy", 977, 860),
  new City("Rabbi", 6, 758),     new City("Addle", 222, 261),
  new City("Smell", 1494, 836),  new City("Quite", 905, 345),
  new City("Lives", 72, 714),    new City("Cross", 23, 680),
  new City("Synth", 1529, 785),  new City("Tweak", 1046, 426),
  new City("Medic", 1485, 514),  new City("Glade", 660, 476),
  new City("Breve", 1586, 448),  new City("Hotel", 1269, 576),
  new City("Toing", 398, 561),   new City("Scorn", 617, 373),
  new City("Tweet", 1253, 403),  new City("Zilch", 1289, 29),
  new City("React", 296, 659),   new City("Fiche", 787, 278),
]
console.log("--- Original Data ---")
console.log(cities)

// sort here by name
console.log("--- By Name ---")
console.log(cities)

// sort here by x
console.log("--- By X Coordinate ---")
console.log(cities)
