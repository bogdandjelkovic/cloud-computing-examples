# Example 3: CWL Workflow with Docker

Commands to build and run the CWL workflow using Docker:

```bash
# Build Docker image from current directory
docker build -t bogdandjelkovic/cc-3-cwl-model-training .
```

```bash
# Push Docker image to Docker Hub
docker tag bogdandjelkovic/cc-3-cwl-model-training bogdandjelkovic/cc-3-cwl-model-training
docker push bogdandjelkovic/cc-3-cwl-model-training
```

```bash
# Install cwtool on local PC
pip install cwltool 
```

```bash
# Run CWL workflow with input file
cwltool main.cwl main.yml
```

Link to docker image: [bogdandjelkovic/cc-3-cwl-model-training](https://hub.docker.com/repository/docker/bogdandjelkovic/cc-3-cwl-model-training/general)