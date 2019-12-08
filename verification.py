#!/bin/python3
# cd /Documents/GitHub/Applications
# Ce code appartient a :
# - Alpha Oumar KANTE
# - Yaya WANE 
# M2 SICOM 2019-2020

import re
import binascii
from itertools import product
from fonctions import n_premiers, hexadeci, deci, euclide_etendu, crypter, decrypter, calc_2alpha, calc_o_alpha, calc_n_alpha, calc_G, calc_order_Gen, best_generator, hash_fichier
import hashlib
import random
import math

CRED = '\033[91m'
CVRT = '\033[92m'
CEND = '\033[0m'
CBLU = '\033[94m'

listex=[]
listey=[]
kerr=2 # Taille des blocs unitaires a encoder


caracteres=['1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f']
fichier="texte.txt"


nchar=len(caracteres)
bl_size=nchar**kerr
ordre = 0


liste_signature=[]

signedLabel = "_signature"
extension = ".txt"
new = re.sub('\.txt$', '', fichier)
new = new + signedLabel + extension
print(new)

# file_signature = open('new', 'r')
with open(new) as f:
	lines = f.readlines()
for i in lines:
	i = re.sub('\\n$', '', i)
	liste_signature.append(i)
print(liste_signature)

a = int(liste_signature[0])
b = int(liste_signature[1])
modulo = int(liste_signature[2])
key = int(liste_signature[3])
empreintec = liste_signature[4]

Gen=calc_G(a,b,modulo) # Tous les generateurs
best_gen=best_generator(Gen,a,b,modulo,bl_size)
G=best_gen[0]
ordre = best_gen[1]
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

bool_fichier = True
while (bool_fichier == True):


	result = [] # Sequence des codes decryptes
	codec = [] # Sequence des codes cryptes
	indice=0
	message='' # Message decrypte
	messagec='' # Message crypte
	hexamessagec='' # Message hexadecimal crypte
	hexamessage='' # Message hexadecimal decrypte
	bonus=caracteres[0] # Caractere de bourage

	toto=0
	# # Test de parite - caractere de bourage
	# if (len(texte1))%kerr==1:
	# 	print("La chaine est impaire ("+ str(len(texte1)) +")")
	# 	texte1=texte1+bonus
	# 	texte1 = binascii.hexlify(texte1.encode()) # Conversion en hexadecimal
	# else:
	# 	print("La chaine est paire("+ str(len(texte1)) +")")
	# 	texte1 = binascii.hexlify(texte1.encode()) # Conversion en hexadecimal
	indice=0
	result=[]
	# conversion du message chiffre en caracteres hexadecimaux 
	messagec = binascii.hexlify(empreintec.encode())
	# print("messagec = ", messagec)


	# PROCESSUS de decryptage
	# Association des valeurs hexadecimales au points elliptiques
	while (indice<len(messagec)):
		m=messagec[indice:indice+2*kerr] # recuperer l'encodege hexadecimal de chaque bloc
		indice=indice+2*kerr
		# print(m)
		point=(couple[combs.index(m)]) # association avec un point elliptique
		# print(point)
		result.append(point)
	print(result)

	# Decryptage des points elliptques, concatenation et transformation en chaine de caracteres 
	indice=1
	# ma_var= 1
	cle = result[0]
	dcodec = []
	while (indice < len(result)):
		val_temp = (cle,result[indice])
		# print(val_temp)
		
		indice = indice + 2
		decrypte = decrypter(val_temp, bl_size, couple, key)
		dcodec.append(decrypte)

		
		# # Decrypter le message transmis
		index = couple.index(decrypte)
		decm=combs[index]
		# print(" Le message dechiffre est :", decm)
		hexamessage = hexamessage + (str(decm))
		decm = binascii.unhexlify(decm).decode() # Conversion en chaine de caracteres
		message=message+decm
		# # Ajout a la liste
		# result.append(decrypte)

	# Affichage synthetique des resultats 
	print(CVRT+"_________________" * 3 )
	print("_________________    RESULTATS    _________________")
	print(CVRT+"_________________" * 3 + "\n"+CEND)
	print(CVRT+"Codes dechiffrés:"+CEND+" liste de points ",dcodec)
	print(CVRT+"\nMessage hexa dechiffré:"+CEND, hexamessage + "\n")
	print(CVRT+"Message dechiffré:"+CEND, message + "\n\n")

	texte1=hash_fichier(fichier)
	print(CVRT+"\n\nValeur de l'empreinte :"+CEND, str(texte1) + "\n")
	texte2 = message
	if texte1 == texte2:
		print(CVRT+"LA SIGNATURE EST AUTHENTIQUE"+CEND)
	else:
		print(CRED+"LA SIGNATURE EST ERRONEE"+CEND+"\n\n")
	bool_fichier = False

