#include <iostream>
#include <string>
using namespace std;

// See book p.64 and following

int main()
{
  string yourName;
  cout << "Enter your name: ";
  cin >> yourName;  // std::cin is easy way to get user input
  cout << "Greetings, " + yourName << endl;
  return 0;
}
