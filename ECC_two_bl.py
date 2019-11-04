#!/bin/python3
# cd /Users/kourakanewane/Desktop/rangement/Cours/M2\ RISM/Securite\ des\ services\ web
# cd \Documents\GitHub\Applications
import random
import math
from itertools import product
import binascii
from fonctions import n_premiers, hexadeci, deci, euclide_etendu, crypter, decrypter, calc_2alpha, calc_o_alpha, calc_n_alpha, calc_G, calc_order_Gen, best_generator

listex=[]
listey=[]
a=4
b=1
lambd=0
modulo=1297
temp=0
i=1
kerr=2 # Taille des blocs unitaires a coder
best_gen=[]
# Calcul du Nombre de blocs
caracteres=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','1','2','3','4','5','6','7','8','9','0']
nchar=len(caracteres)
bl_size=nchar**2
Gen=calc_G(a,b,modulo)
best_gen=best_generator(Gen,a,b,modulo,bl_size)
print('best_gen*********************************************************************',best_gen)
G=best_gen


up = bl_size + 50
n_premiers(bl_size,up)

# Genese des blocs de taille 2
print("\n \n")
combs = [''.join(comb) for comb in product(caracteres, repeat=kerr)]
print(combs)
print("\n \n")
combs = hexadeci(combs)



# G=(1296,1225)
print("\n \n Notre generateur est ",G)
x1=G[0]
y1=G[1]


listex.append(x1)
listey.append(y1)
ordre=1


""" ETAPE 1 : DEFINITION DE (x3,x3) """

val=((3*x1**2)+a)%modulo
#phi_n=37
e=2*y1%modulo

lambda3 = euclide_etendu(e, modulo, val)
print("Lambda =",lambda3)

x3=((lambda3**2)-2*x1)%modulo
y3=(lambda3*(x1-x3)-y1)%modulo
ordre=ordre+1
# Ajout du deuxieme point (2*alpha) a la liste
listex.append(x3)
listey.append(y3)

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
#print(len(listey))


couple = []
for x,y in zip(listex,listey):
 a = (x,y)
 couple.append(a)
print (couple)
## Cryptage
k = 3265477 # cle publique ??
beta = k%modulo
texte="tempo22"
texte1='jevousaimee'
print(len(texte1))
result=[]
indice=0
message=''
messagec=''
hexamessagec='' # Message hexadecimal crypte
hexamessage='' # Message hexadecimal decrypte
bonus='y'

toto=0

if (len(texte1))%kerr==1:
	print("La chaine est impaire")
	texte1=texte1+bonus
	texte1 = binascii.hexlify(texte1.encode()) # Conversion en hexadecimal
else:
	print("La chaine est paire")
	texte1 = binascii.hexlify(texte1.encode()) # Conversion en hexadecimal

#for char in texte1:
while toto!=1:
	m=texte1[indice:indice+2*kerr]
	indice=indice+2*kerr
	print(" Message a chiffrer:", m)
	nombre=combs.index(m)

	point=(couple[nombre]) #equivalent du message dans la courbe elliptique

	crypte = crypter(point,modulo,couple,n_points)
	indexc = couple.index(crypte)
	cm=combs[indexc]
	print(" Le message chiffre est :", cm)
	hexamessagec = hexamessagec + (str(cm))
	cm = binascii.unhexlify(cm).decode() # Conversion en chaine de caracteres
	messagec=messagec+cm
	decrypte = decrypter(crypte,modulo,couple,n_points)
	index = couple.index(decrypte)
	decm=combs[index]
	print(" Le message dechiffre est :", decm)
	hexamessage = hexamessage + (str(decm))
	decm = binascii.unhexlify(decm).decode() # Conversion en chaine de caracteres
	message=message+decm

	result.append(decrypte)
	if(indice>=len(texte1)):
		toto=1

print("Code dechiffre: liste de points ",result)
print("Message hexa chiffre:", hexamessagec)
print("Message chiffre:", messagec)
print("Message hexa dechiffre:", hexamessage)
print("Message dechiffre:", message)