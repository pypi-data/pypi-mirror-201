#!/usr/bin/env bash

RUNNER=cwltool

BIOBB_CHEMISTRY=$HOME/projects/BioBB/biobb_adapters/biobb_adapters/cwl/biobb_chemistry
$RUNNER $BIOBB_CHEMISTRY/acpype/acpype_params_ac.cwl $BIOBB_CHEMISTRY/test/acpype/acpype_params_ac.yml
$RUNNER $BIOBB_CHEMISTRY/acpype/acpype_params_cns.cwl $BIOBB_CHEMISTRY/test/acpype/acpype_params_cns.yml
$RUNNER $BIOBB_CHEMISTRY/acpype/acpype_params_gmx.cwl $BIOBB_CHEMISTRY/test/acpype/acpype_params_gmx.yml
$RUNNER $BIOBB_CHEMISTRY/acpype/acpype_params_gmx_opls.cwl $BIOBB_CHEMISTRY/test/acpype/acpype_params_gmx_opls.yml

$RUNNER $BIOBB_CHEMISTRY/ambertools/reduce_add_hydrogens.cwl $BIOBB_CHEMISTRY/test/ambertools/reduce_add_hydrogens.yml
$RUNNER $BIOBB_CHEMISTRY/ambertools/reduce_remove_hydrogens.cwl $BIOBB_CHEMISTRY/test/ambertools/reduce_remove_hydrogens.yml

$RUNNER $BIOBB_CHEMISTRY/babelm/babel_add_hydrogens.cwl $BIOBB_CHEMISTRY/test/babelm/babel_add_hydrogens.yml
$RUNNER $BIOBB_CHEMISTRY/babelm/babel_remove_hydrogens.cwl $BIOBB_CHEMISTRY/test/babelm/babel_remove_hydrogens.yml
$RUNNER $BIOBB_CHEMISTRY/babelm/babel_convert.cwl $BIOBB_CHEMISTRY/test/babelm/babel_convert.yml
$RUNNER $BIOBB_CHEMISTRY/babelm/babel_minimize.cwl $BIOBB_CHEMISTRY/test/babelm/babel_minimize.yml
