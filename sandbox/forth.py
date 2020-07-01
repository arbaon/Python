#functions
def print_one(arg1, arg2):
    print "%r %r" % (arg1, arg2)
def calc_one(arg1, arg2):
    result = arg1 * arg2
    print arg1 * arg2
    calc_two(result,10)
def calc_two(arg3, arg4):
    print arg3 * arg4

def add(a, b):
    return a + b
def sub(a, b):
    return a - b
def mul(a,b):
    return a * b
def result(a, b):
    addx = add(a, b)
    subx = sub(a, b)
    mulx - mul(a, b)
    print "add %r \n" % addx
print_one("test",1234)
calc_one(10,10)
result (20,25)
