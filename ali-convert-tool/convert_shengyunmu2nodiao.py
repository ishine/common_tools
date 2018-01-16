import sys
from convert_phones import PrintList

def LoadLabPhones(phones_lab_file):
    ph_dict = {}
    for line in open(phones_lab_file,'r'):
        map_ph = line.rstrip().split()
        ph_dict[map_ph[0]] = map_ph[1]
    return ph_dict

def ConvertAli2Id(ali_file, phones_lab_file, output_file, offset = 1):
    out_fp = open(output_file, 'w')
    ph_dict = LoadLabPhones(phones_lab_file)
    for line in open(ali_file,'r'):
        ph_ali = line.rstrip().split()
        key = ph_ali[0]
        id_ali = []
        flagok = True
        for ph in ph_ali[1:]:
            if '_' in ph:
                phone = ph[:-2]
            else:
                phone = ph # SIL
            try:
                id = str(int(ph_dict[phone]) - offset)
                id_ali.append(id)
            except KeyError:
                print("no %s in %s" % (ph,phones_lab_file))
                flagok = False
                break
        if flagok == False:
            print(line)
            continue
        assert len(ph_ali) == len(id_ali) + 1
        id_str = PrintList([key]+id_ali)
        out_fp.write(id_str)
    out_fp.close()
    return True

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("%s phones_lab_file ali_file output_file" % sys.argv[0])
        sys.exit(1)
    phones_lab_file = sys.argv[1]
    ali_file = sys.argv[2]
    output_file = sys.argv[3]
    ConvertAli2Id(ali_file, phones_lab_file, output_file)

