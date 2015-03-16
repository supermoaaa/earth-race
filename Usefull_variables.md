# Configuration des joueurs #
```python

bge.logic.conf=[
[[ namePlayer, playerType, keys, vehicle, wheels ]],
[[ vehicle, [ nameParams, confParams ] ]],
[[ wheels, [ nameParams, confParams ] ]]
]```

L'identifiant de joueur est l'id qui correspond à la position dans la liste de joueur.

Le premier paramètre d'un véhicule ou d'une roue est loaded, et il permet de savoir s'il est fini d'être charger.

The player ID is the position in the list of players.

the keys format is:
```python

[  [ 'accelerate', '122' ],
[ 'reverse', '115' ],
[ 'left', '113' ],
[ 'right', '100' ],
[ 'brake', '32' ],
[ 'boost', '129' ],
[ 'upGear', '101' ],
[ 'downGear', '97' ]
]```

# Placement des joueurs #

```python

bge.logic.dispPlayers=[mode = 3, namePlayer1, namePlayer2, namePlayer3, namePlayer4]
```
Le nombre de namePlayer correspond au nombre de joueurs pour la partie.
La variable ainsi initialisé donne l'affichage:

|namePlayer1|namePlayer2|
|:----------|:----------|
|namePlayer3|namePlayer4|

le mode correspond au type de split sur l'écran
| **mode** | **type de split** |
|:---------|:------------------|
| 0 | plein ecran |
| 1 | 2 joueurs horizontal |
| 2 | 2 joueurs vertical |
| 3 | 4 joueurs |
| 4 | 3 joueurs masque haut gauche|
| 5 | 3 joueurs masque haut droite|
| 6 | 3 joueurs masque bas droite|
| 7 | 3 joueurs masque bas gauche|

We use list for bigest performance, memory use.

# Configuration générale #

```python

bge.logic.generalConf = [True, rd.getAnisotropicFiltering(), 25, 50, 'sun', 'Francais']```

Donc dans l'ordre:

generalConf 0 activation de l'effet mirror

generalConf 1 niveau d'Anisotropic

generalConf 2 gestion du début du brouillard

generalConf 3 gestion de la fin du brouillard

generalConf 4 gestion de la météo

generalConf 5 langue de l'interface (correspond au nom de fichier de langue)

# Configuration du son #

```python

bge.logic.sound = [50, 50, "electro"]```

Donc dans l'ordre:

sound 0 volume des effets sonores (bruit du moteur, crissement de pneu…)

sound 1 volume de la musique

sound 3 nom du dossier des musiques à jouer

# variable interne du menu #

elle sont utiliser exclusivement dans le menu


les listes:

gl.listeRadio ==> liste des radios

gl.listMaps ==> liste des circuits

gl.lstVoiture ==> liste des voitures

gl.lstRoue ==> liste des roues