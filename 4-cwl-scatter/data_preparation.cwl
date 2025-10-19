cwlVersion: v1.2
class: CommandLineTool

baseCommand: ["python", "app/data_preparation.py"]
# baseCommand: ["python3", "/mnt/c/cc/cloud-computing-examples/4-cwl-scatter/data_preparation.py"]

hints:
  DockerRequirement:
    dockerPull: bogdandjelkovic/cc-3-cwl-model-training

inputs:
  dataset_file:
    type: File
    inputBinding:
      position: 1
  k_folds:
    type: int
    inputBinding:
      position: 2
  target_column:
    type: string
    inputBinding:
      position: 3

outputs:
  train_files:
    type:
      type: array
      items: File
    outputBinding:
      glob: "folds/train/*.csv"

  test_files:
    type:
      type: array
      items: File
    outputBinding:
      glob: "folds/test/*.csv"

