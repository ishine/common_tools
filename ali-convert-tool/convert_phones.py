
import sys



def MapPhones(map_ph):
    ph_map_dict={}
    for line in open(map_ph, 'r'):
        ph_line = line.rstrip().split()
        ph_str = ph_line[1]
        for ph in ph_line[2:]:
            ph_str+=" "+ph
        ph_map_dict[ph_str] = ph_line[0].upper()
    return ph_map_dict

def LoadPhones(ph_file):
    phones_list = []
    num = 0
    for line in open(ph_file,'r'):
        ph = line.rstrip().split()
        assert int(ph[1]) == num
        phones_list.append(ph[0])
        num += 1
    return phones_list

# convert align num to phones text
def Ali2Phones(ali_list, phones_list):
    ph_ali = []
    for index in ali_list:
        ph_ali.append(phones_list[int(index)])
    return ph_ali

# split phones ali depend on shengmu
def ConvertWord2Shengyun(word, shengmu_dict):
    shengmu=[]
    yunmu=[]
    for ph in word:
        if ph in shengmu_dict.keys():
            shengmu.append(ph)
        else:
            yunmu.append(ph)
    return [shengmu, yunmu]

def SplitPhonesAli(ph_ali, shengmu_dict):
    words_list = []
    word = [ph_ali[0]]
    for ph in ph_ali[1:]:
        if ph in shengmu_dict.keys() and ph != word[-1]:
            words_list.append(word)
            word=[ph]
        else:
            word.append(ph)
    if len(word) != 0:
        words_list.append(word)
    return words_list

def PrintWordListLen(words_list):
    tot_len = 0
    for word in words_list:
        for ph in word:
            tot_len += len(ph)
            print(len(ph))
    return tot_len

def ConvertPhali2Shengyun(ph_ali, shengmu_dict):
    words_list = SplitPhonesAli(ph_ali, shengmu_dict)
    shengyun_list = []
    for word in words_list:
        shengyun = ConvertWord2Shengyun(word, shengmu_dict)
        shengyun_list.append(shengyun)
    return shengyun_list

def MapPhones2Yunmu(yunmu_list, yunmu_dict):
    ph_str = yunmu_list[0][:-2]
    tmp_ph = yunmu_list[0]
    diao = tmp_ph[-1]
    for ph in yunmu_list[1:]:
        if ph == tmp_ph:
            continue
        tmp_ph = ph
        ph_str += ' '+ph[:-2]
    try:
        yunmu = yunmu_dict[ph_str]
        return yunmu + '_' + diao
    except KeyError:
        print('It\'s not map %s' % ph_str)
        return None
        
def PrintList(p_list):
    li_str = ''
    for val in p_list:
        li_str += str(val)+' '
    li_str += '\n'
    return li_str

def ConvertShengyun2Word(words_list):
    new_words_list = []
    for word in words_list:
        word_str = word[0][0]
        if len(word[1]) != 0:
            word_str += word[1][0]
        word_words = []
        for ph in word[0] + word[1]:
            word_words.append(word_str)
        new_words_list.append(word_str)
    return new_words_list

def Phones2ShengyunAli(old_ali, new_ali, shengmu_dict, yunmu_dict, phones_list):
    new_fp = open(new_ali, 'w')
    new_word_fp = open(new_ali+'.word', 'w')
    for line in open(old_ali, 'r'):
        ali_line = line.rstrip().split()
        key = ali_line[0]
        newword_list = []
        # convert phones text
        ph_ali = Ali2Phones(ali_line[1:], phones_list)
        words_list = ConvertPhali2Shengyun(ph_ali, shengmu_dict)
        new_word = []
        mapflag = True
        for word in words_list:
            new_word.append(word[0])
            if len(word[1]) != 0:
                yunmu = MapPhones2Yunmu(word[1], yunmu_dict)
                if yunmu == None:
                    print('%s --- it\'s map error' % line)
                    mapflag = False
                    break
                yunmu_list = []
                for i in word[1]:
                    yunmu_list.append(yunmu)
                new_word.append(yunmu_list)
            newword_list.append(new_word)
            new_word = []
        if mapflag == False:
            continue
        # output newword_list to new_ali
        new_ph_ali=[key]
        for word in newword_list:
            for new_ph in word:
                new_ph_ali.extend(new_ph)

        # output word ali to new_word_ali
        word_words_list = ConvertShengyun2Word(newword_list)
        new_word_ali = [key]
        for word in word_words_list:
            new_word_ali.extend(word)

        #print(PrintWordListLen(newword_list))
        #print(PrintWordListLen(words_list))
        #print(len(new_ph_ali))
        assert len(new_ph_ali) == len(ali_line)
        str_newali = PrintList(new_ph_ali)
        new_fp.write(str_newali)

        str_newwordali = PrintList(new_word_ali)
        new_word_fp.write()
    new_fp.close()
    new_word_fp.close()
    return True

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("%s old_phones shengmu_file yunmu_file old_ali new_ali" % sys.argv[0])
        sys.exit(1)
    old_phones = sys.argv[1]
    shengmu_file = sys.argv[2]
    yunmu_file = sys.argv[3]
    old_ali = sys.argv[4]
    new_ali = sys.argv[5]
    old_ph_list = LoadPhones(old_phones)
    shengmu_dict = MapPhones(shengmu_file)
    yunmu_dict = MapPhones(yunmu_file)

    Phones2ShengyunAli(old_ali, new_ali, shengmu_dict, yunmu_dict, old_ph_list)

