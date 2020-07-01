#Example of lambda inside of list

class tstlamb:
    def __init__(self):
        self.testone=10
        self.testtwo=20
        self.testthree=30
    def add_one(self,one):
        self.testone += one
        return self.testone
    def add_two(self,two):
        self.testtwo += two
        return self.testtwo
    def add_three(self,three):
        self.testthree += three
        return self.testthree

def test(one,two):
    operation= one['operation']
    dyno = tstlamb()

    operations = {
	    't1' : lambda x: dyno.add_one(x),
	    't2' : lambda x: dyno.add_two(x),
	    't3' : lambda x: dyno.add_three(x)
    }

    if operation in operations:
        return operations[operation](one.get('value'))

one ={ "operation": "t1","value": 3 }
two={ "operation": "t2","value": 6 }
three={ "operation": "t3","value": 9 }
four="null"
testing=test(one,four)
print (testing)
testing=test(two,four)
print (testing)
testing=test(three,four)
print (testing)

