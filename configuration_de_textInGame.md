La structure du fichier textInGame.json est très simple, c'est un tableau de tableau.
Chacun des tableaux donnes les informations sur un bloc de texte, ainsi le premier tableau c'est pour le rapport de vitesse, le deuxième pour les checkpoints, le troisième pour les tours de piste, le quatrième pour le temps.
La première info dans un tableau est pour positionner le texte en X, la deuxième en Y, et la troisième c'est la taille.
La première information peut être "under" pour indiquer que le texte dois être centrer en dessous du texte précédent; dans ce cas, la deuxième information défini l'espace à ajouter verticalement entre les deux textes.

Ainsi à l'heure ou j'écris cette documentation, la configuration par défaut est:
[
> [
> > 0.805,
> > 0.141,
> > 0.08

> ],
> [
> > 0.5,
> > 0.932432,
> > 0.05

> ],
> [
> > "under",
> > 0.0,
> > 0.05    ],

> [
> > "under",
> > 0.0,
> > 0.05    ]
]
