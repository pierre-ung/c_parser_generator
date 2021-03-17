import os
import subprocess
import time 



def test_speed(path_grammaire, words):
    print("\n--- Test on grammar of "+path_grammaire+" ---")
    
    os.system('python ../gen.py '+path_grammaire)                 # Génération du code C du parser sur la grammaire en argument

    os.system('gcc parser.c -o parserToTest')                     # Compilation du parser

    for word in words:                                            # Boucle testant le temps d'execution des mots passé en argument
        print("\nTest on word : "+word)
        timeStarted = time.time()                                 # Sauvegarde du temps de départ

        subprocess.run([".\\parserToTest",word])                  # Execution du parser avec sur un mot

        timeDelta = time.time() - timeStarted                     # Temps d'execution
        print("Finished process in "+str(timeDelta)+" seconds.") 

    
   


# Grammaire 1
words = ["a a","a c","a a a a a a b"]
test_speed("./grammaires/g_test1.txt",words)

# Grammaire 2
words = ["b a","b a x","b b b b b a x x x x x x x"]
test_speed("./grammaires/g_test2.txt",words)

# Grammaire 3
words = ["x x x y y y","x x y","x x x x x a a b b b b y y y y y"]
test_speed("./grammaires/g_test3.txt",words)