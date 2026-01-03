FROM python:3.10-slim

WORKDIR /

# Instalar dependências do sistema necessárias para compilar dlib e opencv
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Atualizar pip
RUN pip install --no-cache-dir --upgrade pip

COPY requirements.txt /requirements.txt

# Instalar pacotes Python
RUN pip install --no-cache-dir -r requirements.txt

COPY handler.py /

# Start the container
CMD ["python3", "-u", "handler.py"]