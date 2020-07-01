#!/usr/bin/python
import sys
total = len(sys.argv)
if total == 3:
    aone,atwo,athree,afour = argv
    print "one:",aone
    print "two:",atwo
    print "three:",athree
    print "four:",afour

hello='hello'
world='world'
ten=10
five=5
helwld= "%s %s" % (hello,world)
formatter = "%r %r %r"
print ("%s" % world)
print "hello world."
print "%s %s %d %d" % (hello,world,five,ten)
print five + ten
print ten / five
print five * ten
print ten - five
print ten > five
print five > ten
print helwld
print "." * 10
test1="t"
test2="e"
test3="s"
test4="t"
print test1 + test2 + test3 +test4
print formatter % (1,2,3)
print "one\ntwo\nthree\nfour\n"
print "test input :",
test=raw_input()
print test
test2=raw_input("test input v2 :")
print test2
