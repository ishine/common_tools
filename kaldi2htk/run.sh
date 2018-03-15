#!/bin/bash -x


#DIR=kaldi-model/input
#DIR=/search/odin/hubo/hubo/clg-tools/source
#DIR=/search/speech/hubo/hubo/chain-model-clg-tools/source
DIR=kaldi-source
OUTDIR=$DIR/htkmodel-0.5trans
mkdir -p $OUTDIR
python hb_kaldi2HTK.py --sil-pdf-classes=2 --silphones=1 --non-sil-pdf-classes=2 \
 $DIR/final.mdl.txt $DIR/phones.txt $DIR/tree $OUTDIR/HTKmodels $OUTDIR/tiedlist


