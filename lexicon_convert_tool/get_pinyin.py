
import sys

if len(sys.argv) != 4:
    print sys.argv[0] + " shengmu_file lexicon_file yunmu_out"
    sys.exit(1)

shengmu_file=sys.argv[1]
lexicon_file=sys.argv[2]
yunmu_out=open(sys.argv[3],'w')



shengmu_set=set()
for line in open(shengmu_file,'r'):
    shengmu_set.add(line.rstrip())

yunmu_set=set()
for line in open(lexicon_file,'r'):
    phones_list=line.rstrip().split()
    yunmu=[]
    for ph in phones_list[1:]:
        if ph in shengmu_set:
            if len(yunmu) > 0:
                str_yunmu=yunmu[0]
                for ph in yunmu[1:]:
                    str_yunmu+=" " + ph
                yunmu_set.add(str_yunmu)
            yunmu=[]
            continue
        else:
            yunmu.append(ph)
    if len(yunmu) > 0:
        str_yunmu=yunmu[0]
        for ph in yunmu[1:]:
            str_yunmu+=" " + ph
        yunmu_set.add(str_yunmu)


for yunmu in yunmu_set:
    yunmu_out.write(yunmu+'\n')

yunmu_out.close()

yunmu_nodiao_set=set()
for yunmu in yunmu_set:
    ph_list=yunmu.split()
    ph_str=ph_list[0][0:len(ph_list[0])-2]
    for ph in ph_list[1:]:
        ph_str+=" "+ph[0:len(ph)-2]
    yunmu_nodiao_set.add(ph_str)

for ph in yunmu_nodiao_set:
    print ph



