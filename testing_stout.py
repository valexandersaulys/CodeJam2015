import sys

sys.stdout.write("%s\t%f\t%d\n" % ("Hello",1.0,2))
sys.stdout.write("%s\t%f\t%d\n" % ("Hello",1.0,2))

def foo(l):
    for i in range(len(l)):
        if l[i] == float(1):
            l[i] = "COMPLETE_REMISSION"
        elif l[i] == float(-1):
            l[i] = "RESISTANT";
    return l;

a = [-1.0,1.0,-1.0,1.0,1.0]
a = foo(a); print type(a);

for i in range(len(a)):
    sys.stdout.write("%s\n" % (a[i]));
