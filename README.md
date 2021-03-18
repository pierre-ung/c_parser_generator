# Projet Automates et Langages
## Sommaire
- [Présentation](#présentation)
- [Utilisation](#utilisation)
  * [Pré-requis](#pré-requis)
  * [Spécification de la grammaire](#spécification-de-la-grammaire)
  * [Lancement rapide](#lancement-rapide)
  * [Lancement personnalisé](#lancement-personnalisé)
- [Précisions techniques](#précisions-techniques)
- [Tests effectués et performances](#tests-effectués-et-performances)
- [Limites](#limites)


## Présentation
Dans le cadre de l'U.E Automates et Langages (INSA Toulouse), nous avons réalisé un programme générant des parser de Context-Free Grammar.
**Groupe** : 4IR - B1
**Étudiants** : Alexandre Gonzalvez, Benjamin Vendeville, Jasper Güldenstein, Marino Benassai, Mikhail Zakharov, Fabien Castilla, Pierre Ung

## Utilisation
### Pré-requis
Version de python
### Spécification de la grammaire
Expliquer le format à utiliser pour spécifier une grammaire ( rédirer une "grammaire type" comme T : ... : Action)

### Lancement rapide
Expliquer ce que fait le makefile

    make

### Lancement personnalisé
Le générateur de parser est un script Python générant un code C (le parser). Pour générer .... 

    python gen.py <fichier grammaire> [fichier_sortie=parser]

Ensuite, compiler ... 

    gcc <fichier_généré.c> -o [nom_executable]

Pour lancer le parser ..... 

    ./nom_executable <mot à analyser>

## Précisions techniques
Traitement de la grammaire (Suppression récursivité gauche directe)
Dans le code C : le mot est split en un tableau de terminaux, puis analysé
autre ???
Gestion des actions

## Tests effectués et performances
Dans le répertoire test_running_time, le script python test_running_time.py execute une fonction générant un parser pour une grammaire donnée et l'exécutant avec les mots. Pour chacun de ces mots, le temps d'exécution est affiché.
L'appel de l'executable semble prendre la majorité du temps, car peut importe la grammaire ou la longueur du mot à reconnaître le temps d'exécution reste similaire (cf capture d'écran ci-dessous)
![Capture d'écran de l'exécution du script test_running_time.py](/images/screenshot_running_time.JPG)
Remarque: Sur certain système d'exploitation comme windows on trouve un temps d'exécution plus long pour le premier mot testé de chaque grammaire.
## Limites
Plusieurs espaces entre deux non terminaux = Segfault
