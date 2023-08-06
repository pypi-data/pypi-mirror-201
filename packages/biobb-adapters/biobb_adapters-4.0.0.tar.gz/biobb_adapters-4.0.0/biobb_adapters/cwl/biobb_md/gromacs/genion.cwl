#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool
baseCommand: genion
hints:
  DockerRequirement:
    dockerPull: quay.io/biocontainers/biobb_md:0.1.5--py_0
inputs:
  input_tpr_path:
    type: File
    # TODO: Not yet in EDAM
    #format: edam:format_GROMACS_TPR
    inputBinding:
      position: 1
      prefix: --input_tpr_path

  output_gro_path:
    type: string
    inputBinding:
      position: 2
      prefix: --output_gro_path
    default: "structure_ions.gro"

  input_top_zip_path:
    type: File
    format: edam:format_2333
    inputBinding:
      position: 3
      prefix: --input_top_zip_path

  output_top_zip_path:
    type: string
    inputBinding:
      position: 4
      prefix: --output_top_zip_path
    default: "topology_ions_top.zip"

  config:
    type: string?
    inputBinding:
      position: 5
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
