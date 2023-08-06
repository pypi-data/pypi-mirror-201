#!/usr/bin/env cwl-runner
cwlVersion: v1.0

class: CommandLineTool

label: Wrapper of the AmberTools (AMBER MD Package) pdb4amber tool module.

doc: |-
  Analyse PDB files and clean them for further usage, especially with the LEaP programs of Amber, using pdb4amber tool from the AmberTools MD package.

baseCommand: pdb4amber

hints:
  DockerRequirement:
    dockerPull: ''

inputs:
  input_pdb_path:
    label: Input 3D structure PDB file
    doc: |-
      Input 3D structure PDB file
      Type: string
      File type: input
      Accepted formats: pdb
      Example file: https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/pdb4amber/1aki_fixed.pdb
    type: File
    format:
    - edam:format_1476
    inputBinding:
      position: 1
      prefix: --input_pdb_path

  output_pdb_path:
    label: Output 3D structure PDB file
    doc: |-
      Output 3D structure PDB file
      Type: string
      File type: input
      Accepted formats: pdb
      Example file: https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/pdb4amber/structure.pdb4amber.pdb
    type: File
    format:
    - edam:format_1476
    inputBinding:
      position: 2
      prefix: --output_pdb_path

  config:
    label: Advanced configuration options for biobb_amber.pdb4amber.pdb4amber Pdb4amber
    doc: |-
      Advanced configuration options for biobb_amber.pdb4amber.pdb4amber Pdb4amber. This should be passed as a string containing a dict. The possible options to include here are listed under 'properties' in the biobb_amber.pdb4amber.pdb4amber Pdb4amber documentation: https://biobb-amber.readthedocs.io/en/latest/pdb4amber.html#module-pdb4amber.pdb4amber
    type: string?
    inputBinding:
      prefix: --config

outputs: {}

$namespaces:
  edam: http://edamontology.org/

$schemas:
- https://raw.githubusercontent.com/edamontology/edamontology/master/EDAM_dev.owl
