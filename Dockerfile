FROM python:3.10
LABEL authors="wonwns"



# 设置 PMD 安装目录
WORKDIR /opt/PMD
# 下载并解压 PMD
RUN wget https://github.com/pmd/pmd/releases/download/pmd_releases/7.16.0/pmd-dist-7.16.0-bin.zip && \
    unzip pmd-dist-7.16.0-bin.zip && \
    rm pmd-dist-7.16.0-bin.zip


#get JAVA
RUN sed -i 's#deb.debian.org#mirrors.aliyun.com#g' /etc/apt/sources.list && \
    sed -i 's#security.debian.org#mirrors.aliyun.com#g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y openjdk-17-jdk wget unzip curl && \
    rm -rf /var/lib/apt/lists/*

# 设置 JAVA_HOME 和 PATH
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH






# 设置 PMD_HOME 环境变量
ENV PMD_HOME=/opt/PMD/pmd-bin-7.16.0
ENV PATH=$PMD_HOME/bin:$PATH

# 设置项目工作目录
WORKDIR /app

# 拷贝依赖文件并安装
COPY Requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 拷贝整个项目
COPY . .

# 默认命令
CMD ["python", "src/main.py"]

