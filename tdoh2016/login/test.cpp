#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <cstring>

int main(){
	unsigned int rnd;
	unsigned int sum = 0;
	for (int i = 0; i < 1000; ++i){
		srand(i);
		rnd = rand() % 1000;	
		if (i == rnd)
			printf("ans: %d\n", i); 
	}
	return 0;
}
