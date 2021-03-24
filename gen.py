# coding=utf-8
import sys
import time

################################################# Fonctions #################################################



# Rend les caractères d'un mot utilisable en C (par ex : '{', ';', ...)
def process_word(w):
    res = w
    equivalents = {"_" : "uscore", "{" : "rbrack", "}" : "lbrack", ";" : "semi", "," : "comma", "=" : "eq", "(" : "lpar", ")" : "rpar", " " : "epsilon"}
    for key in equivalents:
        res = res.replace(key, "_" + equivalents[key])
    res2 = res   
    for c in res2:
        if not (ord("0") <= ord(c) <= ord("9") or ord("a") <= ord(c) <= ord("z") or ord("A") <= ord(c) <= ord("Z")):
            res = res.replace(c, "_" + str(ord(c)))
    return res

# Lis un fichier contenant une grammaire de type 2 (format : S : XY : Action)
#  Retourne un tableau des règles de la grammaire
def read_grammar(filename):
    # Ouvrir, lire et fermer le fichier
    try:
        with open(filename, "r") as grammar:
            content = grammar.read()
    except:
        print("Cannot open the file " + filename)
        exit()
    # Conversion du fichier en liste de règles
    rules = content.splitlines()
    for i in range(len(rules)):
        rules[i] = rules[i].strip()
    rules_couple = []
    for rule in rules:
        if len(rule)>0:
            rule = rule.split(":",2)
            for i in range(len(rule)):
                rule[i] = rule[i].strip()
            #epsilon production
            if(len(rule[1]) == 0):
                try:
                    rule = [rule[0], " ", rule[2]]
                except:
                    rule = [rule[0], " "]
            rules_couple.append(rule)
    return merge_tuples(rules_couple)

#  Fusionne les tuples ayant le même 1er élément (i.e fusion des règles engendrés par le même non terminal)
def merge_tuples(tuples):
    res = []
    # Parcours des tuples
    for i in range(len(tuples)):
        # NT engendrant la règle
        rule_NT = tuples[i][0]
        tmp_tuple = [rule_NT,]
        for t in tuples:
            if(t[0] == rule_NT):
                if len(t) == 3:
                    tmp_tuple.append([t[1], t[2]])
                else:
                    tmp_tuple.append([t[1], ""])
        res.append(tmp_tuple)
    # Suppression des tuples dupliqués puis retour des tuples fusionnés
    return del_left_rec([i for n, i in enumerate(res) if i not in res[:n]])

def del_unreachable(liste):
    fini = False
    while not fini:
        new_liste = []
        fini = True
        NT_utilises = [liste[0][0]]
        for rules in liste:
            for rule in rules[1:]:
                for e in rule[0].split():
                    if e.strip()[0].isupper():
                        NT_utilises.append(e.strip())
        for rules in liste:
            if rules[0] in NT_utilises:
                new_liste.append(rules)
            else:
                fini = False
        liste = new_liste
    return liste

def isoler(liste):
    code = ""
    new_liste = []
    for rules in liste:
        NT = rules[0]
        new_rules = [NT]
        for i in range(1,len(rules)):
            code += "\nvoid isole_" + process_word(NT) + "_" + str(i) + "(void){\n"
            code += "\t"+rules[i][1]+"\n"
            code +="}"
            new_rules.append([rules[i][0],"isole_" + process_word(NT) + "_" + str(i)+"();"])
        new_liste.append(new_rules)
    return code, new_liste

def del_unit(liste): #Peut créer des règles inaccessibles et des conflits en C
    fini = False
    while not fini:
        fini = True
        liste_terminaux = [liste[i][0] for i in range(len(liste))]
        new_list = []
        for rules in liste:
            NT = rules[0]
            new_rules = [NT]
            for rule in rules[1:]:
                if rule[0].strip() in liste_terminaux:
                    fini = False
                    index = liste_terminaux.index(rule[0].strip())
                    for rule2 in liste[index][1:]:
                        new_rule = [rule2[0], rule[1]+rule2[1]]
                        new_rules.append(new_rule)
                else:
                    new_rules.append(rule)
            new_list.append(new_rules)
        liste = new_list
    return liste

