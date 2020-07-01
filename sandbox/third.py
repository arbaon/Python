from sys import argv
script, filename = argv
target = open(filename,'w')
target.truncate
target.write("the first line \n")
target.write("the second line \n")
target.close()
