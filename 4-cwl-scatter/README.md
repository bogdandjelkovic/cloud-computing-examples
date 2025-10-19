# Example 4: CWL Workflow with Docker

This task is using same docker contrainer as one in excercise [3](../3-cwl/README.md).

To run CWL workflow, type:

```bash
cwltool --outdir ./results main.cwl main.yml

# or on local withot using docker containers

cwltool --no-container --outdir ./results main.cwl main.yml
```

Link to docker image: [bogdandjelkovic/cc-3-cwl-model-training](https://hub.docker.com/repository/docker/bogdandjelkovic/cc-3-cwl-model-training/general)