def del_useless(liste):
    fini = False
    while not fini:
        liste_N_terminaux = set([liste[i][0] for i in range(len(liste))])
        new_liste = []
        fini = True
        for regles in liste:
            new_rules = [regles[0]]
            if len(regles) > 1:
                for regle in regles[1:]:
                    mots = regle[0].split()
                    N_terminaux_regle = set([c for c in mots if c[0].isupper()])
                    if N_terminaux_regle.issubset(liste_N_terminaux):
                        new_rules.append(regle)
                    else:
                        fini = False
                new_liste.append(new_rules)
                            
            #Si il existe un terminal sans règles, on l'enlève, sauf si c'est l'axiome
            else:
                if regles == liste[0]:
                    new_liste.append(new_rules) 
                else:
                    fini = False
               
        liste = new_liste
                        
    return liste

def del_epsilon_prod(liste):#Peut dédoubler des règles ?
    old_liste = liste
    #liste = del_unit(liste)
    fini = False
    axiom = liste[0][0]
    limite = len(liste) + 1
    courant = 0
    trouvee = False
    while not fini and courant <= limite:
        fini = True
        courant += 1
        if not trouvee:
            action = ""
            for rule in liste[0][1:]:
                if rule[0] == " ":
                    action = rule[1]
                    trouvee = True
            if trouvee:
                new_liste = []
                for rules in liste:
                    NT = rules[0]
                    new_rules = [NT]
                    for rule in rules[1:]:
                        new_rules.append(rule)
                        if axiom in rule[0]:
                            temp = rule[0].replace(axiom, " ")
                            temp = temp.split()
                            if temp == []:
                                new_rules.append([" ",rule[1]+action])
                            else:
                                new_rules.append([" ".join(temp),rule[1]+action])
                    new_liste.append(new_rules)
                liste = new_liste
            
        epsilon_NT = dict()

        for rules in liste[1:]:
            NT = rules[0]
            for rule in rules:
                if rule[0] == " ":
                    epsilon_NT[NT] = rule[1]                    
                    fini = False
        if not fini:
            for e in epsilon_NT:
                new_liste = []
                for rules in liste:
                    NT = rules[0]
                    new_rules = [NT]
                    for rule in rules[1:]:
                        if NT == axiom or NT not in epsilon_NT or rule[0].split() != []:
                            new_rules.append(rule)
                        if e in rule[0]:
                            temp = rule[0].replace(e, " ")
                            temp = temp.split()
                            if temp == []:
                                new_rules.append([" ",rule[1]+epsilon_NT[e]])
                            else:
                                new_rules.append([" ".join(temp),rule[1]+epsilon_NT[e]])
                    if len(new_rules)>1:
                        new_liste.append(new_rules)
                liste = new_liste
    if courant > limite:
        return old_liste
    else:
        return liste
    
def has_indirect_left_rec(liste):
    pile = [liste[0][0]]
    deja_vu = []
    while pile != []:
        current_NT = pile.pop()
        deja_vu.append(current_NT)
        for rules in liste:
            if rules[0] == current_NT:
                NT_debut = []
                for rule in rules[1:]:
                    temp = rule[0].split()
                    if temp != []:
                        if temp[0].isupper():
                            NT_debut.append(temp[0])
                NT_debut = set(NT_debut)
                for NT in NT_debut:
                    if NT not in deja_vu:
                        pile.append(NT)
                    else:
                        if NT != current_NT:
                            return True
    return False

def inf_or_equal(axiom,a,b):
    if a == b:
        return True
    if a == axiom:
        return True
    if b == axiom:
        return False
    return a < b

