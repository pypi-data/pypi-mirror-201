#!/usr/bin/env bash

RUNNER=cwltool

BIOBB_STRUCTURE_UTILS=$HOME/projects/BioBB/biobb_adapters/biobb_adapters/cwl/biobb_structure_utils
$RUNNER $BIOBB_STRUCTURE_UTILS/utils/cat_pdb.cwl $BIOBB_STRUCTURE_UTILS/test/utils/cat_pdb.yml
$RUNNER $BIOBB_STRUCTURE_UTILS/utils/extract_atoms.cwl $BIOBB_STRUCTURE_UTILS/test/utils/extract_atoms.yml
$RUNNER $BIOBB_STRUCTURE_UTILS/utils/extract_chain.cwl $BIOBB_STRUCTURE_UTILS/test/utils/extract_chain.yml
$RUNNER $BIOBB_STRUCTURE_UTILS/utils/extract_heteroatoms.cwl $BIOBB_STRUCTURE_UTILS/test/utils/extract_heteroatoms.yml
$RUNNER $BIOBB_STRUCTURE_UTILS/utils/extract_model.cwl $BIOBB_STRUCTURE_UTILS/test/utils/extract_model.yml
$RUNNER $BIOBB_STRUCTURE_UTILS/utils/extract_protein.cwl $BIOBB_STRUCTURE_UTILS/test/utils/extract_protein.yml
$RUNNER $BIOBB_STRUCTURE_UTILS/utils/remove_ligand.cwl $BIOBB_STRUCTURE_UTILS/test/utils/remove_ligand.yml
$RUNNER $BIOBB_STRUCTURE_UTILS/utils/remove_pdb_water.cwl $BIOBB_STRUCTURE_UTILS/test/utils/remove_pdb_water.yml
$RUNNER $BIOBB_STRUCTURE_UTILS/utils/renumber_structure.cwl $BIOBB_STRUCTURE_UTILS/test/utils/renumber_structure.yml
$RUNNER $BIOBB_STRUCTURE_UTILS/utils/sort_gro_residues.cwl $BIOBB_STRUCTURE_UTILS/test/utils/sort_gro_residues.yml