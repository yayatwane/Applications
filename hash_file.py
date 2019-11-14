#!/usr/bin/python3
import hashlib

hasher = hashlib.md5()
nom='texte'
nom=nom+'.txt'
print(nom)
with open(nom, 'rb') as afile:
    buf = afile.read()
    hasher.update(buf)
print(hasher.hexdigest())