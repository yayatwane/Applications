#!/bin/python3
# cd /Documents/GitHub/Applications
# M2 SICOM
# - Alpha Oumar KANTE
# - Yaya WANE 

import random
import hashlib
import math
from itertools import product
import binascii
from fonctions import n_premiers, hexadeci, deci, euclide_etendu, crypter, decrypter, calc_2alpha, calc_o_alpha, calc_n_alpha, calc_G, calc_order_Gen, best_generator, hash_fichier

CRED = '\033[91m'
CVRT = '\033[92m'
CEND = '\033[0m'

listex=[]
listey=[]
kerr=2 # Taille des blocs unitaires a encoder
var_bool=0
possibilites = {
	1: 'Caracteres alphabetiques - sans espace',
	2: 'Caracteres alphabetiques - avec espaces, points et virgules',
	3: 'Caracteres alphanumeriques - sans espace',
	4: 'Caracteres alphanumeriques - avec espaces, points et virgules',
	5: 'Caracteres numeriques',
	6: 'Caracteres de hash - hexadecimal [0..9-a..f]'
}
while (var_bool==0):
	programme = input(CVRT+'\n\nChoisissez le programme a implementer: \n - [1] Caracteres alphabetiques - sans espace \n - [2] Caracteres alphabetiques - avec espaces, points et virgules \n - [3] Caracteres alphanumeriques - sans espace \n - [4] Caracteres alphanumeriques - avec espaces, points et virgules \n - [5] Caracteres numeriques \n - [6] Caracteres de hash - hexadecimal [0..9-a..f] \n A vous: '+CEND)
	programme=int(programme)
	if (programme==1):
		caracteres=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
		texte1="headdonaddon"
		var_bool=1
	elif (programme==2):
		caracteres=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',' ','.',',']
		texte1="headdon addon"
		var_bool=1
	elif (programme==3):
		caracteres=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','1','2','3','4','5','6','7','8','9','0']
		texte1="alphayayamaster2sicom2019"
		var_bool=1
	elif (programme==4):
		caracteres=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','1','2','3','4','5','6','7','8','9','0',' ','.',',']
		texte1="alpha yaya, master 2 sicom 2019."
		var_bool=1
	elif (programme==5):
		caracteres=['1','2','3','4','5','6','7','8','9','0']
		texte1="06177992264"
		var_bool=1
	elif (programme==6):
		caracteres=['1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f']
		texte1="b86caad0f27a5668a41deb4ef89b6874"
		var_bool=1
	else:
		print(CRED+"Entree invalide... Try smarter! Les possibilités sont claires:)"+CEND)
# La taille de votre modulo dependra du nombre de caracteres a coder
# caracteres=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','_']
# caracteres=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','1','2','3','4','5','6','7','8','9','0']



nchar=len(caracteres)
bl_size=nchar**kerr
ordre = 0
# a=4
# b=1
a=int(input("Entrez la valeur de a: "))
b=int(input("Entrez la valeur de b: "))
lambd=0
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
		print(ordre)
		if len(best_gen[0]) == 0:
			print(CRED + "Error : Le modulo que vous avez choisi ne permet pas de coder tous vos points. \n Tentez avec une valeur plus grande " + CEND)
			ordre = 0
		G=best_gen[0]
		print(G)
		if ordre < bl_size:
			print(CRED + "Error : Le modulo que vous avez choisi ne permet pas de coder tous vos points. \n Tentez avec une valeur plus grande " + CEND)
			ordre = 0
		else:
			break
	else:
		print(CRED + "Error : Le modulo que vous avez choisi n'est pas un nombre premier." + CEND)
		ordre = 0

# Genese des blocs de taille 2
print("\n \n")
combs = [''.join(comb) for comb in product(caracteres, repeat=kerr)]
print(combs)
print("\n \n")
combs = hexadeci(combs)

# Ajout du generateur comme premier terme de notre liste
print("\n \n Notre generateur est ",G)
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
print("Nombre de points :",n_points)



couple = []
for x,y in zip(listex,listey):
 a = (x,y)
 couple.append(a)
print (couple)
## Cryptage
k = 3265477 # cle privee
l = 23 # cle publique
beta = k%modulo

print(texte1)
print(CVRT+"\nMessage initial :"+CEND, str(texte1) + "\n")
# texte1="headdonaddon"
# texte1="alphayayamaster2sicom2019"
# texte="sicom2019"
# print(len(texte1))
result = [] # Sequence des codes decryptes
codec = [] # Sequence des codes cryptes
indice=0
message='' # Message decrypte
messagec='' # Message crypte
hexamessagec='' # Message hexadecimal crypte
hexamessage='' # Message hexadecimal decrypte
bonus=caracteres[0] # Caractere de bourage

toto=0

if (len(texte1))%kerr==1:
	print("La chaine est impaire ("+ str(len(texte1)) +")")
	texte1=texte1+bonus
	texte1 = binascii.hexlify(texte1.encode()) # Conversion en hexadecimal
else:
	print("La chaine est paire("+ str(len(texte1)) +")")
	texte1 = binascii.hexlify(texte1.encode()) # Conversion en hexadecimal


while toto!=1:
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
		# Transformation de la liste de points elliptiques en chaine hexadecimale
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
# print(resultc)
indice=0
result=[]
# conversion du message chiffre en caracteres hexadecimaux 
messagec = binascii.hexlify(messagec.encode())
# print("messagec = ", messagec)

while (indice<len(messagec)):
	m=messagec[indice:indice+2*kerr] # recuperer l'encodege hexadecimal de chaque bloc
	indice=indice+2*kerr
	# print(m)
	point=(couple[combs.index(m)]) # association avec un point elliptique
	# print(point)
	result.append(point)
print(result)
indice=1
# ma_var= 1
cle = result[0]
dcodec = []
while (indice < len(result)):
	val_temp = (cle,result[indice])
	# print(val_temp)
	
	indice = indice + 2
	decrypte = decrypter(val_temp, bl_size, couple, l)
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
print("_________________" * 3 + "\n"+CEND)
print(CVRT+"Codes chiffrés:"+CEND+" liste de points ",codec)
print(CVRT+"\nMessage hexa chiffré:"+CEND, hexamessagec + "\n")
print(CVRT+"Message chiffré:"+CEND, resultc)
print(CVRT+"_________________" * 3 + "\n"+CEND)
print(CVRT+"Codes dechiffrés:"+CEND+" liste de points ",dcodec)
print(CVRT+"\nMessage hexa dechiffré:"+CEND, hexamessage + "\n")
print(CVRT+"Message dechiffré:"+CEND, message + "\n")

# bool_fichier = True


fichier = str(input("Entrez le nom de votre fichier: "))
# fichier = raw_input("Entrez le nom de votre fichier: ")
hash_fichier(fichier)
