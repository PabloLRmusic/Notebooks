from collections import Counter
import re
from music21 import *
from sklearn.preprocessing import MinMaxScaler
import statistics
import numpy as np
from base import OrderedCounter

#predominancia de movimiento descendente???

def count_intervals(s):
    ntbefore = None

    for num, i in enumerate(obj):
        
        if isinstance(i, note.Rest):
            cnt = cnt + 1
            tmp_string.append('=P')
            
        elif isinstance(i, note.Note):
            cnt = cnt + 1
            if ntbefore is None:
                ntbefore = i.pitch.name
            else:
                inv = interval.Interval(note.Note(ntbefore), note.Note(i.pitch.name))
                invs = inv.semitones
                if invs > 0:
                    invs = '+' + str(invs)
                elif invs == 0:
                    invs = '=' + str(invs)
                else:
                    invs = str(invs)
                tmp_string.append(invs)
                ntbefore = i.pitch.name
            
        elif isinstance(i, chord.Chord):
            cnt = cnt + 1
            ch = i.getChordStep(1).name
            inv = interval.Interval(note.Note(ntbefore), ch)
            invs = inv.semitones
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

    for i in ngram_list:
        voice = seq_ngrams(i, number_grams)
        idx = ngram_list.index(i)
        ngram_list.pop(idx)
        ngram_list.insert(idx, voice)


    # Lo siguiente va en el cuaderno

    dict1 = Counter(ngram_list[0])
    dict2 = Counter(ngram_list[1])
    dict3 = Counter(ngram_list[2])
    dict4 = Counter(ngram_list[3])

    print(dict1.most_common()[-1])

def rec_notas(s, finalis):

    snotes = sorted([x.name for x in s.recurse().getElementsByClass('Note')])
    notes_ordered = list()
    tmp = list()
    cond = False

    for i in snotes:
        if cond is False:
            if i == finalis:
                cond = True
                notes_ordered.append(i)
            else:
                tmp.append(i)
        else:
            notes_ordered.append(i)

    if len(tmp) > 0:
        notes_ordered = notes_ordered + tmp
    else:
        pass


    nt_dict = OrderedCounter(notes_ordered)

    return nt_dict

def ambito(s):
    amb = analysis.discrete.Ambitus(s)
    amb = amb.getPitchSpan(s)
    result = amb[0].nameWithOctave + ' - ' + amb[1].nameWithOctave
    if interval.Interval(amb[0].nameWithOctave, amb[1].nameWithOctave).semitones <= 33:
        return result, 'a voce piena'
    else: return result, 'ad aequales'

def ambito_per_voice(score, x):
    dct = {'superius': 0, 'altus': 1, 'tenor': 2, 'bassus': 3}
    part = score.parts[dct[x]]
    amb = analysis.discrete.Ambitus(part)
    amb = amb.getPitchSpan(part)
    return [amb[0], amb[1]]

def get_finalis(s):

    sc = s.chordify()
    schords = sc.recurse().getElementsByClass('Chord')
    finalis = schords[-1].getChordStep(1)
    return finalis

def armadura(s):
    alt = [i.name for i in s[key.KeySignature].first().alteredPitches]
    return alt

def armadura_comparada(s, x):
    s = s.recurse().getElementsByClass('Note')
    count = {}
    for z in x:
        weight_alt = 0
        weight_nat = 0
        for i in s:
            nm = i.name
            nm_natural = i.name[0]

            if nm == z:
                weight_alt = float(weight_alt) + i.quarterLength
                count[z] = weight_alt
                
            if nm_natural == z:
                weight_nat = float(weight_nat) + i.quarterLength        
                count[z] = weight_nat

        if weight_alt >= weight_nat:
            pass
        else:
            x.remove(z)
            x.append(z[0])
    return x

def intervals(alt, natural_scale, finalis):
    scale = list()
    lst_ordered = list()
    if len(alt) == 0:
        index = natural_scale.index(finalis)
        lst_ordered = natural_scale[index:] + natural_scale[:index]
    else:
        alt_type = alt[0][-1]
        tmp = [i[:1] for i in alt]
        for i in natural_scale:
            if i in tmp: scale.append(i + alt_type)
            else: scale.append(i)

        index = scale.index(finalis)
        lst_ordered = list(scale[index:] + scale[:index])

    intervals = [interval.Interval(note.Note(x), note.Note(lst_ordered[n+1])).semitones\
                    for n, x in enumerate(lst_ordered) if n < len(lst_ordered)-1]
            
    if -10 in intervals:
        idx = intervals.index(-10)
        intervals[idx] = 2
    elif -11 in intervals:
        idx = intervals.index(-11)
        intervals[idx] = 1

    return [intervals, lst_ordered]


