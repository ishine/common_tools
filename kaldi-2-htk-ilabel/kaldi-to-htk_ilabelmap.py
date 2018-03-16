#!/usr/bin/env python

import sys

if len(sys.argv) != 6:
    print sys.argv[0] + " kaldi_ilabel_id htk_ilabel_id kaldi_to_htk_ilabel_map_file htk_disambig_ilabels_file kaldi_disambig_ilabels_file\n"
    sys.exit(1)

ilabel_map_file = open(sys.argv[3], 'w')
disambig_ilabels_file = open(sys.argv[4], 'w')

# read kaldi disambig file
kaldi_disambig_ilabels_set=set()
disambig=0
for line in open(sys.argv[5]):
    disambig_line = line.rstrip()
    kaldi_disambig_ilabels_set.add(disambig_line)
    disambig+=1

'''
first process htk_ilabel_id, save dict
'''
pdf_dict = {}

max_ilabel = -1
#print 'start'
for line in open(sys.argv[2]):
    phone_line = line.rstrip().split(' ')
    num = len(phone_line)
    pdf_str = phone_line[1]
    i = 2
    #    print num
    while i < num:
        pdf_str += '-' + phone_line[i]
        i += 1

    pdf_dict[pdf_str] = phone_line[0]
    if int(phone_line[0]) > max_ilabel:
        max_ilabel = int(phone_line[0])

#   print pdf_str+' '+phone_line[0]

#print 'ok'
#sys.exit(0)
disambig_id = max_ilabel + 1

# kaldi to htk map
# first write 0 0 eps eps
ilabel_map_file.write('0' + ' ' + '0' + '\n')
for line in open(sys.argv[1]):
    hmm_line = line.rstrip().split(' ')
    num = len(hmm_line)
    #    if num==2:
    if int(hmm_line[1]) <= 0:
        if hmm_line[0] in kaldi_disambig_ilabels_set:
            ilabel_map_file.write(hmm_line[0]+' '+str(disambig_id)+'\n')
            disambig_ilabels_file.write(str(disambig_id)+'\n')
            disambig_id += 1
            print hmm_line[0]+' '+str(disambig_id)
            continue
        else:
            print "code have error!disambig ilabels judge error."

        #        if int(hmm_line[1]) > 0:
        #            print(hmm_line[1]+' it\'s error.\n')
    pdf_str = hmm_line[1]
    i = 2
    while i < num:
        pdf_str += '-' + hmm_line[i]
        i += 1
    try:
        htk_id = pdf_dict[pdf_str]
        ilabel_map_file.write(hmm_line[0] + ' ' + htk_id + '\n')
    except KeyError:
        print('no this pdf_str ' + pdf_str + '\n')
        sys.exit(1)

ilabel_map_file.close()
disambig_ilabels_file.close()
