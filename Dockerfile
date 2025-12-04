# Dockerfile - container da aplicação (Spark + Python + Jupyter)
FROM python:3.11-slim

# Instalar Java (necessário para Spark) e dependências do pyodbc
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        default-jdk-headless \
        unixodbc-dev \
        build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Descobrir onde o Java foi instalado automaticamente
RUN echo "JAVA_HOME guess:" && readlink -f /usr/bin/java || true

# Diretório de trabalho dentro do container
WORKDIR /app

# Copiar requirements e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar TODO o projeto para dentro da imagem
COPY . .

# Expor a porta do Jupyter
EXPOSE 8888

# Comando padrão: subir Jupyter Lab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
