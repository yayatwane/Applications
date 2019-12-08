# Applications
Class work and brain food
____________________________________________________________________________________________________________
https://www.smalsresearch.be/elliptic-curve-cryptography-tutoriel2/
https://csrc.nist.gov/csrc/media/events/workshop-on-elliptic-curve-cryptography-standards/documents/papers/session1-miele-paper.pdf
https://www.informatik.tu-darmstadt.de/cdc/home_cdc/index.en.jsp
https://pypi.org/project/fastecdsa/
____________________________________________________________________________________________________________
Target: Obtenir a partir d'une courbe elliptique, tous les parametres pour avoir un nombre de points optimal
____________________________________________________________________________________________________________
1) Done - Input: a, b, t(taille du block unitaire a chiffrer)	  - Uploaded 
2) Done - Calcul du nombre de possibilités de blocs $bl_size      - Uploaded
3) Done - Generer les blocs a partir de la liste de {caracteres}  - Uploaded
4) Done - Coder en ascii puis stocker dans la liste de {blocs}    - Uploaded
5) Done - Générer notre $modulo tel que modulo > bl_size          - Uploaded
6) Done - Choisir un générateur tel que ordre(G) > bl_size		  - Uploaded		
7) Done - Associer le blocs[i] à coder à un point elliptique      - Uploaded
8) Done - Chiffrer le bloc                                        - Uploaded
9) Done - Déchiffrer le bloc                                      - Uploaded
10)Done - Mise en fonction des operations d'addition			  - Uploaded
11)Done - Cryptage hexadecimal des blocs ascii avant envoi		  - Uploaded
12)Done - Verification du modulo (primalite et ordre maximal)	  - Uploaded
13)Done - Affichage d'une liste indicative de modulos eventuels   - Uploaded
14)Done - Mise en fonction generale des fonctionnalités			  - Uploaded
15)Done - Verificatio de a et b (valeur entiere) 				  - Uploaded
16)Done - Signature de documents								  - Uploaded
17)Done - Verification de la Signature 							  - Uploaded
____________________________________________________________________________________________________________
Tests et Utilisation
____________________________________________________________________________________________________________
Lancer la commande:			python ECC_two_bl.py
		(sous MAC)			python3 ECC_two_bl.py
Un menu vous guidera pour la suite de la procedure; 6 options sont possibles 

 - [1] Caracteres alphabetiques - sans espace; (26 caracteres)
 - [2] Caracteres alphabetiques - avec espaces, points et virgules; (29 caracteres)
 - [3] Caracteres alphanumeriques - sans espace; (36 caracteres)
 - [4] Caracteres alphanumeriques - avec espaces, points et virgules; (39 caracteres)
 - [5] Caracteres numeriques; (10 caracteres)
 - [6] Caracteres de hash - hexadecimal [0..9-a..f]; (16 Caracteres)

Pour chaque possibilité vous aurez à saisir le les valeurs de a, b et du modulo.
Ne vous inquietez pas, vous serez guidés dans le choix du modulo.
Pour chaque option, une chaine de caracteres est definie dans la premier boucle while.

Notre script appelle le fichier de fonctions nommé fonctions.py
Le code est commenté de maniere assez detaillée et la navigation a travers le code est assez facile.
____________________________________________________________________________________________________________
Pour signer un document, executer le fichier signature.py. Un fichier de signature sera genere.
Il contiendra les valeurs de a, b, modulo, la cle publique et l'empreinte chiffree.
Le fichier verification.py permet de comparer l'empreinte (issu du hachage du fichier) et l'empreinte 
obtenue apres dechiffrement de l'empreinte chiffree (issue du fichier de signature)
