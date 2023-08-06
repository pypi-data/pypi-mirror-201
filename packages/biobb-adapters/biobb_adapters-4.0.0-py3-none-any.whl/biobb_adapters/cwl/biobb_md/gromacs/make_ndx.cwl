#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool
baseCommand: make_ndx
hints:
  DockerRequirement:
    dockerPull: quay.io/biocontainers/biobb_md:0.1.5--py_0
inputs:
  input_structure_path:
    type: File
    format: edam:format_GROMACS_GRO
    inputBinding:
      position: 1
      prefix: --input_structure_path

  output_ndx_path:
    type: string
    inputBinding:
      position: 2
      prefix: --output_ndx_path
    default: "custom_index.ndx"

  input_ndx_path:
    type: File?
    format: edam:format_2330
    inputBinding:
      prefix: --input_ndx_path

  config:
    type: string?
    inputBinding:
      prefix: --config

outputs:
  output_ndx_file:
    type: File
    format: edam:format_2330
    outputBinding:
      glob: $(inputs.output_ndx_path)

$namespaces:
  edam: http://edamontology.org/
$schemas:
  - https://raw.githubusercontent.com/edamontology/edamontology/master/EDAM_dev.owl
