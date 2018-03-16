#!/usr/bin/env python

import sys


if len(sys.argv) != 4:
    print sys.argv[0]+" kaldi_clg kaldi_to_htk_ilabel_map_file htk_clg\n"
    sys.exit(1)

htk_clg=open(sys.argv[3],'w')

'''
first process kaldi-to-htk_ilabel, save dict
'''
map_dict={}

for line in open(sys.argv[2]):
    map_line=line.rstrip().split()

    map_dict[map_line[0]] = map_line[1]


for line in open(sys.argv[1]):
    fst_line=line.rstrip().split()
    num=len(fst_line);
    if num==1:
        htk_clg.write(fst_line[0]+'\n')
        continue
    fst_str=fst_line[0]
    i=1
    while i < num:
        if i == 2:
            try:
                htk_id = map_dict[fst_line[i]]
                fst_str+=' '+htk_id
            except KeyError:
                print('no this ilabel '+fst_line[i]+'\n')
        else:
            fst_str+=' '+fst_line[i]
        i+=1
    htk_clg.write(fst_str+'\n')

htk_clg.close()
