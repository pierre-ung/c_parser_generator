#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "parser.h"
int analyze_index = 0;
void usage(char *progname)
{
    fprintf(stderr, "Command format error:\n Usage : %s <word_to_analyze>\n", progname);
    exit(EXIT_FAILURE);
}
char *parse_S(char *word)
{
    char *res = NULL;
    int prev_index;

    prev_index = analyze_index;
    if (res == NULL && (res = parse_a(word)) != NULL)
    {
        res = parse_S(word);
        if (res == NULL)
            analyze_index = prev_index;
        else{return res;}
    }
    if (res == NULL && (res = parse_a(word)) != NULL)
    {
        
    }
    return res;
}
char *parse_a(char *word)
{
    if (word[analyze_index] == 'a')
    {
        analyze_index++;
        return word;
    }
    return NULL;
}
int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        usage(argv[0]);
    }
    char *word = argv[1];
    int word_len = strlen(word);
    char *res = parse_S(word);
    if (res == NULL || word_len != analyze_index)
    {
        printf("Le mot n'appartient pas au langage engendré par la grammaire\n");
    }
    else
    {
        printf("Le mot appartient au langage\n");
    }
    return 0;
}
