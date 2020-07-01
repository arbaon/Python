#!/usr/bin/python
import MySQLdb
class Sequence:
    def __init__(self):
        self.Sseq = [0.8,0.8,0.2]
        self.Sval = [0,0]
	self.rst = 0
	self.ubeat = [0,0]
	self.weights = [0,0,0,0,0,0]
    def runseq(self,result):
	self.rst=result[0]
	amod=self.rst
        if self.rst > 3:
	    amod = 3.5
	    self.rst = 3
	if self.rst == 2:
	    amod = 1.5
	    self.rst = 1
        fseq = self.formseq()
	frun = self.formrun(self.rst)
	gbonus = 0.33 * result[1]
	if self.rst > 0:	
	    self.ubeat[0] += 1
	else:
	    self.ubeat[0] = 0
	self.ubeat[1] = 1
        sweight = fseq * amod
	gweight = fseq * gbonus
	rweight = frun + sweight
	totals = [frun,sweight,rweight,gweight,self.ubeat[0],self.ubeat[1]]
	self.weights = map(sum,zip(self.weights,totals))
	self.weights[4]=self.ubeat[0]
    def get_weights(self):
	return self.weights
    def formseq(self):
    	if self.Sseq[1] < self.Sseq[0]:
	    self.Sseq[1] = self.Sseq[0]
    	else:
	    self.Sseq[0] = self.Sseq[0] + self.Sseq[2]
	    #print (self.Sseq[0],self.Sseq[1],self.Sseq[2])
	return self.Sseq[0]
    def formrun(self,result):
	if result == 3:
	    result = 2
    	if result > 0:
	    if self.Sval[0] > 1 and result == 1:
	        self.Sval[1] = self.Sval[1] - result
            else:
	    	self.Sval[1] = self.Sval[1] + result
	    self.Sval[0] = result
    	else:
	    self.Sval[1] = 0
	    self.Sval[0] = 0
	return self.Sval[1]
#X = Sequence()
#X.runseq([1,0])
#X.runseq([1,0])
#X.runseq([4,2])
#X.runseq([3,3])
#X.runseq([0,-1])
#X.runseq([2,1])
#X.print_weights()
