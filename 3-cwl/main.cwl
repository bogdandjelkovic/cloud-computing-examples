class: Workflow
cwlVersion: v1.2

inputs:
    input_file: File
    target_column:
        type: string
    training_percentage:
        type: float

outputs:
    performance_metrics:
        type: File
        outputSource: training/performance_metrics

steps:
    preprocess:
        run: data_preparation.cwl
        in:
            input_file: input_file
        out: [output_file]

    training:
        run: model_training.cwl
        in:
            output_file: output_file
            target_column: target_column
            training_percentage: training_percentage
        out: [performance_metrics]