def calcs_mode(s, alt, natural_scale, natural_mode, finalis, mode_basis, transposed=None):
    
    lst_ordered = intervals(alt, natural_scale, finalis)[1]
    #condicionales para comprobar el ambito del tenor y del soprano
    #si el modo es autentico
    tenor_lowest = ambito_per_voice(s, 'tenor')[0]
    soprano_lowest = ambito_per_voice(s, 'superius')[0]

    if tenor_lowest.name == finalis or soprano_lowest.name == finalis:
        if mode_basis is False:
            return natural_mode[finalis]
        else:
            return str(transposed) + f' sobre {finalis}'
    
    elif tenor_lowest.name == lst_ordered[-1] or\
        soprano_lowest.name == lst_ordered[-1]:
        if mode_basis is False:
            return natural_mode[finalis]
        else:
            return str(transposed) + f' sobre {finalis}'

        
    #para abrir la posibilidad a modos plagales.
    #diferenciar tetrardus plagal del protus auténtico.
    elif tenor_lowest.name in lst_ordered[3:5] or\
        soprano_lowest.name in lst_ordered[3:5]:
        if mode_basis is False:
            return natural_mode[finalis] + ' plagal'
        else:
            if transposed == 'Protus':
                transposed = 'Tetrardus plagal'
                return str(transposed) + f' sobre {finalis}'
            else: return str(transposed) + f' sobre {finalis}'

    elif tenor_lowest.name in lst_ordered[3:5] or\
        soprano_lowest.name in lst_ordered[3:5]:
        if mode_basis is False:
            return natural_mode[finalis] + ' plagal'
        else:
            if transposed == 'Protus':
                transposed = 'Tetrardus plagal'
                return str(transposed) + f' sobre {finalis}'
            else: return str(transposed) + f' sobre {finalis}'
    
    elif finalis == 'F' and tenor_lowest.name == 'B-'\
        or finalis == 'F' and soprano_lowest.name == 'B-':
        if mode_basis is False:
            return natural_mode[finalis]
        else:
            if transposed == 'Protus':
                transposed = 'Tetrardus plagal'
                return str(transposed) + f' sobre {finalis}'
            else: return str(transposed) + f' sobre {finalis}'


def get_mode(s, finalis):
    natural_scale = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    modes = {"[2, 1, 2, 2, 2, 1]": 'Protus', "[2, 1, 2, 2, 1, 2]": 'Protus plagal', "[1, 2, 2, 2, 1, 2]": 'Deuterus', "[1, 2, 2, 1, 2, 2]": 'Deuterus plagal',\
             "[2, 2, 2, 1, 2, 2]": 'Tritus', "[2, 2, 1, 2, 2, 2]": 'Tritus plagal', "[2, 2, 1, 2, 2, 1]": 'Tetrardus'}
    natural_mode = {'D': 'Protus', 'E': 'Deuterus', 'F': 'Tritus', 'G': 'Tetrardus'}
    alt = armadura_comparada(s, armadura(s))
    
    if len(alt) == 0:
        try:
            calcs = calcs_mode(s, alt, natural_scale, natural_mode, finalis, mode_basis=False)
            return calcs
        except:
            try:
                ivls = intervals(alt, natural_scale, finalis)
                tr = modes[str(ivls[0])]
                calcs = calcs_mode(s, alt, natural_scale, natural_mode, finalis, mode_basis=True)
                return calcs
            except:
                alternativa = f'Cierta escala sobre {finalis}'
                return alternativa
    else:
        try:
            ivls = intervals(alt, natural_scale, finalis)
            tr = modes[str(ivls[0])]
            alternativa = calcs_mode(s, alt, natural_scale, natural_mode, finalis, mode_basis=True, transposed=tr)
            return alternativa
                
        except:
            #aquí el problema es que a veces puede haber una alteración que realmente es para avisar de la semitonía,
            #pero no es parte del modo. Conteo de qué versión aparece más en la obra, y tomar esa como base para el cálculo.
            alternativa = f'Cierta escala sobre {finalis}'
            return alternativa


def mean_note(s, x):
    dct = {'superius': 0, 'altus': 1, 'tenor': 2, 'bassus': 3}
    part = s.parts[dct[x]]
    rs = statistics.median([p.ps for p in part.pitches])
    rs = pitch.Pitch(rs)
    return rs.nameWithOctave


def MT_relation(s, voice):
    rs_dct = dict()
    v = s.parts[voice]
    allText = text.assembleLyrics(v)
    ls = search.lyrics.LyricSearcher(v)
    lst = allText.split()
    lst = [i[:-1] if bool(re.search(',', i)) == True or bool(re.search('\\.', i)) == True else i for i in lst]
    lst2 = set(lst)

    for i in lst2:
        sts_tmp = list()
        rs = ls.search(i)
        allRelevantNotes = None
        ########
        for x in range(0, len(rs)):
            firstNote = rs[x].els[0]
            lastNote = rs[x].els[-1]

            allRelevantNotes = [firstNote]
            currentNote = firstNote
            idd = lastNote.id
            ints = 0

            while currentNote is not None:
                currentNote = currentNote.next('Note')
                allRelevantNotes.append(currentNote)
                if currentNote is lastNote:
                    break

            for n, z in enumerate(v.recurse()):
                if z.id == idd:
                    try:
                        if z.next('Note').lyric is None:
                            z = z.next('Note')
                            idd = z.id
                            allRelevantNotes.append(z)
                        else:
                            break
                    except:
                        break
    
            for n, nt in enumerate(allRelevantNotes):
                if n == len(allRelevantNotes)-1:
                    break
                int1 = interval.Interval(note.Note(nt.nameWithOctave), note.Note(allRelevantNotes[n + 1].nameWithOctave))
                sts = int1.semitones
                sts_tmp.append(sts)
        scaler = MinMaxScaler(feature_range=(-1, 1))
        scaled = scaler.fit_transform([[x] for x in sts_tmp])
        rs_dct.update({i: np.mean(scaled)})
            
    return rs_dct
