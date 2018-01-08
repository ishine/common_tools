

import sys

if len(sys.argv) != 5:
    print sys.argv[0] + " shengmu_file map_file lexicon_file map_lexicon"
    sys.exit(1)


shengmu_file=sys.argv[1]
mapfile=sys.argv[2]
lexicon_file=sys.argv[3]
map_lexicon=sys.argv[4]
nomap_lexicon=map_lexicon+"nomap"

map_lexicon_file=open(map_lexicon,'w')
nomap_lexicon_file=open(nomap_lexicon,'w')

def exchange_yunmu(old_yunmu):
    if len(old_yunmu) == 0:
        return None,None
    diao=int(old_yunmu[0][-1])
    yunmu_str=old_yunmu[0][0:-2]
    for ph in old_yunmu[1:]:
        if diao != int(ph[-1]):
            print "it should be process by people"
            return None,None
        yunmu_str+=" "+ph[0:-2]
    return yunmu_str,diao



shengmu_set=set()
for line in open(shengmu_file,'r'):
    shengmu=line.rstrip().split()
    shengmu_set.add(shengmu[0])

ph_map_dict={}
for line in open(mapfile,'r'):
    map_line_list=line.rstrip().split()
    ph_str=map_line_list[1]
    for ph in map_line_list[2:]:
        ph_str+=" "+ph
    ph_map_dict[ph_str] = map_line_list[0].upper()

for line in open(lexicon_file,'r'):
    lex_line_list=line.rstrip().split()
    map_lex=lex_line_list[0]
    yunmu=[]
    yunmu_str=""
    yunmu_diao=0
    for ph in lex_line_list[1:]:
        if ph in shengmu_set:
            if len(yunmu) != 0:
                yunmu_str,yunmu_diao=exchange_yunmu(yunmu)
                yunmu=[]
                if yunmu_str == None:
                    nomap_lexicon_file.write(line)
                    break
                if yunmu_str in ph_map_dict.keys():
                    map_lex+=" "+ ph_map_dict[yunmu_str]+"_"+str(yunmu_diao)
                else:
                    nomap_lexicon_file.write(line)
                    break
            map_lex+=" "+ph
        else:
            yunmu.append(ph)
    if len(yunmu) > 0:
        yunmu_str,yunmu_diao=exchange_yunmu(yunmu)
        if yunmu_str == None:
            nomap_lexicon_file.write(line)
            continue
        if yunmu_str in ph_map_dict.keys():
            map_lex+=" "+ ph_map_dict[yunmu_str]+"_"+str(yunmu_diao)
        else:
            nomap_lexicon_file.write(line)
            continue

    map_lexicon_file.write(map_lex+"\n")

map_lexicon_file.close()
nomap_lexicon_file.close()
