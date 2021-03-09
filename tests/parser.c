#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>
#include "parser.h"
int analyze_index = 0;
void usage(char *progname)
{
    fprintf(stderr, "Command format error:\n Usage : %s <word_to_analyze>\n", progname);
    exit(EXIT_FAILURE);
}

char** str_split(char* a_str, const char a_delim, int* word_len)
{
    char** result    = 0;
    size_t count     = 0;
    char* tmp        = a_str;
    char* last_comma = 0;
    char delim[2];
    delim[0] = a_delim;
    delim[1] = 0;
    while (*tmp){if (a_delim == *tmp){count++;last_comma = tmp;}tmp++;}
    
    count += last_comma < (a_str + strlen(a_str) - 1);*(word_len) = count;count++;result = malloc(sizeof(char*) * count);
    
    
    if (result){size_t idx  = 0;char* token = strtok(a_str, delim);while (token){assert(idx < count);*(result + idx++) = strdup(token);token = strtok(0, delim);}assert(idx == count - 1);*(result + idx) = 0;}
    return result;}


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
        else
        {
            return res;
        }
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
    int word_len;
    char **word = str_split(argv[1], ' ', &word_len);
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
