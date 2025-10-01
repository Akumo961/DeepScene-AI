# Use official PyTorch image (includes CUDA + Python)
FROM pytorch/pytorch:2.2.0-cuda12.1-cudnn8-runtime

# Set working directory
WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    wget \
    curl \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY requirements.txt .
COPY src ./src
COPY data ./data
COPY notebooks ./notebooks

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Jupyter notebook port
EXPOSE 8888

# Start Jupyter notebook by default
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]