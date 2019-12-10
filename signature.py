#!/bin/python3
# cd /Documents/GitHub/Applications
# Ce code appartient a :
# - Alpha Oumar KANTE
# - Yaya WANE 
# M2 SICOM 2019-2020

import random
import hashlib
import math
from itertools import product
import binascii
from fonctions import n_premiers, hexadeci, deci, euclide_etendu, crypter, decrypter, calc_2alpha, calc_o_alpha, calc_n_alpha, calc_G, calc_order_Gen, best_generator, hash_fichier
import re

CRED = '\033[91m'
CVRT = '\033[92m'
CEND = '\033[0m'
CBLU = '\033[94m'

listex=[]
listey=[]
kerr=2 # Taille des blocs unitaires a encoder


caracteres=['1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f']
fichier = str(input("Entrez le nom du fichier que vous souhaitez signer: "))
texte1=hash_fichier(fichier)

nchar=len(caracteres)
bl_size=nchar**kerr
ordre = 0
a=0
b=0
while a==0:
	a=input("Entrez la valeur de a: ")
	if a.isdigit():
		break
	else:
		print(CRED+"La valeur saisie doit etre un entier positif. \nSaisissez une valeur numerique de a..."+CEND)
		a=0
while b==0:
	b=input("Entrez la valeur de b: ")
	if b.isdigit():
		break
	else:
		print(CRED+"La valeur saisie doit etre un entier positif. \nSaisissez une valeur numerique de b..."+CEND)
		b=0

# b=int(input("Entrez la valeur de b: "))
a=int(a)
b=int(b)
print("a: ", a)
print("b: ", b)
liste_signature=[]
liste_signature.append(a)
liste_signature.append(b)

lambd=0

# Operations sur le modulo - primalite, calcl de tous les generateurs, ordres, generateur optimal 

while(ordre < bl_size):

	print("\nIl y a "+str(nchar)+" caracteres a encoder sur des blocs de taille "+str(kerr)+".")
	print("Nous avons donc besoin d'au moins "+ str(bl_size) +" points elliptiques. \n")
	# Cette section permet une assistance au choix du modulo
	up = bl_size + 50
	n_premiers(bl_size,up)
	modulo = int(input("\nEntrez la valeur du modulo (voir liste):  "))
	liste_premiers = n_premiers(2,modulo)
	if modulo in liste_premiers:
		print("Le Modulo ", modulo, " est premier et donc valide.")
		temp=0
		i=1
		best_gen=[]

		#  En fonction de a, b, et modulo,
		Gen=calc_G(a,b,modulo) # Tous les generateurs
		best_gen=best_generator(Gen,a,b,modulo,bl_size) # Calcul du meilleur generateur
		print('best_gen*********************************************************************',best_gen)
		ordre = best_gen[1]
		print("Ordre: ",ordre)
		if len(best_gen[0]) == 0:
			print(CRED + "Error : Le modulo que vous avez choisi ne permet pas de coder tous vos points. \n Tentez avec une valeur plus grande " + CEND)
			ordre = 0
		G=best_gen[0]
		print("Generateur",G)
		if ordre < bl_size:
			print(CRED + "Error : Le modulo que vous avez choisi ne permet pas de coder tous vos points. \n Tentez avec une valeur plus grande " + CEND)
			ordre = 0
		else:
			break
	else:
		print(CRED + "Error : Le modulo que vous avez choisi n'est pas un nombre premier." + CEND)
		ordre = 0

liste_signature.append(modulo)
# Genese des blocs de taille 2
print(CVRT+"\n\nListe des blocs de taille 2: "+CEND)
combs = [''.join(comb) for comb in product(caracteres, repeat=kerr)]
print(combs)
print("\n \n")
combs = hexadeci(combs)

# Ajout du generateur comme premier terme de notre liste
print("\n\nNotre generateur est ",G)
x1=G[0]
y1=G[1]
listex.append(x1)
listey.append(y1)
ordre=1

# Calcul de 2 * G
# Calcul de lambda
val=((3*x1**2)+a)%modulo
e=2*y1%modulo
lambda3 = euclide_etendu(e, modulo, val)
print("Lambda =",lambda3)
# Formule 2 * G
x3=((lambda3**2)-2*x1)%modulo
y3=(lambda3*(x1-x3)-y1)%modulo
ordre=ordre+1
# Ajout du deuxieme point a la liste
listex.append(x3)
listey.append(y3)

