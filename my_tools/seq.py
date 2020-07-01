Sseq = [0.5,0.5,0.5]
Sval = [0,0]
# previous [0] / current [1]
def testing():
    global Sseq
    if Sseq[1] < Sseq[0]:
	Sseq[1] = Sseq[0]
    else:
	Sseq[0] = Sseq[0] + Sseq[2]
    print Sseq[0]
def testing2(result):
    global Sval
    if result > 0:
	if Sval[0] > 1 and result == 1:
	    Sval[0] = result
        else:
	    Sval[1] = Sval[1] + result
	    Sval[0] = result
    else:
	Sval[1] = 0
	Sval[0] = 0
    print Sval[1]

for num in range(0,6):
    testing()
testing2(2)
testing2(1)
testing2(2)
testing2(0)
testing2(1)
testing2(2)
testing2(2)
testing2(1)
testing2(1)
