cwlVersion: v1.2
class: CommandLineTool
baseCommand: ["python", "/app/data_preparation.py"]

hints:
    DockerRequirement:
        dockerPull: bogdandjelkovic/cc-3-cwl-model-training

inputs:
    dataset_file:
    type: File
    inputBinding:
        position: 1

outputs:
    cleaned_dataset:
        type: stdout

stdout: cleaned_dataset.csv