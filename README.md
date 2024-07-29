## How to build and run this container:

Find Hugging Face token that is shared on 1password: "Hugginface Jan De Null Read Access to Repo"

# Build
docker build -t ghcr.io/rebatch-ml/doctr:latest . --build-arg HF_TOKEN="your Hugging Face token"

# Run
docker run --gpus all -p 8080:8080 -i -t ghcr.io/rebatch-ml/doctr:latest

# Push
docker push ghcr.io/rebatch-ml/doctr:latest

# Create RunPod Instance
runpodctl create pod --templateId 'c3mqt91fwi' --communityCloud --gpuCount 2 --imageName 'ghcr.io/rebatch-ml/doctr:latest' --gpuType 'NVIDIA L40S' --name 'Test DOCTR' --volumePath '/app/' --volumeSize 40 --containerDiskSize 40

# testing
## unit tests
Unit tests are defined in the tests/unit and can be run with pytest and are discoverable with the vscode testing extension.

## integration tests
Integration tests are written in the tests/integration folder. It has a bash script that can be run, it will build the docker image and do some calls to it for testing then it will remove the docker image again. ATM if you want to test this locally you still need to ensure that you have all packages installed to run the python script. But usually it just requires the requests library.

- additional packages 
    - pymupdf
    - requests

- test command
    - bash tests/integration/test.sh --huggingface_token <hf_TOKEN>