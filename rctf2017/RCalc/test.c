#include <stdio.h>
#include <stdlib.h>

int main(){
	char s[10];
	scanf("%s", s);
	for (int i = 0; i < 10; ++i)
		printf("s: %c, %x\n", s[i], s[i]);
	//long long r;
	/*for (int i = 0; i < 10000; ++i){
		srand(i);
		long long r;
		r = rand();
		r = (r << 32) | rand();
		if (r / 100000000000000000ll > 0)
			printf("%d, factor(%lld)\n", i, r);
	}*/
}
