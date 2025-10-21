# Example 3: CWL Workflow with Docker

Commands to build and run the CWL workflow using Docker:

```bash
# Build Docker image from current directory
docker build -t bogdandjelkovic/6-kubernetes-ml .
```

```bash
# Push Docker image to Docker Hub
docker tag bogdandjelkovic/6-kubernetes-ml bogdandjelkovic/6-kubernetes-ml
docker push bogdandjelkovic/6-kubernetes-ml
```

```bash
# Install cwtool on local PC
pip install cwltool 
```

Run CWL workflow with input file

```bash
cwltool --outdir ./results main.cwl main.yml

# or on local withot using docker containers

cwltool --no-container --outdir ./results main.cwl main.yml
```

Link to docker image: [bogdandjelkovic/6-kubernetes-ml](https://hub.docker.com/repository/docker/bogdandjelkovic/6-kubernetes-ml/general)