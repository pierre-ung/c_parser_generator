#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "parser.h"

void usage(char *progname)
{
    fprintf(stderr, "Command format error:\nUsage : %s <word_to_analyze>\n", progname);
    exit(EXIT_FAILURE);
}

/** Grammaire
 * S -> aSb
 * S -> cD
 * D -> d
 */

int analyze_index = 0;

char *parse_S(char *word)
{
    char *res;
    if ((res = parse_a(word)) != NULL)
    {
        res = parse_S(word);
        if (res == NULL)
            return NULL;
        res = parse_b(word);
        if (res == NULL)
            return NULL;
        return (res);
    }
    if ((res = parse_c(word)) != NULL)
    {
        res = parse_D(word);
        return (res);
    }
    return NULL;
}

char *parse_D(char *word)
{
    char *res;
    if ((res = parse_d(word)) != NULL)
    {
        return res;
    }
    return NULL;
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

char *parse_b(char *word)
{
    if (word[analyze_index] == 'b')
    {
        analyze_index++;
        return word;
    }
    return NULL;
}

char *parse_c(char *word)
{
    if (word[analyze_index] == 'c')
    {
        analyze_index++;
        return word;
    }
    return NULL;
}

char *parse_d(char *word)
{
    if (word[analyze_index] == 'd')
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

    /* Mot non reconnu OU partiellement reconnu (Un sous-mot de ce mot appartient au langage) */
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