# Calcul des autres alpha
tempo=0
while tempo!=1:
	x2=x3
	y2=y3
	val1=(y2-y1)%modulo
	e1=(x2-x1)%modulo
	lambda1 = euclide_etendu(e1, modulo, val1)
	x3=((lambda1**2)-x1-x2)%modulo
	y3=(lambda1*(x1-x3)-y1)%modulo
	if (x3 == G[0]):
		listex.append(x3)
		listey.append(y3)
		ordre=ordre+1
		print("Dernier point : (", x3 ,",",y3 ,")")
		tempo=1
	else:
		listex.append(x3)
		listey.append(y3)
		ordre=ordre+1
#print(listex)
#print(listey)
n_points=len(listex)
print(CVRT+"\n\nNombre de points elliptiques : "+str(n_points)+CEND)



couple = []
for x,y in zip(listex,listey):
 a = (x,y)
 couple.append(a)
print (couple)
## Cryptage
# k = 3265477 # cle privee
l = random.randint(1,1000000) # cle publique
liste_signature.append(l)
bool_fichier = True
while (bool_fichier == True):
	print(CVRT+"\n\nMessage initial :"+CEND, str(texte1) + "\n")
	mess_initial =texte1

	result = [] # Sequence des codes decryptes
	codec = [] # Sequence des codes cryptes
	indice=0
	message='' # Message decrypte
	messagec='' # Message crypte
	hexamessagec='' # Message hexadecimal crypte
	hexamessage='' # Message hexadecimal decrypte
	bonus=caracteres[0] # Caractere de bourage

	toto=0
	# Test de parite - caractere de bourage
	if (len(texte1))%kerr==1:
		print("La chaine est impaire ("+ str(len(texte1)) +")")
		texte1=texte1+bonus
		texte1 = binascii.hexlify(texte1.encode()) # Conversion en hexadecimal
	else:
		print("La chaine est paire("+ str(len(texte1)) +")")
		texte1 = binascii.hexlify(texte1.encode()) # Conversion en hexadecimal

	# PROCESSUS de Cryptage de la chaine de caracteres
	# Cryptage puis concatenation des valeurs hexadecimales associees
	while toto!=1:
		k = random.randint(1, 1000000)
		m=texte1[indice:indice+2*kerr]
		indice=indice+2*kerr
		# print(" Message a chiffrer:", m)
		# Crypter notre chaine de caractere
		nombre=combs.index(m)
		point=(couple[nombre]) # Point equivalent du message dans la courbe elliptique
		crypte = crypter(point, bl_size, couple, k, l)
		print(crypte)
		# ajout a la liste
		codec.append(crypte)
		if(indice>=len(texte1)):
			toto=1

	for code in codec:
		# print (code)
		var1 = code[0]
		v1 = couple.index(var1)
		cm1 = combs[v1]
		var2 = code[1]
		v2 = couple.index(var2)
		cm2 = combs[v2]
		hexamessagec = hexamessagec + (str(cm1)) # Concateneation a la chaine hexadecimale
		cm1 = binascii.unhexlify(cm1).decode() # Conversion en chaine de caracteres
		messagec=messagec+cm1 # Concatenation a la chaine de caracteres
		hexamessagec = hexamessagec + (str(cm2)) # Concateneation a la chaine hexadecimale
		cm2 = binascii.unhexlify(cm2).decode() # Conversion en chaine de caracteres
		messagec=messagec+cm2 # Concatenation a la chaine de caracteres
	# Sortie de la boucle
	resultc = messagec
	liste_signature.append(resultc)
	# print(liste_signature)
	# Affichage synthetique des resultats 
	print(CVRT+"_________________" * 3 )
	print("_________________    RESULTATS    _________________")
	print("_________________" * 3 + "\n"+CEND)
	print(CVRT+"Message initial: "+CBLU+ str(mess_initial)+CEND + "\n\n")
	print(CVRT+"Codes chiffrés:"+CEND+" liste de points ",codec)
	print(CVRT+"\nMessage hexa chiffré:"+CEND, hexamessagec + "\n")
	print(CVRT+"Message chiffré:"+CEND, resultc)
	

	signedLabel = "_signature"
	extension = ".txt"
	new = re.sub('\.txt$', '', fichier)
	new = new + signedLabel + extension
	# print(new)
	print("\nVoici la signature : "+ CVRT+ str(liste_signature) + CEND)

	MyFile=open(new,'w+')
	for element in liste_signature:
		MyFile.write(str(element))
		MyFile.write('\n')
	MyFile.close()
	

	# CETTE PARTIE EST DESTINEE A UNE AUTRE APPLICATION
	print(CVRT+"\nSouhaitez vous signer un autre document ?"+CEND)
	reponse = (str(input("Reponse (Oui/Non): "))).lower()
	# print(reponse)

	if (reponse=="non"):
		bool_fichier = False
		break
	elif (reponse=="oui"):
		fichier = str(input("Entrez le nom de votre fichier: "))
		texte1=hash_fichier(fichier)
		bool_fichier = True
	
	