#!/usr/local/bin/python
import argparse
from sys import argv

parser = argparse.ArgumentParser()
parser.add_argument("--server","-s", help="server name")
#parser.add_argument("square", help="square given number",type=int)
#parser.add_argument("-v","--verbosity", help="increase output verbosity",action ="store_true")
args = parser.parse_args()
#answer = args.square**2
#if args.verbosity:
#    print "the square of {} equals {}".format(args.square, answer)
#else:
#    print answer
print args.server
print argv[1]
