cwlVersion: v1.2
class: Workflow

requirements:
  ScatterFeatureRequirement: {}
  StepInputExpressionRequirement: {}

inputs:
  input_file: File
  target_column: string
  k_folds: int

steps:
  preprocess:
    run: data_preparation.cwl
    in:
      dataset_file: input_file
      k_folds: k_folds
      target_column: target_column
    out: [train_files, test_files]

  cross_validation:
    run: model_training.cwl
    scatter: [train_file, test_file]
    scatterMethod: dotproduct
    in:
      train_file: preprocess/train_files
      test_file: preprocess/test_files
      target_column: target_column
    out: [rmse_file]

  aggregate:
    run: aggregate_metrics.cwl
    in:
      rmse_files: cross_validation/rmse_file
    out: [aggregated_rmse]

outputs:
  aggregated_rmse:
    type: File
    outputSource: aggregate/aggregated_rmse
