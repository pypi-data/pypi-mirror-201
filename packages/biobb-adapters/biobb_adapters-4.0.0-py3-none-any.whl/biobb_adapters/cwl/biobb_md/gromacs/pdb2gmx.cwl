#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool
baseCommand: pdb2gmx
hints:
  DockerRequirement:
    dockerPull: quay.io/biocontainers/biobb_md:0.1.5--py_0
inputs:
  input_pdb_path:
    type: File
    format: edam:format_1476
    inputBinding:
      position: 1
      prefix: --input_pdb_path

  output_gro_path:
    type: string
    inputBinding:
      position: 2
      prefix: --output_gro_path
    default: "structure.gro"

  output_top_zip_path:
    type: string
    inputBinding:
      position: 3
      prefix: --output_top_zip_path
    default: "topology.zip"

  config:
    type: string?
    inputBinding:
      position: 4
      prefix: --config

outputs:
  output_gro_file:
    type: File
    format: edam:format_GROMACS_GRO
    outputBinding:
      glob: $(inputs.output_gro_path)
  output_top_zip_file:
    type: File
    format: edam:format_2333
    outputBinding:
      glob: $(inputs.output_top_zip_path)

$namespaces:
  edam: http://edamontology.org/
$schemas:
  - https://raw.githubusercontent.com/edamontology/edamontology/master/EDAM_dev.owl
