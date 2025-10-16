cwlVersion: v1.2
class: CommandLineTool

baseCommand: ["python", "app/model_training.py"]

# no container run
# baseCommand: ["python3", "/mnt/c/cc/cloud-computing-examples/3-cwl/model_training.py"]

hints:
    DockerRequirement:
        dockerPull: bogdandjelkovic/cc-3-cwl-model-training

inputs:
    cleaned_dataset:
        type: File
        inputBinding:
            position: 1
    target_column:
        type: string
        inputBinding:
            position: 2
    training_percentage:
        type: float
        inputBinding:
            position: 3

outputs:
    performance_metrics:
        type: stdout

stdout: performance_metrics.txt