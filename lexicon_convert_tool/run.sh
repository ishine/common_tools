#!/bin/bash


outdir=outdir

mkdir -p $outdir

export LC_ALL=zh_CN.gbk
sed 'y/£á£â£ã£ä£å£æ£ç£è£é£ê£ë£ì£í£î£ï£ð£ñ£ò£ó£ô£õ£ö£÷£ø£ù£ú/abcdefghihklmnopqrstuvwxyz/' lexicon.txt > $outdir/tmp.file

grep '[a-z]' $outdir/tmp.file > $outdir/english.txt

grep -v '[a-z]' $outdir/tmp.file > $outdir/chinese.txt

grep -v '[0-9]' phones.txt > $outdir/shengmu.txt

grep '[0-9]' phones.txt > $outdir/yunmu.txt

python get_pinyin.py $outdir/shengmu.txt $outdir/chinese.txt $outdir/chinese_yunmu.txt > $outdir/nodiao_chinese_yunmu.txt
python get_pinyin.py $outdir/shengmu.txt $outdir/english.txt $outdir/english_yunmu.txt > $outdir/nodiao_english_yunmu.txt


#paste `awk '{print NF}' yunmu_map.txt` yunmu_map.txt|sort -rnk 1 > sort_yunmu_map.txt

python map_pinyin.py $outdir/shengmu.txt yunmu_map.txt $outdir/chinese.txt $outdir/map_chinese.txt
python map_pinyin.py $outdir/shengmu.txt yunmu_map.txt $outdir/english.txt $outdir/map_english.txt

awk '{for(i=2;i<=NF;++i)print $i}' $outdir/map_chinese.txt |sort -u > $outdir/chinese.phones.txt
awk '{for(i=2;i<=NF;++i)print $i}' $outdir/map_english.txt |sort -u> $outdir/english.phones.txt

cat $outdir/chinese.phones.txt $outdir/english.phones.txt |sort -u > $outdir/phones.txt

cat $outdir/map_english.txt $outdir/map_chinese.txt |\
	sed 'y/abcdefghihklmnopqrstuvwxyz/£á£â£ã£ä£å£æ£ç£è£é£ê£ë£ì£í£î£ï£ð£ñ£ò£ó£ô£õ£ö£÷£ø£ù£ú/' > $outdir/lexicon.txt

