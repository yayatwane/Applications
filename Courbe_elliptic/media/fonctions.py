#!/bin/python3
import binascii
import math
import hashlib

CVRT = '\033[92m'
CBLU = '\033[94m'
CEND = '\033[0m'

# Calcul des modulos possibles
def n_premiers(lower,upper):
	print("Les nombres premiers entre",lower,"et",upper,"sont:")
	prime=[]
	for num in range(lower,upper + 1):
	   # prime numbers are greater than 1
	   if num > 1:
	       for i in range(2,num):
	           if (num % i) == 0:
	               break
	       else:
	           #print(num)
	           prime.append(num)
	print(CVRT + str(prime) + CEND)
	return prime

# Conversion en hexadecimal
def hexadeci(listed):
	listeh=[]
	for uni in listed:
		hexa = binascii.hexlify(uni.encode())
		listeh.append(hexa)
	print(listeh)
	return listeh

# Conversion en decimal
def deci(listeh):
	listed=[]
	for uni in listeh:
		deci = binascii.unhexlify(uni).decode()
		listed.append(deci)
	print(listed)
	return listed

# Algorithme dEuclide etendu 
def euclide_etendu(e, phi_n, val) :
  d = 1
  temp = (e*d)%phi_n
  while(temp != val):
    d = d+1
    temp = (e*d)%phi_n
  return d

# Cryptage
def crypter(m, phi_n, tab, k, kpv) :
	cpt=[]
	## Cryptage
	print("code a chiffrer:" , m)
	y1=tab[(k-1)%phi_n]
	y2=tab.index(m)+((k-1)*(kpv-1))
	indice2 = y2%phi_n
	y2=tab[indice2]
	cpt=(y1,y2)
	print("code chiffre:", cpt)

	return cpt
# Decryptage
def decrypter(m, phi_n, tab, kpv) :
	dcpt=[]
	y1 = m[0]
	y2 = m[1]
	indice1=tab.index(y1)
	indice2=tab.index(y2)
	dec = (indice2-(kpv-1)*indice1)%phi_n
	dcpt=tab[dec]
	# print("code dechiffre:", dcpt)
	return dcpt

# Calcul de 2 alpha
def calc_2alpha(x1,y1,mod,a):
	lamda=0	
	e=2*y1%mod
	omega = (3*(x1**2)+a) % mod
	lamda = euclide_etendu(e,mod,omega)
	x3=(lamda**2-2*x1)%mod
	y3=(lamda*(x1-x3)-y1)%mod
	temp=[]
	temp.append(x3)
	temp.append(y3)
	return temp

# Calcul des multiples de alpha [3alpha:end]
def calc_o_alpha(x1,y1,x2,y2,mod,a):
	lamda=0	
	e=(x2-x1) % mod
	omega = (y2-y1) % mod
	lamda = euclide_etendu(e,mod,omega)
	x3=(lamda**2-x1-x2)%mod
	y3=(lamda*(x1-x3)-y1)%mod
	temp=[]
	temp.append(x3)
	temp.append(y3)
	return temp

# Calcul des generateurs
def calc_G(a,b,mod):
	x=1
	entier=0
	# counter=0
	Generator=[]
	while x<mod:
		y=1
		while y<mod:
			rp=((x**3)+(a*x)+b)%mod
			lp=(y*y)%mod
			if rp==lp:
				# counter=counter+1
				print ("\n( le generateur est ",x,",",y,")")
				temp=[]
				if y!=0:

					temp.append(x)
					temp.append(y)
					Generator.append(temp)
			y=y+1
		x=x+1
	# counter=(counter*2)+1
	# print('counter____________________________________________________________',counter)
	return Generator

# Calcul de n alpha
def calc_n_alpha(G,n,mod,a):
	n_alpha=[]
	two_alpha=[]
	current_alpha=[]
	two_alpha=calc_2alpha(G[0],G[1],mod,a)
	cur_a=two_alpha
	if n==2:
		n_alpha=two_alpha
	else:
		i =2	
		while i<n:
			cur_a=calc_o_alpha(G[0],G[1],cur_a[0],cur_a[1],mod,a)
			i=i+1
		n_alpha=cur_a
	print('n_alpha________________________________________',n_alpha)
	return n_alpha

# Calcul de lOrdre d'un generateur
def calc_order_Gen(G,a,b,mod):
	x1=G[0]
	y1=G[1]
	all_alpha={}
	all_alpha['a']=G
	current_alpha=[]
	cur_a=calc_2alpha(G[0],G[1],mod,a)
	all_alpha['2a']=cur_a
	i =2
	while 1:
		#all_alpha.append(cur_a)
		# all_alpha[str(i)+'a']=cur_a
		i=i+1
		if cur_a[0] == G[0]:
			#all_alpha.append(cur_a)
			#print('cur_a___________________1',cur_a)
			#all_alpha.append(cur_a)
			break
		else :
			cur_a=calc_o_alpha(G[0],G[1],cur_a[0],cur_a[1],mod,a)
	# print ('all_alpha',all_alpha)
	#print('_________________________________________________________________')
	# print('ordre de (' + str(G[0])+' , ' + str(G[1]) +') '+str(len(all_alpha)))
	#print('ordre de (' + str(G[0])+' , ' + str(G[1]) +') '+str(i))
	# order=len (all_alpha)
	return i

# Calcul du meilleur generateur
def best_generator(Gen,a,b,mod,bs):
	b_size=0
	order=0
	b_gen=[]
	print('Gen_0__________________________________',Gen[0],"\n")
	print(CBLU+"Veuillez patienter... Le calcul du meilleur generateur est en cours"+CEND)
	# b_size=mod+2*(mod**(1/2))+1
	b_size=mod+2*math.sqrt(mod)+1
	# b_size=calc_order_Gen(Gen[0],a,b,mod)
	for t in Gen:
		order=calc_order_Gen(t,a,b,mod)
		# print('order__________________________________',order)

		if order>=bs:
			if order<=b_size:
				b_size=order
				# print('b_size__________________________________',b_size)
				b_gen=t
	print('bs__________________________________',bs)
	print('b_size__________________________________',b_size)
	print('b_gen__________________________________',b_gen)
	return b_gen,b_size

# Fonction de hashage de fichier
def hash_fichier(nom_fichier):
	hasher = hashlib.md5()
	# nom_fichier=nom_fichier+".txt"
	# print(nom)
	with open(nom_fichier, 'rb') as afile:
	    buf = afile.read()
	    hasher.update(buf)
	    res=hasher.hexdigest()
	    print(res)
	return res