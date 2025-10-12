#include <iostream>
#include <string>
using namespace std;

// See book p.64

int main()
{
  string yourName;
  cout << "Enter your name: ";
  cin >> yourName;  // this will only read to the first whitespace character!
  cout << "Greetings, " + yourName << endl;
  return 0;
}
