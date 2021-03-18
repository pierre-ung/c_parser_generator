import os
import subprocess
import time 



def test_speed(path_grammaire, path_words):
    print("\n--- Test on grammar of "+path_grammaire+" ---")
    
    os.system('python3 ../gen.py '+path_grammaire)                 # Génération du code C du parser sur la grammaire en argument

    os.system('gcc parser.c -o parserToTest')                     # Compilation du parser

    # Récupération des mots
    try:
        grammar = open(path_words, "r")
        content = grammar.read()
        grammar.close()
    except:
        print("Cannot open the file " + path_words)
        exit()
    
    words = content.splitlines()
    

    for word in words:
        word = word.split(':')                                            # Boucle testant le temps d'execution des mots passé en argument
        print("\ntest word : "+word[0])
        print("Expected :" + word[1] + "\nResult : ")
        timeStarted = time.time()                                 # Sauvegarde du temps de départ

        subprocess.run(["./parserToTest",word[0]])                  # Execution du parser avec sur un mot

        timeDelta = time.time() - timeStarted                     # Temps d'execution
        print("Finished process in "+str(timeDelta)+" seconds.") 

    
   


# Grammaire 1
#words = ["a a","a c","a a a a a a b"]
test_speed("./grammaires/g_test1.txt","./grammaires/words/g_test1_words.txt")

# Grammaire 2
#words = ["b a","b a x","b b b b b a x x x x x x x"]
test_speed("./grammaires/g_test2.txt","./grammaires/words/g_test2_words.txt")

# Grammaire 3
#words = ["x x x y y y","x x y","x x x x x a a b b b b y y y y y",""]
test_speed("./grammaires/g_test3.txt","./grammaires/words/g_test3_words.txt")

# Grammaire 4
test_speed("./grammaires/g_test4.txt","./grammaires/words/g_test4_words.txt")

# Grammaire 5
test_speed("./grammaires/g_test5.txt","./grammaires/words/g_test5_words.txt")

# Grammaire 6
test_speed("./grammaires/g_test6.txt","./grammaires/words/g_test6_words.txt")