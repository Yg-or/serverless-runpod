FROM python:3.10

WORKDIR /

# Instalar dependências mínimas
RUN apt-get update && apt-get install -y cmake && rm -rf /var/lib/apt/lists/*

# Instalar pacotes em ordem
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir numpy==1.24.3 && \
    pip install --no-cache-dir dlib==19.24.2 && \
    pip install --no-cache-dir face-recognition==1.3.0 && \
    pip install --no-cache-dir opencv-python-headless==4.8.1.78 && \
    pip install --no-cache-dir pillow==10.1.0 && \
    pip install --no-cache-dir requests==2.31.0 && \
    pip install --no-cache-dir runpod==1.7.2

COPY handler.py /

CMD ["python3", "-u", "handler.py"]