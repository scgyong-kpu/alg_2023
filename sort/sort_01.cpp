#include <iostream>
#include <algorithm>

using namespace std;

class City {
public:
  string name;
  int x, y;
  City(const char *name, int x, int y) {
    this->name = name; this->x = x; this->y = y;
  }
  ostream &print(ostream &os) const {
    os << name << '(' << x << ',' << y << ')';
    return os;
  }
};
ostream &operator <<(ostream &os, const City &c) {
  return c.print(os);
}
void printCities(City *p, int count) {
  for (int i = 0; i < count; i++, p++) {
    cout << *p << ' ';
  }
  cout << '\n';
}
City cities[] = {
    City("Clean", 1336, 536), City("Prosy", 977, 860),  City("Rabbi", 6, 758),    City("Addle", 222, 261),
    City("Smell", 1494, 836), City("Quite", 905, 345),  City("Lives", 72, 714),   City("Cross", 23, 680),
    City("Synth", 1529, 785), City("Tweak", 1046, 426), City("Medic", 1485, 514), City("Glade", 660, 476),
    City("Breve", 1586, 448), City("Hotel", 1269, 576), City("Toing", 398, 561),  City("Scorn", 617, 373),
    City("Tweet", 1253, 403), City("Zilch", 1289, 29),  City("React", 296, 659),  City("Fiche", 787, 278),
};

int main(void) 
{
  int n_cities = sizeof(cities) / sizeof(cities[0]);

  cout << "--- Original Data ---" << endl;
  printCities(cities, n_cities);

  // sort here by name
  cout << "--- By Name ---" << endl;
  printCities(cities, n_cities);

  // sort here by y coordinate
  cout << "--- By Y Coordinate ---" << endl;
  printCities(cities, n_cities);

  return 0;
}
