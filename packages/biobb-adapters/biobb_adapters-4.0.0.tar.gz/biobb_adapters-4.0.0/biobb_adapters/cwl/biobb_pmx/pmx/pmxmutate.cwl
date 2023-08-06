#!/usr/bin/env cwl-runner
cwlVersion: v1.0

class: CommandLineTool

label: Wrapper class for the PMX mutate module.

doc: |-
  None

baseCommand: pmxmutate

hints:
  DockerRequirement:
    dockerPull: https://quay.io/repository/biocontainers/biobb_pmx:3.5.0--py_0

inputs:
  input_structure_path:
    label: Path to the input structure file
    doc: |-
      Path to the input structure file
      Type: string
      File type: input
      Accepted formats: pdb, gro
      Example file: https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/data/pmx/frame99.pdb
    type: File
    format:
    - edam:format_1476
    - edam:format_2033
    inputBinding:
      position: 1
      prefix: --input_structure_path

  output_structure_path:
    label: Path to the output structure file
    doc: |-
      Path to the output structure file
      Type: string
      File type: output
      Accepted formats: pdb, gro
      Example file: https://github.com/bioexcel/biobb_pmx/raw/master/biobb_pmx/test/reference/pmx/ref_output_structure.pdb
    type: string
    format:
    - edam:format_1476
    - edam:format_2033
    inputBinding:
      position: 2
      prefix: --output_structure_path
    default: system.pdb

  input_b_structure_path:
    label: Path to the mutated input structure file
    doc: |-
      Path to the mutated input structure file
      Type: string
      File type: input
      Accepted formats: pdb, gro
      Example file: null
    type: File?
    format:
    - edam:format_1476
    - edam:format_2033
    inputBinding:
      prefix: --input_b_structure_path

  config:
    label: Advanced configuration options for biobb_pmx Pmxmutate
    doc: |-
      Advanced configuration options for biobb_pmx Pmxmutate. This should be passed as a string containing a dict. The possible options to include here are listed under 'properties' in the biobb_pmx Pmxmutate documentation: https://biobb-pmx.readthedocs.io/en/latest/pmx.html#module-pmx.pmxmutate
    type: string?
    inputBinding:
      prefix: --config

outputs:
  output_structure_path:
    label: Path to the output structure file
    doc: |-
      Path to the output structure file
    type: File
    outputBinding:
      glob: $(inputs.output_structure_path)

$namespaces:
  edam: http://edamontology.org/

$schemas:
- https://raw.githubusercontent.com/edamontology/edamontology/master/EDAM_dev.owl
