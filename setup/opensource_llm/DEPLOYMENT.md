# vLLM Deployment on AWS EC2

## Experimental Setup

**Instance Type**: g5.xlarge (24GB VRAM, 1 NVIDIA A10G GPU)

**AMI**: AWS Deep Learning AMI (Ubuntu 20.04 or 22.04)
- Search for "Deep Learning AMI GPU" in AWS Marketplace when launching instance
- AMI includes pre-installed: NVIDIA drivers, CUDA toolkit, Docker, NVIDIA Container Toolkit
- No additional setup required

## Deployment Steps

1. **Launch EC2 Instance**
   - Instance type: g5.xlarge
   - AMI: AWS Deep Learning AMI GPU PyTorch (Ubuntu 22.04)
   - Storage: 100GB+ EBS volume
   - Key pair: Create or use existing

3. **SSH into Instance**
   ```bash
   ssh -i your-key.pem ubuntu@<EC2_PUBLIC_IP>
   ```

4. **Copy Deployment Script**
   ```bash
   # From your local machine
   scp -i your-key.pem setup/opensource_llm/start_vllm_server.sh ubuntu@<EC2_PUBLIC_IP>:~/
   ```

5. **Start vLLM Server**
   ```bash
   # On EC2 instance
   chmod +x start_vllm_server.sh
   
   # Start Qwen 2.5 VL
   ./start_vllm_server.sh Qwen/Qwen2.5-VL-3B-Instruct 8000
   
   # Or start Gemma 3
   ./start_vllm_server.sh google/gemma-3-2b-it 8001
   ```

6. **Update Benchmark Configuration**
   
   In `config/experiments.yaml`, set the `api_url` to your EC2 public IP:
   ```yaml
   config:
     api_url: "http://<EC2_PUBLIC_IP>:8000/v1/chat/completions"
   ```

7. **Verify Connection**
   ```bash
   # From your local/benchmark machine
   curl http://<EC2_PUBLIC_IP>:8000/v1/models
   ```

## Cost Estimation

- **g5.xlarge**: ~$1.00/hour (on-demand)
- **Storage**: ~$0.10/GB/month for EBS
- **Network**: Data transfer costs apply

**Tip**: Use EC2 Spot Instances to save ~70% on compute costs.

## Managing the Server

```bash
# View running containers
docker ps

# View logs
docker logs -f vllm-qwen2.5-vl-3b-instruct-8000

# Stop server
docker stop vllm-qwen2.5-vl-3b-instruct-8000

# Restart server
docker restart vllm-qwen2.5-vl-3b-instruct-8000
```

## Stopping the Instance

When experiments are complete, **stop or terminate** the EC2 instance to avoid charges:

```bash
# From AWS Console or CLI
aws ec2 stop-instances --instance-ids <INSTANCE_ID>
```
