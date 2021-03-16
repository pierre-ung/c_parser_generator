# coding=utf-8
import sys

################################################# Fonctions #################################################

# Lis un fichier contenant une grammaire de type 2 (format : S -> XY)
#  Retourne un tableau des règles de la grammaire


# Rend les caractères d'un mot utilisable en C (par ex : '{', ';', ...)
def process_word(w):
    res = w
    equivalents = {"{" : "rbrack", "}" : "lbrack", ";" : "semi", "," : "comma", "=" : "eq", "(" : "lpar", ")" : "rpar", " " : "epsilon"}
    for key in equivalents:
        res = res.replace(key, equivalents[key])
    return res

def read_grammar(filename):
    # Ouvrir, lire et fermer le fichier
    try:
        grammar = open(filename, "r")
        content = grammar.read()
        grammar.close()
    except:
        print("Cannot open the file " + filename)
        exit()
    # Conversion du fichier en liste de règles
    rules = content.splitlines()
    rules_couple = []
    for rule in rules:
        #Supprimer les deux premiers espace (Entre le Terminal et sa dérivation)
        rule = rule.replace(' ', '', 2)
        rule = list(rule.split(":"))
        for i in range(len(rule)):
            rule[i] = rule[i].rstrip()
        #epsilon production=
        if(len(rule[1]) == 0):
            rule = list([rule[0], " "])

        rules_couple.append(rule)
    print(rules_couple)
    print(merge_tuples(rules_couple))
    return merge_tuples(rules_couple)

#  Fusionne les tuples ayant le même 1er élément (i.e fusion des règles engendrés par le même non terminal)
def merge_tuples(tuples):
    res = []
    # Parcours des tuples
    for i in range(len(tuples)):
        # NT engendrant la règle
        rule_NT = tuples[i][0]
        tmp_tuple = (rule_NT,)
        for t in tuples:
            if(t[0] == rule_NT):
                l = list(tmp_tuple)
                l.append(t[1])
                tmp_tuple = tuple(l)
        res.append(tmp_tuple)
    # Suppression des tuples dupliqués puis retour des tuples fusionnés
    return [i for n, i in enumerate(res) if i not in res[:n]]


def gen_str_split():
    code =  "char** str_split(char* a_str, const char a_delim, int* word_len){\n"
    code += "char** result=0;size_t count=0;char* tmp=a_str;char* last_comma=0;char delim[2];delim[0]=a_delim;delim[1]=0;\n"
    code += "while (*tmp){if (a_delim == *tmp){count++;last_comma = tmp;}tmp++;}"
    code += "count += last_comma < (a_str + strlen(a_str) - 1);*(word_len) = count;count++;result = malloc(sizeof(char*) * count);"
    code += "if (result){size_t idx  = 0;char* token = strtok(a_str, delim);while (token){assert(idx < count);*(result + idx++) = strdup(token);token = strtok(0, delim);}assert(idx == count - 1);*(result + idx) = 0;}"
    code += "return result;}"
    return code


# Génère le code C de la fonction parsant un NON TERMINAL
def gen_parse_NT(rule):
    NT = rule[0]
    code = "char** parse_" + NT + "(char** word){\n"
    code += "if(analyze_index > word_len) return NULL;\n"
    code += "char** res = NULL;\n"
    code += "int prev_index = analyze_index;"
    for i in range(1, len(rule)):
        if(rule[i] != " "):
            current_rule = rule[i].split(" ")
        else:
            current_rule = rule[i]  
        code += "if(res == NULL && (res = parse_" + process_word(current_rule[0]) + "(word)) != NULL){\n"
        for j in range(1, len(current_rule)):
            code += "res = parse_" + process_word(current_rule[j]) + "(word);\n"
            code += "if(res == NULL) {\n"
            code += "analyze_index = prev_index;\n"
            code += "goto " + "label_" + NT + str(i) + ";\n"
            code += "}\n"
        code += "}"
        code += "label_" + NT + str(i) + ":\n"
    code += "return res;\n}"
    return code

