import sys

################################################# Fonctions #################################################

# Lis un fichier contenant une grammaire de type 2 (format : S -> XY)
#  Retourne un tableau des règles de la grammaire


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
        rules_couple.append(tuple(rule.split("->")))
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

# Génère le code C de la fonction parsant un NON TERMINAL
def gen_parse_NT(rule):
    NT = rule[0]
    code = "char* parse_" + NT + "(char* word){\n"
    code += "char* res = NULL;\n"
    code += "int prev_index = analyze_index;"
    for i in range(1, len(rule)):
        current_rule = rule[i]
        code += "if(res == NULL && (res = parse_" + current_rule[0] + "(word)) != NULL){\n"
        for j in range(1, len(current_rule)):
            code += "if(res != NULL){\n"
            code += "res = parse_" + current_rule[j] + "(word);\n"
            code += "if(res == NULL) analyze_index = prev_index;\n"
            code += "}"
        #code += "return res;\n}\n"
        code += "}"
    code += "return res;\n}"
    return code

# Génère le code C de la fonction parsant un TERMINAL
def gen_parse_T(T):
    code = "char* parse_" + T + "(char* word){\n"
    code += "if(word[analyze_index] ==\'" + T + "\'){\n"
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
            for char in compo:
                # Genere les fonctions associés aux terminaux
                if(char.islower() and char not in already_gen):
                    code += gen_parse_T(char)
                    already_gen.append(char)
    return code            

# Génération du code du fichier .h
def gen_h_code(rules):
    already_gen = []
    code = ""
    for rule in rules : 
        for compo in rule :
            for char in compo :
                if(char not in already_gen):
                    code += "char *parse_" + char + "(char *word);\n"
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
c_header += "#include \"" + output_name + ".h\"\n"
c_header += "int analyze_index = 0;\n"

# Génération du code de la fonction Usage
c_usage = "void usage(char *progname){\n"
c_usage += "fprintf(stderr, \"Command format error:\\n Usage : %s <word_to_analyze>\\n\", progname); exit(EXIT_FAILURE);}\n"

# Generation des fonctions parse_X
c_functions = gen_parse(rules) + "\n"

# Génération du main
c_main = "int main(int argc, char *argv[]){\n"
c_main += "if (argc != 2){usage(argv[0]);}\n"
c_main += "char *word = argv[1];\n"
c_main += "int word_len = strlen(word);\n"
c_main += "char *res = parse_" + rules[0][0] + "(word);\n"
c_main += "if (res == NULL || word_len != analyze_index){printf(\"Le mot n'appartient pas au langage engendré par la grammaire\\n\");}\n"
c_main += "else{printf(\"Le mot appartient au langage\\n\");}\n"
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