## William LABBE 4A GPSE TP1
# Réponses aux question du TD_ransomeware 

## Q1 
### Quelle est le nom de l'algorithme de chiffrement ? Est-il robuste et pourquoi ?

L'Algorithme de chiffrement utilisé est un chiffrement XOR, c'est une opération logique entre le fichier à chiffrer et la clé utilisée.
Il n'est pas robuste au sens où il est possible de retrouver la clé de chiffrement si l'on possède un fichier à la fois en clair et chiffré.

## Q2
### Pourquoi ne pas hacher le sel et la clef directement ? Et avec un hmac ?

Hasher directement le sel et la clé affecterait la sécurité du système de chiffrement. Un hmac ne permet pas de dériver une clé mais de vérifier l'intégrité des données.

## Q3
### Pourquoi il est préférable de vérifier qu'un fichier token.bin n'est pas déjà présent ?

Il est préférable de vérifier qu'aucun fichier token.bin n'est présent car il témoignerait d'une précédente utilisation du ransomeware, hors, en remplaçant ce fichier, on compromettrait le déchiffrement de la précédente opération.

## Q4
### Comment vérifier que la clef la bonne ?

Pour ce faire on peut dériver la clé fournie avec le sel et vérifier que l'on ré-obtient le token.