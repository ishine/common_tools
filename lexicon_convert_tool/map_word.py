from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os, sys, shutil, time


def MapMuchToOne(onedict, mlist):
    key=''
    for m in mlist:
        key += m
    try:
        return onedict[key]
    except KeyError:
        print('It shouldn\'t happen, you should examine.')
        print(key)
        return None

def MapDict(map_file):
    mdict = {}
    for line in open(map_file, 'r'):
        mlist = line.rstrip().split()
        key=''
        for d in mlist[1:]:
            key += d
        mdict[key] = mlist[0]
    return mdict

def GetSet(shengmu_file):
    shengmu_set = set()
    for line in open(shengmu_file, 'r'):
        shengmu = line.rstrip().split()[-1]
        shengmu_set.add(shengmu)
    return shengmu_set

def ConvertToWord(lexicon_in, shengmu_set, mdict):
    lexicon_out = []
    lexicon_nomap = []
    for line in open(lexicon_in, 'r'):
        word_pron = []
        lex_list = line.rstrip().split()
        word_str = lex_list[0]
        match = True
        for py in lex_list[1:]:
            if py in shengmu_set:
                if len(word_pron) != 0:
                    pron = MapMuchToOne(mdict, word_pron)
                    if pron == None:
                        lexicon_nomap.append(line)
                        match = False
                        break
                    word_str += ' ' + pron
                    word_pron = []
            word_pron.append(py)
        if match == False:
            continue
        pron = MapMuchToOne(mdict, word_pron)
        if pron == None:
            lexicon_nomap.append(line)
            continue
        word_str += ' ' + pron
        word_str += '\n'
        lexicon_out.append(word_str)
    return lexicon_out, lexicon_nomap

def WriteList(lex_list, file_out):
    fp_out = open(file_out,'w')
    for lex in lex_list:
        fp_out.write(lex)


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("%s shengmu_file map_file lexicon_in lexicon_out" % sys.argv[0])
        sys.exit(0)
    shengmu_file = sys.argv[1]
    map_file = sys.argv[2]
    lexicon_in = sys.argv[3]
    lexicon_out = sys.argv[4]
    shengmu_set = GetSet(shengmu_file)
    mdict = MapDict(map_file)
    lexicon_list, lexicon_nomap = ConvertToWord(lexicon_in, shengmu_set, mdict)

    WriteList(lexicon_list, lexicon_out)
    WriteList(lexicon_nomap, lexicon_out+'nomap')