def del_ind_left_rec(liste):
    fini = False
    axiom = liste[0][0]
    limite = 200
    courant = 0
    while not fini and courant < limite and sum([len(e) for sl in liste for e in sl])<1000: #Limites au cas où l'on rentre dans une boucle (qui peut fait grossir la grammaire à l'infini)
        courant += 1
        fini = True
        new_liste = [liste[0]]
        for rules in liste[1:]:
            if not fini:
                new_liste.append(rules)
            else:
                NT = rules[0]
                new_rules = [NT]
                for rule in rules[1:]:
                    premier =  rule[0].split()[0]
                    if premier.isupper() and not inf_or_equal(axiom, NT , premier):
                        fini = False
                        alpha = " ".join(rule[0].split()[1:])
                        for orules in liste:
                            if orules[0] == premier:
                                for orule in orules[1:]:
                                    new_rules.append([orule[0] + " " + alpha,rule[1]+orule[1]])
                    else:
                        new_rules.append(rule)
                new_liste.append(new_rules)
        liste = new_liste
    return liste
            

def nouveau_NT(liste_NT):
    compteur = 0
    while "Z"+str(compteur) in liste_NT:
        compteur += 1
    return "Z"+str(compteur)

#Supprime la recusivite gauche direct d'une grammaire
def del_left_rec(liste):
    code = ""
    liste = del_useless(liste)
    try:
        code_temp, liste_temp = isoler(liste)
        liste_temp = del_epsilon_prod(liste_temp)
        has_rec = has_indirect_left_rec(liste_temp)
    except:
        has_rec = False
    if has_rec:
        liste_temp = del_ind_left_rec(liste_temp)
        code = code_temp
        liste = liste_temp
    #liste = del_unit(liste)
    #liste = del_unreachable(liste)
    new_rules = []
    liste_terminaux = [liste[i][0] for i in range(len(liste))]    
            
    for regle in liste:
        liste_left_rec = []
        liste_no_rec = []
        non_terminal = regle[0]
        for i in range(1,len(regle)):
            if regle[i][0][0] == non_terminal:
                liste_left_rec.append(regle[i])
            else :
                liste_no_rec.append(regle[i])
        if liste_left_rec != []:
            new_terminal = nouveau_NT(liste_terminaux)
            liste_terminaux.append(new_terminal)
            temp = []
            for b in liste_no_rec:
                temp.append([(b[0] + " " + new_terminal).strip(), b[1]])
            tuple_B = temp+liste_no_rec
            tuple_A = []
            for A in liste_left_rec:
                if A[0] == non_terminal:
                    tuple_A.append([A[0].replace(non_terminal, " ", 1),A[1]])
                else:
                    tuple_A.append([A[0].replace(non_terminal, "", 1).strip(),A[1]])
                tuple_A.append([(A[0].replace(non_terminal, "", 1) + " " + new_terminal).strip(),A[1]])
            #tuple_A = tuple(tuple_A)
            new_rules.append([non_terminal] + sorted(tuple_B, key = lambda x : -len(x[0])))
            new_rules.append([new_terminal] + sorted(tuple_A, key = lambda x : -len(x[0])))
        else:
            new_rules.append(regle)
    return code, new_rules

#Genere la fonction C str_split, pour séparer une chaine de caracteres en un tableau de chaines de caracteres
def gen_str_split():
    code =  "char** str_split(char* a_str, const char a_delim, int* word_len){\n"
    code += "char** result=0;size_t count=0;int nb_delim=0;char* tmp=a_str;char* last_comma=0;char delim[2];delim[0]=a_delim;delim[1]=0;\n"
    code += "while (*tmp){if (a_delim == *tmp){nb_delim +=1;if (a_delim != *(tmp+1)){count++;last_comma = tmp;}}tmp++;}"
    code += "if (strlen(a_str) == count) {result = malloc(sizeof(char)*1); result[0] = \"\"; return result;}"
    code += "count -= a_str[0] == a_delim;count += last_comma < (a_str + strlen(a_str) - 1);*(word_len) = count;count++;result = malloc(sizeof(char*) * count);"
    code += "if (result){size_t idx  = 0;char* token = strtok(a_str, delim);while (token){assert(idx < count);*(result + idx++) = strdup(token);token = strtok(0, delim);}assert(idx == count - 1);*(result + idx) = 0;}"
    code += "return result;}\n"
    return code


