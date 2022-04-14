from collections import Counter, OrderedDict
from IPython.display import display, HTML

def print_newlines(df):
    return display( HTML( df.to_html().replace("\\n","<br>") ) )

class OrderedCounter(Counter, OrderedDict):
    'Counter that remembers the order elements are first encountered'

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, OrderedDict(self))

    def __reduce__(self):
        return self.__class__, (OrderedDict(self),)
    

def flat_values(dc):
    new_vals= list()
    new_dc = dict()
    vals = list(dc.values())
    keys = list(dc.keys())
    for i in vals:
        lista = list()
        for z in i:
            string = "\n".join(z)
            lista.append(string)

        new_vals.append(lista)
                    
    for i, z in zip(keys, new_vals):
        new_dc.update({i: z})
    
    return new_dc


def dic2txt(x, y, z):
    with open(x, 'w') as f:
        for n, i in enumerate(z):
            f.write(i + '\n')
            for key, value in y[n].items(): 
                f.write('%s:%s\n' % (key, value))
    f.close()
    return f

        
    
