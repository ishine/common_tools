#!/usr/bin/python

import os, sys, re

if len(sys.argv) != 4:
    print sys.argv[0] + " hmmdefs cd-phone.list output\n"
    sys.exit(1)

#HMMDEFS="hmmdefs"
#INQUIRY="cd-phone.list"
HMMDEFS = sys.argv[1]
INQUIRY = sys.argv[2]
output = sys.argv[3]

cmd = 'grep -B 2 NUMMIXES %s | grep ~s  | sed \'s:\"::g\' - | sed \'s:~s ::g\' - > pdflist.tmp ' % HMMDEFS
os.system(cmd)
fin = open("pdflist.tmp", 'rt')
ctx2pdfid = {}
id = -1
for triphone in fin:
    triphone = triphone.strip()
    id += 1
    ctx2pdfid[triphone] = id
fin.close()

cmd = "grep -A 12 ~h %s | grep -E \'~h|~s\' > tiedlist.tmp" % HMMDEFS
os.system(cmd)
tiedphone = {}
state = []
flag = 0
for line in open("tiedlist.tmp"):
    (token, triphone, c) = line.split('\"')
    if token == "~h ":
        if flag == 0:
            key = triphone
            flag += 1
        else:
            tiedphone[key] = state
            key = triphone
            state = []
    else:
        state.append(triphone)
tiedphone[key] = state

htk_pdfmap = open(output, 'w')

cdphone2pdfid = {}
states = []
nline = 1
for line in open(INQUIRY):
    cdphone = line.strip()
    #       print cdphone
    pdfid = []
    htk_pdfmap.write(str(nline) + ' ')
    nline += 1
    try:
        states = tiedphone[cdphone]
    except KeyError:
        print('no this cd phone ' + cdphone + '\n')
        sys.exit(1)
    for i in range(len(states)):
        pdfid.append(ctx2pdfid[states[i]])
        htk_pdfmap.write(str(ctx2pdfid[states[i]]) + ' ')
    htk_pdfmap.write('\n')
    cdphone2pdfid[cdphone] = pdfid
#cd_map=open('cd_map','w')
#cd_map.write(cdphone2pdfid)
#cd_map.close()
#print cdphone2pdfid
