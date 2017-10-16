#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/mman.h>
#include <stdlib.h>
#include <time.h>

#define HEART_MAX 100

struct heart {
	size_t size ;
	char heart_name[32];
	char *secret ;	
};
struct heart *list = NULL;

void init_proc(){
	int addr = 0;
	setvbuf(stdout,0,2,0);
	setvbuf(stdin,0,2,0);
	srand(time(NULL));
	while(addr <= 0x10000){
		addr = rand() & 0xfffff000;
	}	
	list = mmap(addr,0x1000,PROT_READ|PROT_WRITE,MAP_PRIVATE|MAP_ANONYMOUS ,-1,0);
	if(list == -1){
		puts("mmap error");
		exit(0);
	}
}

int read_input(char *buf,unsigned int size){
    int ret ;
    ret = read(0,buf,size);
    if(ret <= 0){
        puts("read error");
        exit(1);
    }
    if(buf[ret-1] == '\n')
        buf[ret-1] = '\x00';
	return ret ;
}

int read_int(){
	int ret ;
    char buf[16];
    unsigned choice ;
    ret = read(0,buf,15);
    if(ret <= 0){
        puts("read error");
        exit(1);
    }
    choice = atoi(buf);
    return choice;
}

void heart_ctor(struct heart *h,size_t size){
	int ret ;
	h->size = size ;
	printf("Name of heart :");
	read_input(h->heart_name,32);
	h->secret = (char *)malloc(size);
	if(!h->secret){
		puts("Allocate Error !");
		exit(0);
	}
	printf("secret of my heart :");
	ret = read_input(h->secret,size);
	h->secret[ret] = '\x00'; 		// overflow, maybe shrink the heap
}

void heart_dtor(struct heart *h){
	h->size = 0;
	memset(h->heart_name,0,32);
	free(h->secret);
	h->secret = NULL;
}

void get_the_secret(){
	printf("Your secret : %p\n",list);
	puts("Good bye ~");
	exit(0);
}

void add_secret(){
	int i;
	size_t size ;
	for(i = 0 ; i < HEART_MAX ; i++){
		if(!list[i].secret){
			printf("Size of heart : ");
			size = read_int();
			if(size > 0x100){
				puts("Too big !");
				return ;
			}
			heart_ctor(&list[i],size);
			puts("Done !");				
			return ;
		}
	}
	puts("Fulled !!");	
}

void show_secret(){
	unsigned int idx ;
	printf("Index :");
	idx = read_int();
	if(idx < 0 || idx >= 100){
		puts("Out of bound !");
		exit(-2);
	}
	if(list[idx].secret){
		printf("Index : %d\n",idx);
		printf("Size : %lu\n",list[idx].size);
		printf("Name : %s\n",list[idx].heart_name);
		printf("Secret : %s\n",list[idx].secret);
	}else{
		puts("No such heap !");
	}	
}

void del_secret(){
	unsigned int idx ;
	printf("Index :");
	idx = read_int();
	if(idx < 0 || idx >= 100){
		puts("Out of bound !");
		exit(-2);
	}
	if(list[idx].secret){
		heart_dtor(&list[idx]);
		puts("Done !");
	}else{
		puts("No such heap !");
	}	
}

void menu(){
	puts("==================================");
	puts("        Secret of my heart        ");	
	puts("==================================");
	puts(" 1. Add a secret                  ");
	puts(" 2. show a secret                 ");
	puts(" 3. delete a secret               ");
	puts(" 4. Exit                          ");
	puts("==================================");
	printf("Your choice :");

}

int main(){
	init_proc();
	while(1){
		menu();
		switch(read_int()){
			case 1 :
				add_secret();
				break ;
			case 2 :
				show_secret();
				break ;
			case 3 :
				del_secret();
				break ;
			case 4 :
				exit(0);
				break ;
			case 4869 :
				get_the_secret();
				break ;
			default :
				puts("Invalid choice");
				break ;

		}
	}
}
