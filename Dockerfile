# 第一阶段：只拿 JDK
FROM openjdk:17-slim AS jdk

# 第二阶段：Python + JDK
FROM python:3.10-slim
LABEL authors="wonwns"

# 拷贝 JDK 过来
COPY --from=jdk /usr/local/openjdk-17 /usr/local/openjdk-17

# 设置环境变量
ENV JAVA_HOME=/usr/local/openjdk-17
ENV PATH=$JAVA_HOME/bin:$PATH

# 装 wget unzip 等
RUN apt-get update && apt-get install -y wget unzip curl \
    && rm -rf /var/lib/apt/lists/*
# 安装git
RUN apt-get update && apt-get install -y git \
    && rm -rf /var/lib/apt/lists/*
# 下载并解压 PMD
WORKDIR /opt/PMD
RUN wget -q https://github.com/pmd/pmd/releases/download/pmd_releases/7.16.0/pmd-dist-7.16.0-bin.zip \
    && unzip pmd-dist-7.16.0-bin.zip \
    && rm pmd-dist-7.16.0-bin.zip

# 设置 PMD
ENV PMD_HOME=/opt/PMD/pmd-bin-7.16.0
ENV PATH=$PMD_HOME/bin:$JAVA_HOME/bin:$PATH

# 应用代码
WORKDIR /app
COPY Requirements.txt .
RUN pip install --no-cache-dir -r Requirements.txt
COPY . .

RUN pmd --version
ENTRYPOINT ["python", "src/main.py"]