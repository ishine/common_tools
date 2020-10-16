#!/bin/bash 

export PATH=./src/:$PATH
if [ -z $KALDI_ROOT ]
then
	export KALDI_ROOT=/home/hubo/git/github-online/github/kaldi
fi
#echo $KALDI_ROOT
. path.sh

stage=1
tool_dir=$PWD

rm -rf $output_dir

if [ $# != 3 ]
then
    echo $0 am_dir clg outputdir
    exit 1;
fi

am=$1
clg=$2
output_dir=$3
if [ ${output_dir:0:1} != "/" ]
then
	output_dir=$PWD/$output_dir
fi
#treeinfo=3_1
#self_loop_scale=0.1
treeinfo=2_1
self_loop_scale=1.0
mkdir -p $output_dir

clgdir=`dirname $clg`
if [ ! -f $am/tree ] || [ ! -f $am/final.mdl ] || [ ! -f $clgdir/ilabels_${treeinfo} ] || [ ! -f $clgdir/disambig_ilabels_${treeinfo}.int ]
then
    echo miss file $am/tree or $am/final.mdl or $clgdir/ilabels_${treeinfo} $clgdir/disambig_ilabels_${treeinfo}.int
    exit 1;
fi


date
# context depend phone to hmm
make-ilabel-transducer-sort --binary=false \
	--old-to-new-mapping=$output_dir/old2new \
	--write-disambig-syms=$output_dir/newdisambig --sort-disambig=true \
	$clgdir/ilabels_${treeinfo} $am/tree $am/final.mdl \
	$output_dir/new_ilabels_${treeinfo} > $output_dir/convert.fst || exit 1;

date
# construct hmm fst and input is trans_id
cdphone-to-pdf --reorder=true --self-loop-scale=$self_loop_scale  \
	$output_dir/new_ilabels_${treeinfo} $am/tree $am/final.mdl \
   	$output_dir/H.fst > $output_dir/kaldi_ilabel_to_pdf || exit 1;

date
# construct input pdf+1 and output trans_id fst
make-pdf-to-tid-transducer $am/final.mdl > $output_dir/pdf2tid.fst || exit 1;

date
# modefy hmm input is pdf+1 
for hmm in `ls $output_dir/H.fst*.fst`
do
	fsttablecompose $output_dir/pdf2tid.fst $hmm > ${hmm}.pdf || exit 1;
done

# generate hmm.list
hmm_num=`ls $output_dir/H.fst*.fst.pdf|wc -l`
rm -f $output_dir/hmm.pdf.list
rm -f $output_dir/hmm.tid.list
for i in `seq $hmm_num`
do
	tidhmm=$output_dir/H.fst${i}.fst
	pdfhmm=$output_dir/H.fst${i}.fst.pdf
	if [ -f $onehmm ]
	then
		echo $tidhmm >> $output_dir/hmm.tid.list
		echo $pdfhmm >> $output_dir/hmm.pdf.list
	else
		echo "no $pdfhmm, it shouldn't happen"
		exit -1
	fi
done

date
# optimize graph
fsttablecompose $output_dir/convert.fst $clg |\
	fstdeterminizestar --use-log=true  |\
	fstrmsymbols $output_dir/newdisambig |\
   	fstrmepslocal |\
   	fstminimizeencoded > $output_dir/det_min_clg.fst || exit 1;

date
echo make graph ok;
exit 0;

