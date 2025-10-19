cwlVersion: v1.2
class: CommandLineTool

baseCommand: ["python", "app/model_training.py"]
# baseCommand: ["python3", "/mnt/c/cc/cloud-computing-examples/4-cwl-scatter/model_training.py"]

hints:
  DockerRequirement:
    dockerPull: bogdandjelkovic/cc-3-cwl-model-training

inputs:
  train_file:
    type: File
    inputBinding:
      position: 1
  test_file:
    type: File
    inputBinding:
      position: 2
  target_column:
    type: string
    inputBinding:
      position: 3

outputs:
  rmse_file:
    type: File
    outputBinding:
      glob: rmse.txt

stdout: rmse.txt