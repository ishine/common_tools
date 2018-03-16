#!/bin/bash

cd /search/speech/hubo/git/kaldi/egs/hubo-ctc/s5
. path.sh
cd -

stage=1
tool_dir=$PWD

rm -rf $output_dir

if [ $# != 4 ]
then
    echo $0 htk_hmmdefs am_dir clg outputdir
    exit 1;
fi

htk_hmmdefs=$1
am=$2
clg=$3
output_dir=$4
mkdir -p $output_dir

clgdir=`dirname $clg`
if [ ! -f $am/tree ] || [ ! -f $am/final.mdl ] || [ ! -f $clgdir/ilabels_3_1 ] || [ ! -f $clgdir/disambig_ilabels_3_1.int ]
then
    echo miss file $am/tree or $am/final.mdl or $clgdir/ilabels_3_1 $clgdir/disambig_ilabels_3_1.int
    exit 1;
fi


cdphone-to-pdf $clgdir/ilabels_3_1  $am/tree $am/final.mdl  H.fst > $output_dir/kaldi_ilabel_to_pdf || exit 1;


grep "~h" $htk_hmmdefs | sed 's:~h ::g' | sed 's:"::g' > $output_dir/htk_cdphone

output_htk_hmm_to_pdf=$output_dir/htk_ilabel_to_pdf
output_kaldi_to_htk_ilabel_map_file=$output_dir/output_kaldi_to_htk_ilabel_map_file

$tool_dir/htk_cdphone_to_pdf.py $htk_hmmdefs $output_dir/htk_cdphone $output_htk_hmm_to_pdf || exit 1;

echo convert_kaldi_to_htk.py ok
#exit 0;

$tool_dir/kaldi-to-htk_ilabelmap.py $output_dir/kaldi_ilabel_to_pdf $output_htk_hmm_to_pdf \
    $output_kaldi_to_htk_ilabel_map_file  $output_dir/disambig_ilabels_file \
	$clgdir/disambig_ilabels_3_1.int || exit 1;


mv H.fst pdflist.tmp tiedlist.tmp $output_dir

echo kaldi-to-htk_cdphone.py ok
echo ilabel map end
exit 0
fstprint $clg > $output_dir/CLG_3_1.fst.txt

./kaldi-to-htk_clg.py $output_dir/CLG_3_1.fst.txt $output_kaldi_to_htk_ilabel_map_file $output_dir/htkilabel_clg.txt || exit 1;

echo clg exchange OK
fstcompile $output_dir/htkilabel_clg.txt $output_dir/htkilabel_clg.txt.bin

fstdeterminizestar --use-log=true $output_dir/htkilabel_clg.txt.bin \
    |fstrmsymbols $output_dir/disambig_ilabels_file | fstrmepslocal \
    | fstminimizeencoded > $output_dir/det_min_clg_htk.fst || exit 1;

echo it\'s OK

exit 0
