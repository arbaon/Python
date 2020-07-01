from sys import argv
from os.path import exists
script, fileone, filetwo = argv
txtone = open(fileone)
dataone = txtone.read()
print txtone.read()

datatwo = open(filetwo,'w')
datatwo.write(dataone)
datatwo.close()
txtone.close()
print exists(filetwo)
filename = raw_input("> ")
txt_again = open(filename)
print txt_again.read()
