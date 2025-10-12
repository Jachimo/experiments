#include <iostream>
#include <string>
using namespace std;

int main()
{
  string toyName = "Balloons";
  string toyQuantity = "99";
  string toyColor = "Red";
  string outputText;
  outputText = (toyQuantity + " " + toyColor + " " + toyName);
  cout << outputText << endl;
  return 0;
}
