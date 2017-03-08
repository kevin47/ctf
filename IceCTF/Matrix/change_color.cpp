#include <iostream>
#include <cstdio>

using namespace std;

int main(){
	char buff[128];
	while (gets(buff)){
		for (int i = 0; buff[i]; ++i){
			if (buff[i] == '1'){
				cout << "\033[1;40m  \033[0m";
			}
			else
				cout << "\033[1;47m  \033[0m";
		}
		cout << "\n";
	}
}