# Génère le code C de la fonction parsant un NON TERMINAL
def gen_parse_NT(rule):
    NT = rule[0]
    code = "char** parse_" + process_word(NT) + "(char** word){\n"
    code += "if(analyze_index > word_len) return NULL;\n"
    code += "char** res = NULL;\n"
    code += "int prev_index = analyze_index;int prev_action = strlen(actions);"
    for i in range(1, len(rule)):
        if(rule[i][0] != " "):
            current_rule = rule[i][0].split()
        else:
            current_rule = rule[i][0]
        code += "if(res == NULL && (res = parse_" + process_word(current_rule[0]) + "(word)) != NULL){\n"
        for j in range(1, len(current_rule)):
            code += "res = parse_" + process_word(current_rule[j]) + "(word);\n"
            code += "if(res == NULL) {\n"
            code += "analyze_index = prev_index;tronquer(actions,prev_action);\n"
            code += "goto " + "label_" + process_word(NT) + "_" + str(i) + ";\n"
            code += "}\n"
        code += "add_action(\""+ process_word(NT) + "_" + str(i)+"\");\n"
        code += "return res;"
        code += "}"
        code += "label_" + process_word(NT) + "_" + str(i) + ":\n"
    code += "return res;\n}"
    return code

def gen_actions(rules):
    code = ""
    for rule in rules:
        NT = rule[0]
        for i in range(1,len(rule)):
            code += "\nvoid action_" + process_word(NT) + "_" + str(i) + "(void){\n"
            code += "\t"+rule[i][1]+"\n"
            code +="}\n"
    return code

#Code C permettant d'ajouter une action à la liste des actions à effectuer en fin de programme
def gen_ajouter_actions():
    code = """void add_action(char * label){
        int n = strlen(actions) + 2 + strlen(label) + 1;
        char * temp = (char*) malloc(sizeof(char)*n);
        strcpy(temp, actions);
        strcat(temp, label);
        strcat(temp, " ");
        char * to_free = actions;
        actions = temp;
        free(to_free);
    }
    
    void tronquer(char* chaine, int l){
    	chaine[l] = 0;
    }\n
    """
    return code
#Code C permettant d'effectuer les différentes actions en fin de programme
def gen_actionneur(rules):
    code = """void actionneur(void){
    int nb_actions;
    char ** tab_actions = str_split(actions, ' ', &nb_actions);
    int i;
    for (i = nb_actions - 1; i > -1; i--){"""
    for rule in rules:
        NT = rule[0]
        for i in range(1,len(rule)):
            code += """if (strcmp(tab_actions[i],\"""" + process_word(NT) + "_" + str(i) + "\") == 0){" + rule[i][1] +"}"
    code +=  """
        }
    }\n
    """
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
            if compo[0] != " ":
                compo[0] = compo[0].split()
            for c in compo[0]:
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
        for compo in rule:
            for char in compo[0]:
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

code, rules = read_grammar(filename)

#### Génération du code des fichiers .c et .h
###Génération du code .c
# Génération de l'en-tête du fichier .c 
c_header =  "#include <stdlib.h>\n"
c_header += "#include <stdio.h>\n"
c_header += "#include <string.h>\n"
c_header += "#include <assert.h>\n"
c_header += "#include \"" + output_name + ".h\"\n"
c_header += "int analyze_index = 0; int word_len = 0;char * actions;\n"


# Génération du code de la fonction Usage
c_usage = "void usage(char *progname){\n"
c_usage += "fprintf(stderr, \"Command format error:\\n Usage : %s <word_to_analyze>\\n\", progname); exit(EXIT_FAILURE);}\n"

# Generation des fonctions auxilliaires et parse_X
c_functions = gen_str_split() + gen_ajouter_actions() + gen_parse(rules) + code + gen_actionneur(rules) + "\n"

# Génération du main
c_main = "int main(int argc, char *argv[]){\n"
c_main += "actions = malloc(sizeof(char));strcpy(actions,\"\");"
c_main += "if (argc != 2){usage(argv[0]);}\n"
c_main += "char ** word;"
c_main += "word = str_split(argv[1], ' ', &word_len);\n"
c_main += "char **res = parse_" + rules[0][0] + "(word);\n"
c_main += "if (res == NULL || word_len != analyze_index){printf(\"KO\\n\");}\n"
c_main += "else{actionneur();printf(\"OK\\n\");}\n"
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
