#!/bin/bash
set -e

if [ $# -lt 2 ]; then
  echo "Usage: $0 <MODEL_NAME> <PORT>"
  echo "Example: $0 Qwen/Qwen2.5-VL-3B-Instruct 8000"
  exit 1
fi

MODEL_NAME=$1
PORT=$2
IMAGE="vllm/vllm-openai:latest"

CONTAINER_NAME=$(echo "vllm-$(basename $MODEL_NAME)-$PORT" | tr '[:upper:]' '[:lower:]' | tr '/' '-')

echo "[INFO] Starting vLLM server: ${MODEL_NAME} on port ${PORT}"
docker ps -q --filter "name=${CONTAINER_NAME}" | grep -q . && docker rm -f ${CONTAINER_NAME}

docker run --gpus all -d \
  -p ${PORT}:8000 \
  --name ${CONTAINER_NAME} \
  ${IMAGE} \
  --model ${MODEL_NAME} \
  --trust-remote-code \
  --max-model-len 4096 \
  --gpu-memory-utilization 0.9

echo "[✓] Server started: ${CONTAINER_NAME}"
echo "    Logs: docker logs -f ${CONTAINER_NAME}"
echo "    Test: curl http://localhost:${PORT}/v1/models"

