# 使用Python 3.10官方镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖（X11库作为opencv的备用）
RUN apt-get update && apt-get install -y \
    libxcb-xinerama0 \
    libxcb-cursor0 \
    libxcb1-dev \
    libxext6 \
    libx11-6 \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 复制backend依赖文件
COPY backend/requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制backend应用代码
COPY backend/ .

# 暴露端口（Railway会自动设置PORT环境变量）
EXPOSE 8000

# 启动命令 - 使用Railway的PORT环境变量
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
