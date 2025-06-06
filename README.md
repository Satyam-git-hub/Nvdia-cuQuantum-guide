# 🚀 cuQuantum Appliance on ARM64 with CUDA

This guide walks you through setting up the **NVIDIA cuQuantum Appliance** on an **ARM64-based Ubuntu server** with **CUDA support** already installed.

## 📋 Prerequisites

- ARM64-based server (e.g., Ampere Altra, Graviton, Jetson, etc.)
- Ubuntu 20.04 / 22.04
- NVIDIA GPU with CUDA installed and functional
- Docker installed (`docker version` should work)

---

## 🐳 Step 1: Install Docker (if not already installed)

```bash
sudo apt update
sudo apt install -y docker.io
sudo systemctl enable --now docker
````

Optional: Add your user to the `docker` group so you can run Docker without `sudo`.

```bash
sudo usermod -aG docker $USER
newgrp docker
```

---

## 🧰 Step 2: Install NVIDIA Container Toolkit

Set up the NVIDIA container repository:

```bash
distribution=$(. /etc/os-release; echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/libnvidia-container/gpgkey | \
  sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/nvidia-container.gpg

curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-container.list
```

Then install the toolkit:

```bash
sudo apt update
sudo apt install -y nvidia-container-toolkit
```

Configure Docker to use the NVIDIA runtime:

```bash
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

---

## 🧪 Step 3: Verify GPU Access in Docker

```bash
docker run --rm --gpus all nvidia/cuda:12.2.0-base-ubuntu22.04 nvidia-smi
```

You should see your GPU listed.

---

## 📦 Step 4: Pull cuQuantum Appliance Container (ARM64)

```bash
docker pull nvcr.io/nvidia/cuquantum-appliance:24.08-cuda12.2.2-devel-ubuntu22.04-arm64
```

> 💡 Replace `24.08` with the latest tag if needed: [https://catalog.ngc.nvidia.com/orgs/nvidia/containers/cuquantum-appliance](https://catalog.ngc.nvidia.com/orgs/nvidia/containers/cuquantum-appliance)

---

## ▶️ Step 5: Run cuQuantum Appliance Container

### Attached mode
```bash
docker run --gpus all -it --rm \
  nvcr.io/nvidia/cuquantum-appliance:24.08-cuda12.2.2-devel-ubuntu22.04-arm64
```

### Detached mode (-d)
```bash
docker run -d --gpus all --name cuquantum-arm64 \
  nvcr.io/nvidia/cuquantum-appliance:24.08-cuda12.2.2-devel-ubuntu22.04-arm64 sleep infinity

```

---

## 🧠 Step 6: Learn and Experiment Inside the Container

Explore installed tools:

```bash
conda info --envs
nvcc --version
python --version
```

Run a sample program:

```bash
cd /opt/cuquantum/examples/cutensornet
python3 einsum_network.py
```

Try out your own mini tensor contraction:

```python
from cuquantum import cutensornet as cutn
import numpy as np

A = np.random.rand(2,2).astype(np.float32)
B = np.random.rand(2,2).astype(np.float32)
C = np.einsum('ij,jk->ik', A, B)
print("Einsum result:\n", C)
```

---

## 🛠 Troubleshooting

If you face OpenSSL issues when using SSH inside the container:

```bash
export LD_PRELOAD=/usr/lib/aarch64-linux-gnu/libcrypto.so.3
```

---

## 📚 Resources

* [cuQuantum SDK Docs](https://docs.nvidia.com/cuda/cuquantum/index.html)
* [NGC cuQuantum Appliance](https://catalog.ngc.nvidia.com/orgs/nvidia/containers/cuquantum-appliance)

---

> Happy quantum hacking on ARM64! 🧪⚛️💥

```

---

Let me know if you want this bundled as a [GitHub-ready repo](f), [Docker Compose setup](f), or [cuQuantum project starter](f)!
```

