from music21 import *
from collections import Counter
import matplotlib.pyplot as plt
import re

def seq_ngrams(x, numbergram):
    pre = ["".join(x[i:i+numbergram]) for i in range(len(x)-numbergram+1)]
    last = [i if i[:2] == '=P' or i[:2] == '=0' else '=0' + i[2:] if i[2] == '-' or i[2] == '+' or i[2] == '=' else '=0' + i[3:] for i in pre]
    return last

def int_ngrams(s, none_items):
    
    piter = s.recurse()
    obj = piter.getElementsByClass(['Part', 'Note', 'Chord', 'Rest'])

    # Lo siguiente será un parámetro de la función
    ngram_list = list()
    tmp_string = list()
    cnt = 0

    ntbefore = None
    rest = False
    for num, i in enumerate(obj):
        
        if isinstance(i, note.Rest):
            cnt = cnt + 1
            if none_items is False:
                continue
            if rest is True:
                continue
            else:
                tmp_string.append('=P')
                rest = True
            
        elif isinstance(i, note.Note):
            rest = False
            cnt = cnt + 1
            if ntbefore is None:
                ntbefore = i.pitch.nameWithOctave
            else:
                inv = interval.Interval(note.Note(ntbefore), note.Note(i.pitch.nameWithOctave))
                invs = inv.semitones
                if invs > 0:
                    invs = '+' + str(invs)
                elif invs == 0:

                    if none_items is False:
                        continue
                    else:
                        invs = '=' + str(invs)
                else:
                    invs = str(invs)
                tmp_string.append(invs)
                ntbefore = i.pitch.nameWithOctave
            
        elif isinstance(i, chord.Chord):
            rest = False
            cnt = cnt + 1
            ch = i.getChordStep(1).nameWithOctave
            inv = interval.Interval(note.Note(ntbefore), ch)
            invs = inv.semitones
            if invs > 0:
                invs = '+' + str(invs)
            elif invs == 0:

                if none_items is False:
                    continue
                else:
                    invs = '=' + str(invs)
            else:
                invs = str(invs)
            tmp_string.append(invs)
            ntbefore = ch

        else:
            
            if isinstance(i, stream.Part):
                
                if num == 0:
                    continue
                
                else:

                    cnt = 0
                    ngram_list.append(tmp_string)
                    tmp_string = list()
                    continue

            else:
                pass

    ngram_list.append(tmp_string)
    return ngram_list

def split_ngrams(ngram_list, number_grams):
    for i in ngram_list:
        voice = seq_ngrams(i, number_grams)
        idx = ngram_list.index(i)
        ngram_list.pop(idx)
        ngram_list.insert(idx, voice)

    return ngram_list

def create_dict(d, tags, n):
    data = dict()
    if n == 4 and len(d) == len(tags):
        for i,z in zip(d, tags):
            if bool(re.search('más', z)) == True:
                
                mx = max(list(i.values()))
                max_format = [k for k,v in i.items() if v == mx]
                try: 
                    if len(data[z]) >= 1:
                        data[z].append(max_format)
                except:
                    data.update({z: [max_format]})
            else:
                
                mn = min(list(i.values()))
                min_format = [k for k,v in i.items() if v == mn]
                try:
                    if len(data[z]) >= 1:
                        data[z].append(min_format)
                except:
                    data.update({z: [min_format]})               
                
    else:
        return 'Error. No se ha configurado bien esta función.'
    
    return data

def parsons_code(x):
    rs = ''
    for n, i in enumerate(x):
        if n == len(x)-1:
            break
        if i == '=' and x[n+1] == 'P':
            rs = rs + 'R'
        elif i == '=' and x[n+1] == '0':
            rs = rs + '='
        elif i == '+' or i == '-':
            numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
            if n == len(x)-2:
                interval = int(x[n:])
                if interval > 2:
                    rs = rs + 'U'
                elif interval < 2 and interval >= 0:
                    rs = rs + 'u'
                elif interval < -2:
                    rs = rs + 'D'
                else:
                    rs = rs + 'd'
                break
                
            elif x[n+2] not in numbers:
                interval = int(x[n:n+2])
                if interval > 2:
                    rs = rs + 'U'
                elif interval < 2 and interval >= 0:
                    rs = rs + 'u'
                elif interval < -2:
                    rs = rs + 'D'
                else:
                    rs = rs + 'd'
            else:
                interval = int(x[n:n+3])
                if interval > 2:
                    rs = rs + 'U'
                elif interval < 2 and interval >= 0:
                    rs = rs + 'u'
                elif interval < -2:
                    rs = rs + 'D'
                else:
                    rs = rs + 'd'
        else:
            continue

    return rs                
            
def simplify_ngrams(x):
    dct = dict()
    for k, v in x.items():
        general_lst = list()
        for i in v:
            lst = list()
            for e in i:
                code = parsons_code(e)
                if code in lst:
                    continue
                else:
                    lst.append(code)
            general_lst.append(lst)
        dct.update({k: general_lst})
        
    
    return dct