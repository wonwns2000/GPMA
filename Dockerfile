# Get JDK
FROM openjdk:17-slim AS jdk

# Get Python
FROM python:3.10-slim
LABEL authors="wonwns"

# Copy JDK
COPY --from=jdk /usr/local/openjdk-17 /usr/local/openjdk-17

# Setting JAVA PATH
ENV JAVA_HOME=/usr/local/openjdk-17
ENV PATH=$JAVA_HOME/bin:$PATH

# Get  wget unzip
RUN apt-get update && apt-get install -y wget unzip curl \
    && rm -rf /var/lib/apt/lists/*
# Get git
RUN apt-get update && apt-get install -y git \
    && rm -rf /var/lib/apt/lists/*
# Get PMD
WORKDIR /opt/PMD
RUN wget -q https://github.com/pmd/pmd/releases/download/pmd_releases/7.16.0/pmd-dist-7.16.0-bin.zip \
    && unzip pmd-dist-7.16.0-bin.zip \
    && rm pmd-dist-7.16.0-bin.zip

# Setting PMD PATH
ENV PMD_HOME=/opt/PMD/pmd-bin-7.16.0
ENV PATH=$PMD_HOME/bin:$JAVA_HOME/bin:$PATH

# Get Project
WORKDIR /app
COPY Requirements.txt .
RUN pip install --no-cache-dir -r Requirements.txt
COPY . .

RUN pmd --version
ENTRYPOINT ["python", "src/main.py"]