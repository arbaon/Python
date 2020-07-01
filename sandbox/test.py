#!/usr/local/bin/python
import re # regex
import os
import sys
# store the path of the script..
my_path = os.path.abspath(sys.argv[0])
print "absolute path of this script:",my_path
# regex matching
regexp_test = re.compile(r"^([0-9]+)")
result_1 = regexp_test.match("B999")
result_2 = regexp_test.match("919")
print result_1,result_2
def text_block():
    """
    ASDFDSAFADSFSDAFAS
    ASFDFASDFDSAFDSAFDAS
    2r23rerdsfasdfasdfdsf
    """
text_block()
