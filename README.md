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
Parler du script lançant les tests, expliquer les résultats (screen ?)

## Limites
Plusieurs espaces entre deux non terminaux = Segfault
