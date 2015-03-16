# Introduction #

Cette section énumère les règles a suivre pour crée des roues compatibles avec HSR.


# Mise en place #

Vous devez dans un premier temps crée un dossier portant le noms de la roue.

Placez se dossier dans objects\wheels\

chaque élément du dossier sera décrit dans les sections suivantes.

# Le modèle 3D #

c'est un fichier .blend crée avec le logiciel libre Blender **http://www.blender.org/**

Il doit porter lui aussi le nom de la roue.

exemple:
NomDeMaRoue.blend


# Le fichier de configuration #

Comme précédemment il doit porter le nom de la roue.
avec l’extension  .cfg

exemple:
NomDeMaRoue.cfg

> C'est un fichier texte dans un format simple

exemple:
```
wheel = Circle
decoration = Plane
damp = 15000
friction = 2
max_force = 70000
steer_rate = 2.0
steer_limit = 0.6
brake = 3500
skidSound = pneu.mp3
```
  * "`wheel`" permet de désigner l'objet principal

  * "`decoration`" permet de désigner des objets de décoration qui ne doivent pas tourner avec la roue

  * "`damp`" permet de définir le rebond des amortisseurs

  * "`friction`" permet de définir la friction des roues

  * "`max_force`" permet de définir l'adhérence des roues

  * "`steer_rate`" permet de définir la vitesse de rotation des roues directionnelles

  * "`steer_limit`" permet de définir l'angle maximum de rotation des roues directionnelles

  * "`brake`" permet de définir la force de freinage

  * "`skidSound`" permet de définir le nom du fichier de son pour les dérapages


# Les textures #

Vous devrez placer  vos  textures dans le dossier.

Utiliser le format png pour les textures avec un canal alpha
et jpg pour les autres

Leurs dimensions doivent êtres des puissances de 2 et ne pas dépasser 1024x1024 .

De façon générale éviter de faire un dossier trop lourd ou les performances du jeu vont énormément baisser.