

# Projet Automates et Langages
## Sommaire
- [Présentation](#présentation)
- [Utilisation](#utilisation)
  * [Pré-requis](#pré-requis)
  * [Spécification de la grammaire](#spécification-de-la-grammaire)
  * [Lancement rapide](#lancement-rapide)
  * [Lancement personnalisé](#lancement-personnalisé)
  * [Analyser un mot](#analyser-un-mot)
- [Précisions techniques](#précisions-techniques)
- [Tests effectués et performances](#tests-effectués-et-performances)
- [Limites](#limites)


## Présentation
Dans le cadre de l'U.E Automates et Langages (INSA Toulouse), nous avons réalisé un programme générant des parser de Context-Free Grammar.
**Groupe** : 4IR - B1 
**Étudiants** : Alexandre Gonzalvez, Benjamin Vendeville, Jasper Güldenstein, Marino Benassai, Mikhail Zakharov, Fabien Castilla, Pierre Ung

## Utilisation
### Pré-requis
Le programme a été développé et testé  avec :

 - **Python 3.8.5**
 - **gcc 9.3.0**
 - **GNU Make 4.2.1**

*Il est probable qu'il fonctionne aussi avec des versions antérieurs* 

### Spécification de la grammaire
Pour spécifier une grammaire il faut rédiger la grammaire dans un fichier texte sous le format suivant :

    NT : t NT [: Action]
    NT : NT2 [: Action]
    NT2 : a b [: Action]
    ect... 
**L'axiome** de la grammaire est le terminale de la **première règle** décrite (ici, NT).
Exemple de grammaire à fournir en entrée :

    S : a S b : printf("S");
    S : X : printf("S");
    X : c : printf("X")
    X : d
    X : 

**Remarques :** 
Définir une action à effectuer est optionnel. Une action doit être écrite en C.



### Lancement rapide
Pour générer un parser par défaut, parsant la grammaire du fichier g_test.txt, l’exécutable sera nommé *parser*  :

    make
    
Pour générer un parser en fonction d'une autre grammaire : 

    make gen in=<grammaire_in> out=<nom_executable_out>
    
Pour supprimer les fichiers intermédiaires (.c et .h) : 

    make clean

### Lancement manuel
Le générateur de parser est un script Python générant un code C (le parser). Pour générer le parser :

    python gen.py <fichier grammaire> [nom_fichier_c_out=parser]

Ensuite, compilez le fichier C généré : 

    gcc <fichier_généré.c> -o [nom_executable]

### Analyser un mot
Pour lancer le parser généré sur un mot à analyser :

    ./nom_executable <mot à analyser>
Si le mot appartient au langage engendré par la grammaire, **OK** s'affiche. Sinon, **KO** s'affiche. 

## Précisions techniques

 - Dans le script Python, nous modifiant la grammaire pour y supprimer les récursivités gauches directes (sans changer le langage engendré)
 -  Afin d'analyser un mot, il est séparé en un tableau de chaînes de caractères, correspondants aux terminaux séparés par un espace.
 - Pour l'analyse d'un mot, on dispose d'un curseur (analyse_index) indiquant la progression de l'analyse.
 - Les actions ne s'effectuent que si le mot est reconnu. 

## Tests effectués et performances
Dans le répertoire test_running_time, le script python test_running_time.py appel une fonction générant un parser pour une grammaire donnée et exécutant ce parser avec les mots donné. Pour chacun de ces mots, le temps d'exécution, le résultat attendu et le résultat obtenu sont affichés.
L'appel de l’exécutable par l’interpréteur python semble prendre la majorité du temps, car peut importe la grammaire ou la longueur du mot à reconnaître le temps d'exécution reste similaire (cf capture d'écran ci-dessous)
![Capture d'écran de l'exécution du script test_running_time.py](/images/screenshot_running_time.JPG)
**Remarque**: Sur certain système d'exploitation comme Windows on trouve un temps d'exécution plus long pour le premier mot testé de chaque grammaire. Le fichier exécutable est sans doute stocké dans la mémoire vive.

## Limites

 - Lorsque l'on spécifie un mot à analyser, il faut au maximum un espace entre les terminaux
 - Pas de backtracking  
