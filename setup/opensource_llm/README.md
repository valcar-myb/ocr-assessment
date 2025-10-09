# Open-source LLM Setup via vLLM

This directory contains setup instructions for running open-source multimodal LLMs using vLLM with OpenAI-compatible API.

## Overview

Open-source LLMs are served on a **separate GPU server** using [vLLM](https://github.com/vllm-project/vllm), which provides:
- High-throughput serving with PagedAttention
- OpenAI-compatible API endpoint
- Efficient GPU memory management
- Docker-based deployment

## Supported Models

| Model | HuggingFace ID |
|-------|----------------|
| Qwen 2.5 VL (3B) | `Qwen/Qwen2.5-VL-3B-Instruct`|
| Gemma 3 (2B) | `google/gemma-3-2b-it` |

## Target Machine Requirements

The vLLM server should run on a **dedicated GPU machine** (local workstation or cloud instance like AWS EC2 g5.xlarge).

### Hardware Requirements
- **GPU**: NVIDIA GPU with CUDA support
  - Minimum: 12GB VRAM (for Qwen 2.5 VL 3B)
  - Recommended: 16GB+ VRAM
- **CPU**: 8+ cores
- **RAM**: 32GB+ system RAM
- **Storage**: 50GB+ free space (for model downloads)

### Software Requirements
- **OS**: Linux (Ubuntu 20.04+ recommended)
- **Docker**: Docker 20.10+ with NVIDIA Container Toolkit
- **NVIDIA Driver**: Latest stable driver (535.x+)
- **CUDA**: Compatible with your GPU (CUDA 11.8+ or 12.x)

## Setup on Target Machine

### 1. Install Docker and NVIDIA Container Toolkit

```bash
# Install Docker (Ubuntu)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker

# Test GPU access
docker run --rm --gpus all nvidia/cuda:12.0.0-base-ubuntu22.04 nvidia-smi
```

### 2. Pull vLLM Docker Image

```bash
docker pull vllm/vllm-openai:latest
```

### 3. Start vLLM Server

Use the provided script:

```bash
# For Qwen 2.5 VL
bash start_vllm_server.sh Qwen/Qwen2.5-VL-3B-Instruct 8000

# For Gemma 3
bash start_vllm_server.sh google/gemma-3-2b-it 8001
```

**Script Parameters:**
- `MODEL_NAME`: HuggingFace model identifier
- `PORT`: Port to expose (8000, 8001, etc.)

### 4. Verify Server is Running

```bash
# Check container status
docker ps | grep vllm

# Check API endpoint
curl http://localhost:8000/v1/models

# View logs
docker logs -f vllm-qwen2.5-vl-3b-instruct-8000
```

## Network Configuration

If the vLLM server is on a **remote machine**, update the `api_url` in your configuration:

```yaml
config:
  api_url: "http://<GPU_SERVER_IP>:8000/v1/chat/completions"
```

If running **locally**, use:
```yaml
config:
  api_url: "http://localhost:8000/v1/chat/completions"
```

## Configuration

Open-source LLM systems use the following parameters in `config/experiments.yaml`:

- `api_url`: vLLM API endpoint (default: `http://localhost:8000/v1/chat/completions`)
- `hf_model_name`: HuggingFace model identifier (required)
- `prompt`: Custom OCR prompt (optional)
- `max_tokens`: Maximum tokens in response (default: `1024`)
- `temperature`: Sampling temperature (default: `0.0`)
- `measure_time`: Measure processing time (default: `false`)

### Example Configuration

```yaml
ocr_systems:
  - name: "qwen25vl"
    type: "opensource_llm"
    config:
      api_url: "http://localhost:8000/v1/chat/completions"  # Or remote IP
      hf_model_name: "Qwen/Qwen2.5-VL-3B-Instruct"
      prompt: "Extract all visible text from this document image. Return only the text"
      max_tokens: 1024
      temperature: 0.0
      measure_time: true
      
  - name: "gemma3"
    type: "opensource_llm"
    config:
      api_url: "http://localhost:8001/v1/chat/completions"  # Different port
      hf_model_name: "google/gemma-3-2b-it"
      prompt: "Extract all visible text from this document image. Return only the text"
      max_tokens: 1024
      temperature: 0.0
      measure_time: true
```

## Architecture

All open-source LLM implementations:
1. Convert images to base64 PNG format
2. Send requests to vLLM server via OpenAI-compatible API
3. Parse responses in OpenAI chat completion format
4. Return raw JSON output for evaluation


## Complete Workflow

### On GPU Server (Target Machine):
1. Install Docker and NVIDIA Container Toolkit (Steps 1-4)
2. Pull vLLM image (Step 5)
3. Start server with `start_vllm_server.sh` (Step 7)
4. Keep server running during experiments

### On Benchmark Machine:
1. Install dependencies: `pip install -r requirements.txt`
2. Configure `api_url` in `config/experiments.yaml` to point to GPU server
3. Run experiments as usual

## Files in This Directory

- **README.md**: This file - main setup guide
- **DEPLOYMENT.md**: Detailed deployment checklist for target machine
- **start_vllm_server.sh**: Script to start vLLM Docker container
- **requirements.txt**: Python dependencies (minimal, for benchmark machine)

## Reference

- vLLM documentation: https://docs.vllm.ai
- vLLM Docker: https://docs.vllm.ai/en/latest/serving/deploying_with_docker.html
- NVIDIA Container Toolkit: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/
- Qwen 2.5 VL: https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct
- Gemma 3: https://huggingface.co/google/gemma-3-2b-it

