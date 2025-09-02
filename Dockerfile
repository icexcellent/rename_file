FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-chi-sim \
    tesseract-ocr-eng \
    libopencv-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgthread-2.0-0 \
    libgtk-3-0 \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libatlas-base-dev \
    gfortran \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制requirements文件
COPY requirements.txt requirements_gui.txt ./

# 安装Python依赖
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r requirements_gui.txt && \
    pip install --no-cache-dir pyinstaller

# 复制应用代码
COPY . .

# 设置环境变量
ENV PYTHONPATH=/app
ENV TESSDATA_PREFIX=/usr/share/tessdata
ENV EASYOCR_MODULE_PATH=/app/easyocr_models

# 创建构建脚本
RUN echo '#!/bin/bash\n\
echo "开始构建应用..."\n\
echo "清理之前的构建..."\n\
rm -rf build dist\n\
echo "使用PyInstaller构建..."\n\
pyinstaller --onefile --windowed --name=FileRenamer --clean \\\n\
  --hidden-import=pkg_resources \\\n\
  --hidden-import=pkg_resources.extern.pyparsing \\\n\
  --hidden-import=pkg_resources.extern.packaging \\\n\
  --hidden-import=pyparsing \\\n\
  --hidden-import=packaging \\\n\
  --hidden-import=PyQt6.QtCore \\\n\
  --hidden-import=PyQt6.QtWidgets \\\n\
  --hidden-import=PyQt6.QtGui \\\n\
  --hidden-import=pytesseract \\\n\
  --hidden-import=PIL \\\n\
  --hidden-import=PIL.Image \\\n\
  --hidden-import=cv2 \\\n\
  --hidden-import=easyocr \\\n\
  --hidden-import=requests \\\n\
  --hidden-import=urllib3 \\\n\
  --hidden-import=threading \\\n\
  --hidden-import=queue \\\n\
  --collect-all=pytesseract \\\n\
  --collect-all=PIL \\\n\
  --collect-all=cv2 \\\n\
  --collect-all=easyocr \\\n\
  file_renamer_gui.py\n\
echo "构建完成！"\n\
echo "检查构建结果..."\n\
if [ -f "dist/FileRenamer" ]; then\n\
    echo "✅ 构建成功！文件大小: $(du -h dist/FileRenamer | cut -f1)"\n\
else\n\
    echo "❌ 构建失败"\n\
    exit 1\n\
fi' > /app/build.sh && chmod +x /app/build.sh

# 设置默认命令
CMD ["/app/build.sh"]
