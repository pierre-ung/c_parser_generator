import sys

# Fonctions

## Lis un fichier contenant une grammaire de type 2 (format : S -> XY)
## Retourne un tableau des règles de la grammaire
def read_grammar(filename):
    ### Ouvrir, lire et fermer le fichier
    grammar = open(filename, "r")
    content = grammar.read()
    grammar.close()

    ### Conversion du fichier en liste de règles
    rules = content.splitlines()
    rules_couple = []
    for rule in rules:
        rules_couple.append(tuple(rule.split("->")))
    return merge_tuples(rules_couple)

# Fusionne les tuples ayant le même 1er élément (i.e fusion des règles engendrés par le même non terminal)
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
def gen_parse_NT(rule) :
    NT = rule[0]
    code = "char* parse_" + NT + "(char* word){\n"
    code += "char* res;\n"
    for i in range(1, len(rule)):
        current_rule = rule[i]
        code += "if((res = parse_" + current_rule[0] + "(word)) != NULL){\n"
        for j in range(1, len(current_rule)):
            code += "res = parse_" + current_rule[j] + "(word);\n"
            code += "if(res == NULL) return NULL;\n"
        code += "return res;\n}\n"
    code += "return NULL;\n}"
    return code



# Script
## Vérification des arguments
if(len(sys.argv) < 2):
    print("Usage : python3 ", sys.argv[0], " <grammaire> [out.c]")
    sys.exit()

## Ouverture du fichier contenant la grammaire cible
filename = "g_test.txt" #sys.argv[1]

rules = read_grammar(filename)
print(gen_parse_NT(rules[1]))


