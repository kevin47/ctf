#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include "scoreText.h"

#define TEMP 20
#define STEP 0.2
#define COUNT 10000

char *playfairDecipher(char *key, char *in,char *out, int len);
float playfairCrack(char *text,int len, char* maxKey);
static char *shuffleKey(char *in);

int main(int argc, char *argv[])
{
    // THINGS TO ENSURE: CIPHER AND KEY MUST BE UPPERCASE, CONSISTING ONLY OF LETTERS A-Z, AND NO OTHERS. YOU CAN SPELL OUT NUMBERS IF YOU NEED TO.
    // NEITHER THE CIPHER OR THE KEY SHOULD HAVE THE LETTER 'J' IN IT. IT WILL CRASH IF YOU DO NOT DO THESE THINGS. THIS IS A PROOF OF CONCEPT ONLY.
    //char cipher[]  = "XZOGQRWVQWNROKCOAELBXZWGEQYLGDRZXYZRQAEKLRHDUMNUXYXSXYEMXEHDGNXZYNTZONYELBEUGYSCOREUSWTZRLRYBYCOLZYLEMWNSXFBUSDBORBZCYLQEDMHQRWVQWAEDPGDPOYHORXZINNYWPXZGROKCOLCCOCYTZUEUIICERLEVHMVQWLNWPRYXHGNMLEKLRHDUYSUCYRAWPUYECRYRYXHGNBLUYSCCOUYOHRYUMNUXYXSXYEMXEHDGN";
    char *cipher = argv[1];
    int len = strlen(cipher);  
    char *out = (char *)malloc(sizeof(char)*(len+1));
    srand((unsigned)time(NULL)); // randomise the seed, so we get different results each time we run this program

    printf("Running playfaircrack, this could take a few minutes...\n");

    char key[] = "ABCDEFGHIKLMNOPQRSTUVWXYZ";
    int i=0;
    double score,maxscore=-99e99;
    // run until user kills it
    while(1){
        i++;
        score = playfairCrack(cipher,len,key);
        if(score > maxscore){
            maxscore = score;
            printf("best score so far: %f, on iteration %d\n",score,i);
            printf("    Key: '%s'\n",key);
            playfairDecipher(key, cipher,out, len);
            printf("    plaintext: '%s'\n",out);
        }
    }
    free(out);
    return 0;
}

void exchange2letters(char *key){
    int i = rand()%25;
    int j = rand()%25;
    char temp = key[i];
    key[i]= key[j];
    key[j] = temp;
}

void swap2rows(char *key){
    int i = rand()%5;
    int j = rand()%5;
    char temp;
    int k;
    for(k=0;k<5;k++){
        temp = key[i*5 + k];
        key[i*5 + k] = key[j*5 + k];
        key[j*5 + k] = temp;
    }
}

void swap2cols(char *key){
    int i = rand()%5;
    int j = rand()%5;
    char temp;
    int k;
    for(k=0;k<5;k++){
        temp = key[k*5 + i];
        key[k*5 + i] = key[k*5 + j];
        key[k*5 + j] = temp;
    }
}

/* our key modification consists of several different modifications: swapping rows, cols, flipping the
   keysquare rows, flipping all cols and reversing the whole key. In addition to this, single letter
   swaps are made. The letter swaps occur ~90% of the time. */
void modifyKey(char *newKey,char *oldKey){
    int k,j,i = rand()%50;
    switch(i){
        case 0: strcpy(newKey,oldKey); swap2rows(newKey); break;
        case 1: strcpy(newKey,oldKey); swap2cols(newKey); break;       
        case 2: for(k=0;k<25;k++) newKey[k] = oldKey[24-k]; newKey[25] = '\0'; break; // reverse whole keysquare
        case 3: for(k=0;k<5;k++) for(j=0;j<5;j++) newKey[k*5 + j] = oldKey[(4-k)*5+j]; // swap rows up-down
                newKey[25] = '\0';
                break;
        case 4: for(k=0;k<5;k++) for(j=0;j<5;j++) newKey[j*5 + k] = oldKey[(4-j)*5+k]; // swap cols left-right
                newKey[25] = '\0';
                break;
        default:strcpy(newKey,oldKey); 
                exchange2letters(newKey);
    }
}

/* this is the bit that implements the simulated annealing algorithm */
float playfairCrack(char *text,int len, char* bestKey){
    int i,j,count;
    float T;
    char temp, *deciphered = (char *)malloc(sizeof(char) * (len+1));
    char testKey[26];
    char maxKey[26];
    double prob,dF,maxscore,score;
    double bestscore;
    strcpy(maxKey,bestKey);
    playfairDecipher(maxKey,text,deciphered,len);
    maxscore = scoreTextQgram(deciphered,len);
    bestscore = maxscore;
    for(T = TEMP; T >= 0; T-=STEP){
        for(count = 0; count < COUNT; count++){ 
            modifyKey(testKey,maxKey);    
            playfairDecipher(testKey,text,deciphered,len);
            score = scoreTextQgram(deciphered,len);
            dF = score - maxscore;
            if (dF >= 0){
                maxscore = score;
                strcpy(maxKey,testKey);
            }else if(T > 0){
                prob = exp(dF/T);
                if(prob > 1.0*rand()/RAND_MAX){
                    maxscore = score;
                    strcpy(maxKey,testKey);                
                }
            }
            // keep track of best score we have seen so far
            if(maxscore > bestscore){
                bestscore = maxscore;
                strcpy(bestKey,maxKey);
            } 
        }
    }
    free(deciphered);
    return bestscore;
}


char *playfairDecipher(char *key, char *text, char *result, int len){
    int i;
    char a,b; /* the digram we are looking at */
    int a_ind,b_ind;
    int a_row,b_row;
    int a_col,b_col;
    
    for (i = 0; i < len; i += 2){
        a = text[i];
        b = text[i+1];
        /*if (index(key,a) == NULL || index(key,b) == NULL) break;*/
        a_ind = (int)(strchr(key,a) - key);
        b_ind = (int)(strchr(key,b) - key);
        a_row = a_ind / 5;
        b_row = b_ind / 5;
        a_col = a_ind % 5;
        b_col = b_ind % 5;
        if(a_row == b_row){
            if(a_col == 0){
                result[i] = key[a_ind + 4];
                result[i+1] = key[b_ind - 1];
            }else if(b_col == 0){
                result[i] = key[a_ind - 1];
                result[i+1] = key[b_ind + 4];
            }else{
                result[i] = key[a_ind - 1];
                result[i+1] = key[b_ind - 1];
            }
        }else if(a_col == b_col){
            if(a_row == 0){
                result[i] = key[a_ind + 20];
                result[i+1] = key[b_ind - 5];
            }else if(b_row == 0){
                result[i] = key[a_ind - 5];
                result[i+1] = key[b_ind + 20];
            }else{
                result[i] = key[a_ind - 5];
                result[i+1] = key[b_ind - 5];
            }
        }else{
            result[i] = key[5*a_row + b_col];
            result[i+1] = key[5*b_row + a_col];
        }
    }
    result[i] = '\0';
    return result;
}

// do fisher yeates shuffle      
static char *shuffleKey(char *in){
    int i,j;
    char temp;
    for (i = 24; i >= 1; i--){
        j = rand() % (i+1);
        temp = in[j];
        in[j] = in[i];
        in[i] = temp;
    }
    return in;
} 


