#!/usr/bin/env cwl-runner
cwlVersion: v1.0

class: CommandLineTool

label: This class is a wrapper of the Structure Checking tool to extract a protein
  from a 3D structure.

doc: |-
  Wrapper for the Structure Checking tool to extract a protein from a 3D structure.

baseCommand: extract_protein

hints:
  DockerRequirement:
    dockerPull: https://quay.io/biocontainers/biobb_structure_utils:3.5.2--py_0

inputs:
  input_structure_path:
    label: Input structure file path
    doc: |-
      Input structure file path
      Type: string
      File type: input
      Accepted formats: pdb
      Example file: https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/extract_protein.pdb
    type: File
    format:
    - edam:format_1476
    inputBinding:
      position: 1
      prefix: --input_structure_path

  output_protein_path:
    label: Output protein file path
    doc: |-
      Output protein file path
      Type: string
      File type: output
      Accepted formats: pdb
      Example file: https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/ref_extract_protein.pdb
    type: string
    format:
    - edam:format_1476
    inputBinding:
      position: 2
      prefix: --output_protein_path
    default: system.pdb

  config:
    label: Advanced configuration options for biobb_structure_utils ExtractProtein
    doc: |-
      Advanced configuration options for biobb_structure_utils ExtractProtein. This should be passed as a string containing a dict. The possible options to include here are listed under 'properties' in the biobb_structure_utils ExtractProtein documentation: https://biobb-structure-utils.readthedocs.io/en/latest/utils.html#module-utils.extract_protein
    type: string?
    inputBinding:
      prefix: --config

outputs:
  output_protein_path:
    label: Output protein file path
    doc: |-
      Output protein file path
    type: File
    outputBinding:
      glob: $(inputs.output_protein_path)
    format: edam:format_1476

$namespaces:
  edam: http://edamontology.org/

$schemas:
- https://raw.githubusercontent.com/edamontology/edamontology/master/EDAM_dev.owl
