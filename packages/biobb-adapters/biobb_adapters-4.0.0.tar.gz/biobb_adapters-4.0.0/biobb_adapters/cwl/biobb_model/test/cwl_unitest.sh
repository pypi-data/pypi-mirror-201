#!/usr/bin/env bash

RUNNER=cwltool

BIOBB_MODEL=$HOME/projects/biobb_adapters/biobb_adapters/cwl/biobb_model
$RUNNER $BIOBB_MODEL/model/mutate.cwl $BIOBB_MODEL/test/model/mutate.yml
$RUNNER $BIOBB_MODEL/model/fix_side_chain.cwl $BIOBB_MODEL/test/model/fix_side_chain.yml
