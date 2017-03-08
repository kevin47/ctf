#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>
#include <stdlib.h>
#define TIMEOUT 60


unsigned int money = 100000;

struct poke{
	char name[128];
	unsigned int price;
};

unsigned int count = 0;
struct poke* bag[20];

void sig_alarm_handler(int signum){
	puts("Timeout");
	exit(1);
}

void init(){
	setvbuf(stdout,0,2,0);
	signal(SIGALRM,sig_alarm_handler);
	alarm(TIMEOUT);
}

void menu(){
	puts("***********************************");
	puts("*          AIS3 pokeshop          *");
	puts("***********************************");
	puts("* 1.Buy a pokemon                 *");
	puts("* 2.Transfer a pokemon            *");
	puts("* 3.Rename your pokemon           *");
	puts("* 4.Exit                          *");
	puts("***********************************");
	printf("Your choice:");
}

void pokemenu(){
	puts("***********************************");
	puts("*    Which pokemon do you want?   *");
	puts("***********************************");
	puts("* 1.Magikarp ($ 1000000)          *");
	puts("* 2.Pikachu ($ 56746)             *");
	puts("* 3.Dragonite ($ 31337)           *");
	puts("* 4.Snorlax ($ 5566)              *");
	puts("* 5.Eevee ($ 8763)                *");
	puts("***********************************");
	printf("Your money : %u\n",money);
	printf("Your choice:");
}

int addpoke(char *name,unsigned int pokeprice){
	if(money < pokeprice){
		puts("You don't have enough money for the pokemon.");
		return -1;
	}
	if(count > 20){
		puts("Your bag is full");
		return -1;
	}
	for(int i=0; i < 20 ; i++){
		if(!bag[i]){
			bag[i] = (struct poke*)malloc(sizeof(struct poke));
			if(!bag[i]){
				puts("Allocate failed");
				exit(-1);
			}
			strcpy(bag[i]->name,name);
			bag[i]->price = pokeprice;
			count++;
			money -= pokeprice;
			puts("Buy successful");
			break;
		}
	}
}

void buy(){
	unsigned int choice;
	pokemenu();
	scanf("%u",&choice);
	switch(choice){
		case 1:
			addpoke("Magikarp",1000000);
			break ;
		case 2:
			addpoke("Pikachu",56746);
			break ;
		case 3:
			addpoke("Dragonite",31337);
			break ;
		case 4:
			addpoke("Snorlax",5566);
			break ;
		case 5:
			addpoke("Eevee",8763);
			break ;
		default:
			puts("Invalid Choicde");
			break;
	}
}

void listpoke(){
	if(count > 0){
		puts("Your pokemon:");
		puts("-----------------------------------");
		for(int i=0 ; i < 20;i++){
			if(bag[i]){
				printf("%d : %s, $ %u\n",i,bag[i]->name,bag[i]->price);
			}
		}
		puts("-----------------------------------");
	}
}

void transfer(){
	unsigned int choice;
	if(count <=0){
		puts("You don't have pokemon in your bag");
		return;
	}
	listpoke();
	printf("Which pokemon do you want to transfer :");
	scanf("%d",&choice);
	if(choice >= 0 && choice < 20){
		if(bag[choice]){
			printf("You get %u\n",(bag[choice]->price)/2);
			money += (bag[choice]->price)/2;
			count-- ;
			free(bag[choice]);
			bag[choice] = NULL;
			puts("Transfer successful!!");
		}else{
			puts("Invalid Choice");
			return;
		}
	}else{
		puts("Invalid Choice");
		return;
	}

};

void re(){
	char name[128];
	unsigned int choice;
	if(count <=0){
		puts("You don't have pokemon in your bag");
		return;
	}
	listpoke();
	printf("Which pokemon do you want to rename :");
	scanf("%d",&choice);
	if(choice >=0 && choice < 20){
		if(bag[choice]){
			printf("Name:");
			scanf("%128s",name);
			strcpy(bag[choice]->name,name);
			puts("Done !");
		}else{
			puts("Invalid Choice");
			return;
		}
	}else{
		puts("Invalid Choice");
		return;
	
	}

}

int main(void){	
	char buf[128];
	unsigned int choice;
	init();
	while(1){
		menu();
		read(0,buf,128);
		choice = atoi(buf);
		switch(choice){
			case 1:
				buy();
				break;
			case 2:
				transfer();
				break;
			case 3:
				re();
				break;
			case 4:
				return 0;
				break;
			default:
				puts("Invalid Choice");
				break;
		}

	}
	
}
