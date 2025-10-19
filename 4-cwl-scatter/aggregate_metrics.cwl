cwlVersion: v1.2
class: CommandLineTool

baseCommand: ["python", "app/aggregate_metrics.py"]
# baseCommand: ["python3", "/mnt/c/cc/cloud-computing-examples/4-cwl-scatter/aggregate_metrics.py"]

hints:
  DockerRequirement:
    dockerPull: bogdandjelkovic/cc-3-cwl-model-training

inputs:
  rmse_files:
    type:
      type: array
      items: File
    inputBinding:
      prefix: ""   # positional arguments
      
stdout: aggregated_rmse.txt

outputs:
  aggregated_rmse:
    type: stdout
