import excess_functions as ef
from text_to_list import list_correct

df = list_correct()
dead =  ef.list_variances(df)

a = sorted(dead)
a.reverse()
print a[:20]

b = sorted(range(len(dead)), key=lambda k: dead[k]);
b.reverse()
print b[:20];


