#!/bin/bash

echo "🐳 Docker构建脚本 - FileRenamer应用"
echo "=================================="

# 检查Docker是否运行
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker未运行，请启动Docker"
    exit 1
fi

# 设置变量
IMAGE_NAME="filerenamer-builder"
CONTAINER_NAME="filerenamer-build"
BUILD_DIR="docker_build"

echo "🔧 准备构建环境..."

# 创建构建目录
mkdir -p $BUILD_DIR

# 复制必要文件到构建目录
echo "📁 复制文件到构建目录..."
cp file_renamer_gui.py $BUILD_DIR/
cp deepseek_api_service.py $BUILD_DIR/
cp requirements.txt $BUILD_DIR/
cp requirements_gui.txt $BUILD_DIR/
cp app_config.json $BUILD_DIR/
cp config.json $BUILD_DIR/
cp .gitignore $BUILD_DIR/

# 复制test_file目录（如果存在）
if [ -d "test_file" ]; then
    cp -r test_file $BUILD_DIR/
fi

echo "🏗️ 构建Docker镜像..."
docker build -t $IMAGE_NAME $BUILD_DIR

if [ $? -ne 0 ]; then
    echo "❌ Docker镜像构建失败"
    exit 1
fi

echo "✅ Docker镜像构建成功"

echo "🚀 运行构建容器..."
docker run --name $CONTAINER_NAME $IMAGE_NAME

if [ $? -ne 0 ]; then
    echo "❌ 容器运行失败"
    exit 1
fi

echo "📦 复制构建产物..."
docker cp $CONTAINER_NAME:/app/dist/FileRenamer ./FileRenamer

if [ -f "./FileRenamer" ]; then
    echo "✅ 构建产物复制成功"
    echo "📏 文件大小: $(du -h ./FileRenamer | cut -f1)"
else
    echo "❌ 构建产物复制失败"
fi

echo "🧹 清理容器..."
docker rm $CONTAINER_NAME

echo "🎉 构建完成！"
echo "📁 可执行文件: ./FileRenamer"
