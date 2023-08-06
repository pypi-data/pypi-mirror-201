#!/usr/bin/env bash

RUNNER=cwltool

BIOBB_ANALYSIS=$HOME/projects/BioBB/biobb_adapters/biobb_adapters/cwl/biobb_analysis
$RUNNER $BIOBB_ANALYSIS/ambertools/cpptraj_average.cwl $BIOBB_ANALYSIS/test/ambertools/cpptraj_average.yml
$RUNNER $BIOBB_ANALYSIS/ambertools/cpptraj_bfactor.cwl $BIOBB_ANALYSIS/test/ambertools/cpptraj_bfactor.yml
$RUNNER $BIOBB_ANALYSIS/ambertools/cpptraj_convert.cwl $BIOBB_ANALYSIS/test/ambertools/cpptraj_convert.yml
$RUNNER $BIOBB_ANALYSIS/ambertools/cpptraj_dry.cwl $BIOBB_ANALYSIS/test/ambertools/cpptraj_dry.yml
$RUNNER $BIOBB_ANALYSIS/ambertools/cpptraj_image.cwl $BIOBB_ANALYSIS/test/ambertools/cpptraj_image.yml
$RUNNER $BIOBB_ANALYSIS/ambertools/cpptraj_mask.cwl $BIOBB_ANALYSIS/test/ambertools/cpptraj_mask.yml
$RUNNER $BIOBB_ANALYSIS/ambertools/cpptraj_rgyr.cwl $BIOBB_ANALYSIS/test/ambertools/cpptraj_rgyr.yml
$RUNNER $BIOBB_ANALYSIS/ambertools/cpptraj_rms.cwl $BIOBB_ANALYSIS/test/ambertools/cpptraj_rms.yml
$RUNNER $BIOBB_ANALYSIS/ambertools/cpptraj_rmsf.cwl $BIOBB_ANALYSIS/test/ambertools/cpptraj_rmsf.yml
$RUNNER $BIOBB_ANALYSIS/ambertools/cpptraj_slice.cwl $BIOBB_ANALYSIS/test/ambertools/cpptraj_slice.yml
$RUNNER $BIOBB_ANALYSIS/ambertools/cpptraj_snapshot.cwl $BIOBB_ANALYSIS/test/ambertools/cpptraj_snapshot.yml
$RUNNER $BIOBB_ANALYSIS/ambertools/cpptraj_strip.cwl $BIOBB_ANALYSIS/test/ambertools/cpptraj_strip.yml

$RUNNER $BIOBB_ANALYSIS/gromacs/gmx_cluster.cwl $BIOBB_ANALYSIS/test/gromacs/gmx_cluster.yml
$RUNNER $BIOBB_ANALYSIS/gromacs/gmx_energy.cwl $BIOBB_ANALYSIS/test/gromacs/gmx_energy.yml
$RUNNER $BIOBB_ANALYSIS/gromacs/gmx_image.cwl $BIOBB_ANALYSIS/test/gromacs/gmx_image.yml
$RUNNER $BIOBB_ANALYSIS/gromacs/gmx_rgyr.cwl $BIOBB_ANALYSIS/test/gromacs/gmx_rgyr.yml
$RUNNER $BIOBB_ANALYSIS/gromacs/gmx_rms.cwl $BIOBB_ANALYSIS/test/gromacs/gmx_rms.yml
$RUNNER $BIOBB_ANALYSIS/gromacs/gmx_trjconv_str.cwl $BIOBB_ANALYSIS/test/gromacs/gmx_trjconv_str.yml
$RUNNER $BIOBB_ANALYSIS/gromacs/gmx_trjconv_str_ens.cwl $BIOBB_ANALYSIS/test/gromacs/gmx_trjconv_str_ens.yml
$RUNNER $BIOBB_ANALYSIS/gromacs/gmx_trjconv_trj.cwl $BIOBB_ANALYSIS/test/gromacs/gmx_trjconv_trj.yml