


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
  * [Lancement des tests](#lancement-des-tests)
  * [Fonctionnement des tests](#fonctionnement-des-tests)
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
Pour spécifier une grammaire, il faut rédiger la grammaire dans un fichier texte sous le format suivant :

    NT : t NT [: Action]
    NT : NT2 [: Action]
    NT2 : a b [: Action]
    ect... 
**L'axiome** de la grammaire est le terminal de la **première règle** décrite (ici, NT).
Exemple de grammaire à fournir en entrée :

    S : a S b : printf("S");
    S : X : printf("S");
    X : c : printf("X")
    X : d
    X : 

**Remarques :** 
Définir une action à effectuer est optionnel. Une action doit être une suite d'instructions C valides, écrite sur une seule ligne.
Par exemple : ```c int i; i = 0; printf("%d\n",i);```



### Lancement rapide
Pour générer un parser par défaut, parsant la grammaire du fichier g_test.txt, et générant un exécutable *parser*  :

    make
    
Pour générer un parser à partir d'une autre grammaire : 

    make gen in=<grammaire_in> out=<nom_executable_out>
    
Pour supprimer les fichiers intermédiaires (.c et .h) : 

    make clean

### Lancement manuel
Le générateur de parser est un script Python générant un code C (le parser). Pour générer le parser :

    python3 gen.py <fichier grammaire> [nom_fichier_c_out=parser]

Ensuite, compilez le fichier C généré : 

    gcc <fichier_généré.c> -o [nom_executable]

### Analyser un mot
Pour lancer le parser généré sur un mot à analyser :

    ./nom_executable <mot à analyser>
Si le mot appartient au langage engendré par la grammaire, **OK** s'affiche, et les actions précisées pour chaque règle sont effectuées.
Sinon, **KO** s'affiche. 

## Précisions techniques

 - Dans le script Python, nous modifions la grammaire pour y supprimer les récursivités gauches directes et les règles inutiles (sans changer le langage engendré).
 - Afin d'analyser un mot, il est séparé en un tableau de chaînes de caractères, correspondants aux terminaux séparés par un espace.
 - Pour l'analyse d'un mot, on dispose d'un curseur (analyse_index) indiquant la progression de l'analyse.
 - Les actions ne s'effectuent que si le mot est reconnu. 

## Tests effectués et performances
### Lancement des tests
Pour lancer les tests : 

    cd test_running_time/
    python3 test_running_time.py
    
ou alors, depuis la racine du projet :

    make test
### Fonctionnement des tests
Dans le répertoire test_running_time, le script python test_running_time.py appelle une fonction générant un parser pour une grammaire donnée et exécutant ce parser avec les mots donnés (situés respectivement dans les dossiers /test_running_time/grammaires et /test_running_time/grammaires/words). Pour chacun de ces mots, le temps d'exécution, le résultat attendu et le résultat obtenu sont affichés.
L'appel de l’exécutable par l’interpréteur python semble prendre la majorité du temps, car peu importe la grammaire ou la longueur du mot à reconnaître le temps d'exécution reste similaire (cf capture d'écran ci-dessous)
![Capture d'écran de l'exécution du script test_running_time.py](/images/screenshot_running_time.JPG)

**Remarque**: Sur certains systèmes d'exploitation comme Windows on trouve un temps d'exécution plus long pour le premier mot testé de chaque grammaire. Le fichier exécutable est sans doute stocké dans la mémoire vive.

## Limites

 - Pas de backtracking
 - Pas de prise en charge de la récursivité gauche indirecte
