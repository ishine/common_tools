#!/bin/bash

if [ -z $KALDI_ROOT ]
then
	export KALDI_ROOT=kaldi
fi

source=source-dir
./run.sh $source/dict $source/dict/tmp $source/graph/L \
	$source/lm/lm.arpa $source/graph/G \
	$source/am  $source/graph/hclg

