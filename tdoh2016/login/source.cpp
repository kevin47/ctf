nclude <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <cstring>
int main(void)
{
	unsigned int rnd;
	unsigned int sum = 0;
	char buffer[24];
	puts("Welcome to TDOH login system v1.0");
	//puts("HINT, KEY TYPE: TDOH{xxxxxxxxxxx}");
	printf("What's your name? ");
	fflush(stdout);
	
	scanf("%23s", buffer);
	for(int i = 0; i < strlen(buffer); i++ )
		sum += buffer[i];

	srand( sum );	
	rnd = rand() % 1000;	

	printf("Input your passcode: ");
	fflush(stdout);
	scanf("%i", &sum);
	
	if ( sum == rnd ) 
		system("cat flag");
	else
		puts("GANDALF: you shall not pass."); 		
	return 0;
}

