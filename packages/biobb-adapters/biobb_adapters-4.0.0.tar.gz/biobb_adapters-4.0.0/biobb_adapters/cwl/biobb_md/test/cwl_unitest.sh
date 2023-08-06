#!/usr/bin/env bash

RUNNER=cwltool

BIOBB_MD=$HOME/projects/biobb_adapters/biobb_adapters/cwl/biobb_md
$RUNNER $BIOBB_MD/gromacs/pdb2gmx.cwl $BIOBB_MD/test/gromacs/pdb2gmx.yml
$RUNNER $BIOBB_MD/gromacs/editconf.cwl $BIOBB_MD/test/gromacs/editconf.yml
$RUNNER $BIOBB_MD/gromacs/genion.cwl $BIOBB_MD/test/gromacs/genion.yml
$RUNNER $BIOBB_MD/gromacs/genrestr.cwl $BIOBB_MD/test/gromacs/genrestr.yml
$RUNNER $BIOBB_MD/gromacs/grompp.cwl $BIOBB_MD/test/gromacs/grompp.yml
$RUNNER $BIOBB_MD/gromacs/mdrun.cwl $BIOBB_MD/test/gromacs/mdrun.yml
$RUNNER $BIOBB_MD/gromacs/solvate.cwl $BIOBB_MD/test/gromacs/solvate.yml
$RUNNER $BIOBB_MD/gromacs/make_ndx.cwl $BIOBB_MD/test/gromacs/make_ndx.yml
$RUNNER $BIOBB_MD/gromacs_extra/ndx2resttop.cwl $BIOBB_MD/test/gromacs_extra/ndx2resttop.yml
