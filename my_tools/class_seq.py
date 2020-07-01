class Sequence:
    def __init__(self):
        #self.Sseq = [0.5,0.5,0.5]
        self.Sseq = [0.8,0.8,0.2]
        self.Sval = [0,0]
    def runseq(self,result):
        fseq = self.formseq()
	frun = self.formrun(result)
        sweight = fseq * result
	rweight = frun + sweight
	aweights = [frun,sweight,rweight]
	return aweights
    def formseq(self):
    	if self.Sseq[1] < self.Sseq[0]:
	    self.Sseq[1] = self.Sseq[0]
    	else:
	    self.Sseq[0] = self.Sseq[0] + self.Sseq[2]
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
def get_seq(mresults):
    X = Sequence()
    totals = [0,0,0]
    nlbonus = 6
    for num in range(0,6):
        mytest = X.runseq(mresults[num])
        totals = map(sum, zip(totals,mytest))
	if mresults[num] == 0:
	    nlbonus = nlbonus - 1
        print mytest[0],mytest[1],mytest[2]
    print totals[0],totals[1],totals[2],nlbonus
test = [0,1,3,3,3,1]
get_seq(test)
test2 = [3,3,3,3,3,3]
get_seq(test2)
test3 = [1,1,1,1,1,3]
get_seq(test3)

