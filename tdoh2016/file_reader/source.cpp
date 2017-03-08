#include <stdio.h>
#include <stdlib.h>
#include <memory.h>
#include <iostream>
char *fName;

void output(void)
{
	char *buff = (char*) malloc( sizeof(char)* 1024 );
	FILE *Fin = fopen( fName, "r" );
	fscanf( Fin, "%1023s", buff );
	printf( "%s\n", buff );
	fflush( stdout );
	fclose( Fin );
	free( buff );
}

int main(void)
{
	puts("Loser's Flag Reader v1.0");
	puts("What's your name?");
        fflush( stdout );

	char *buff = (char*) malloc( sizeof(char)* 32 );
	fName = (char*) malloc( 100 );
	memcpy( buff, "Loser", 5 );
	memcpy( fName, buff, 5 );
	free(buff);	

	char *guest = (char*) malloc( sizeof(char)* 32 );
	scanf( "%s", guest );

	printf( "Hello, %s! \nI will read \"%s\" file for your. :)\n", guest, fName); 
	fflush( stdout );
	output();
	return 0;
}

