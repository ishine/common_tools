#!/bin/bash -x

if [ $# != 7 ]
then
	echo $0 lang langtmp langout LMin LMout am hclg
	exit 1;
fi
. path.sh
lang=$1
langtmp=$2
langout=$3

LMin=$4
LMout=$5

am=$6

hclg=$7

if true
then
./utils/prepare_lang.sh --position-dependent-phones false \
	--num-sil-states 5 --num-nonsil-states 3 --sil-prob 0.5 \
	--phone-symbol-table $am/phones.txt \
	$lang '!SIL' $langtmp $langout || exit 1;

./shell_lm.sh $langout/words.txt $LMin $LMout || exit 1;

ln -s $PWD/$LMout/G.fst $langout
fi


utils/mkgraph.sh --transition-scale 1.0 --self-loop-scale 0.1 $langout $am $hclg || exit 1;
echo make graph ok;




