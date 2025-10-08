# DocTR Setup

## Installation

```bash
pip install -r requirements.txt
```

## System Requirements

- Python >= 3.8
- PyTorch >= 2.0.0
- CUDA (optional, for GPU acceleration)

## Configuration

DocTR supports the following parameters in `config/experiments.yaml`:

- `det_arch`: Detection architecture (default: `db_resnet50`)
- `reco_arch`: Recognition architecture (default: `crnn_vgg16_bn`)
- `pretrained`: Use pretrained models (default: `true`)
- `device`: Device to use (`cpu` or `cuda`)
- `measure_time`: Measure processing time (default: `false`)

## Available Models

### Detection Architectures:
- `db_resnet50` - DBNet with ResNet-50 backbone
- `db_mobilenet_v3_large` - DBNet with MobileNetV3

### Recognition Architectures:
- `crnn_vgg16_bn` - CRNN with VGG16-BN
- `crnn_mobilenet_v3_small` - CRNN with MobileNetV3

## Reference

DocTR documentation: https://mindee.github.io/doctr/