# Génère le code C de la fonction parsant un TERMINAL
def gen_parse_T(T):
    code = ""
    # Si le terminal est epsilon :
    if T == " ":
        code += "char** parse_" + process_word(T) + "(char** word){\n"
        code += "return word;}\n"
    # Sinon :
    else:
        code += "char** parse_" + process_word(T) + "(char** word){\n"
        code += "if (analyze_index >= word_len) return NULL;\n" # end if word len is already reached, not checked for epsilon production
        code += "if(strcmp(word[analyze_index], \"" + T + "\") == 0){\n"
        code += "analyze_index++;\n"
        code += "return word;}\n"
        code += "return NULL;\n}"
    return code

# Génère le code associé aux fonctions parse des T et NT
def gen_parse(rules):
    code = ""
    already_gen = []
    # On génère des fonction parsant tous les terminaux et non-terminaux
    for rule in rules:
        # Genrere les fonctions associés aux NT engendrant les règles
        code += gen_parse_NT(rule)
        for compo in rule[1:]:
            # Si ce n'est pas une regle X -> epsilon
            if compo != " ":
                compo = compo.split(' ')
            for c in compo:
                # Genere les fonctions associés aux terminaux
                if(not c[0].isupper() and c not in already_gen):
                    code += gen_parse_T(c)
                    already_gen.append(c)
    return code            

# Génération du code du fichier .h
def gen_h_code(rules):
    already_gen = []
    code = ""
    for rule in rules : 
        for compo in rule :
            if compo != " ":
                compo = compo.split(" ")
            for char in compo :
                if(char not in already_gen):
                    code += "char **parse_" + process_word(char) + "(char **word);\n"
                    already_gen.append(char)
    return code
                

        

################################################# Script #################################################
# Vérification des arguments
if(len(sys.argv) < 2):
    print("Usage : python3 ", sys.argv[0], " <grammaire> [out.c]")
    sys.exit()

# Ouverture du fichier contenant la grammaire cible
filename = sys.argv[1]
try:
    output_name = sys.argv[2]
except: 
    output_name = "parser"

rules = read_grammar(filename)

#### Génération du code des fichiers .c et .h
###Génération du code .c
# Génération de l'en-tête du fichier .c 
c_header =  "#include <stdlib.h>\n"
c_header += "#include <stdio.h>\n"
c_header += "#include <string.h>\n"
c_header += "#include <assert.h>\n"
c_header += "#include \"" + output_name + ".h\"\n"
c_header += "int analyze_index = 0; int word_len = 0;\n"


# Génération du code de la fonction Usage
c_usage = "void usage(char *progname){\n"
c_usage += "fprintf(stderr, \"Command format error:\\n Usage : %s <word_to_analyze>\\n\", progname); exit(EXIT_FAILURE);}\n"

# Generation des fonctions auxilliaires et parse_X
c_functions = gen_str_split() + gen_parse(rules) + "\n"

# Génération du main
c_main = "int main(int argc, char *argv[]){\n"
c_main += "if (argc != 2){usage(argv[0]);}\n"
c_main += "char **word = str_split(argv[1], ' ', &word_len);\n"
c_main += "char **res = parse_" + rules[0][0] + "(word);\n"
c_main += "if (res == NULL || word_len != analyze_index){printf(\"KO\\n\");}\n"
c_main += "else{printf(\"OK\\n\");}\n"
c_main += "for(int i=0; i<word_len; i++){free(word[i]);}free(word);\n"
c_main += "return 0;}\n"

# Code final du fichier .c
c_code = c_header + c_usage + c_functions + c_main

# Code final du fichier .h
h_code = gen_h_code(rules)


# Génération des fichiers .h et .c
try:
    c_file = open(output_name+".c", "w")
    h_file = open(output_name+".h", "w")
    c_file.write(c_code)
    h_file.write(h_code)
except:
    print("Cannot create target files (" + output_name + ".c or" + output_name + ".h)")
    exit()
print("Parser created ! Please keep .h et .c files in the same folder.")