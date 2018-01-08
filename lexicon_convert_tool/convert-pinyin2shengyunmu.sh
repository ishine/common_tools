#!/bin/bash

sourcedir=sheng-yun-mu
outdir=outdir-shengyunmu
outdir_words=outdir-words


mkdir -p $outdir $outdir_words

export LC_ALL=zh_CN.gbk
sed 'y/£á£â£ã£ä£å£æ£ç£è£é£ê£ë£ì£í£î£ï£ð£ñ£ò£ó£ô£õ£ö£÷£ø£ù£ú/abcdefghihklmnopqrstuvwxyz/' $sourcedir/lexicon.txt > $outdir/tmp.file

grep '[a-z]' $outdir/tmp.file > $outdir/english.txt

grep -v '[a-z]' $outdir/tmp.file > $outdir/chinese.txt

grep -v '[0-9]' $sourcedir/phones.txt > $outdir/shengmu.txt

grep '[0-9]' $sourcedir/phones.txt > $outdir/yunmu.txt

python get_pinyin.py $outdir/shengmu.txt $outdir/chinese.txt $outdir/chinese_yunmu.txt > $outdir/nodiao_chinese_yunmu.txt
python get_pinyin.py $outdir/shengmu.txt $outdir/english.txt $outdir/english_yunmu.txt > $outdir/nodiao_english_yunmu.txt


#paste `awk '{print NF}' yunmu_map.txt` yunmu_map.txt|sort -rnk 1 > sort_yunmu_map.txt

python map_pinyin.py $outdir/shengmu.txt $sourcedir/yunmu_map.txt $outdir/chinese.txt $outdir/map_chinese.txt
python map_pinyin.py $outdir/shengmu.txt $sourcedir/yunmu_map.txt $outdir/english.txt $outdir/map_english.txt

awk '{for(i=2;i<=NF;++i)print $i}' $outdir/map_chinese.txt |sort -u > $outdir/chinese.phones.txt
awk '{for(i=2;i<=NF;++i)print $i}' $outdir/map_english.txt |sort -u> $outdir/english.phones.txt

cat $outdir/chinese.phones.txt $outdir/english.phones.txt |sort -u > $outdir/phones.txt

cat $outdir/map_english.txt $outdir/map_chinese.txt |\
	sed 'y/abcdefghihklmnopqrstuvwxyz/£á£â£ã£ä£å£æ£ç£è£é£ê£ë£ì£í£î£ï£ð£ñ£ò£ó£ô£õ£ö£÷£ø£ù£ú/' > $outdir/lexicon.txt

awk '{for(i=2;i<=NF;++i) printf("%s ",$i);printf("\n");}' $outdir/map_chinese.txt |\
	awk '
		{
			if(NF%2 != 0)
			{
				printf("%s is error!\n",$0);
				exit(1);
			}
			for(i=1;i<=NF;i+=2) 
				printf("%s%s %s %s\n",$i,$(i+1),$i,$(i+1));
		}' |sort -u > $outdir_words/map_word2shengyunmu.txt

python map_word.py $outdir_words/map_word2shengyunmu.txt $outdir/map_chinese.txt $outdir_words/map_chinese.txt

