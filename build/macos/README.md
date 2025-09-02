# 🍎 macOS构建说明

本文件夹包含用于构建macOS版本FileRenamer的所有文件。

## 📁 文件说明

- `Dockerfile` - Docker镜像构建配置
- `docker_build.sh` - macOS构建脚本
- `.dockerignore` - Docker构建忽略文件

## 🚀 使用方法

### 前置要求
1. 确保Docker Desktop已启动
2. 确保有足够的磁盘空间（至少2GB）

### 构建步骤
```bash
# 进入构建目录
cd build/macos

# 运行构建脚本
./docker_build.sh
```

### 构建完成后
- 可执行文件将保存在项目根目录：`../FileRenamer`
- 文件大小约300-320MB
- 支持Apple Silicon (ARM64) 和 Intel (x64) 架构

## 🔧 构建配置

### Docker镜像优化
- 使用国内镜像源（阿里云apt源 + 清华大学pip源）
- 优化依赖安装顺序
- 充分利用Docker缓存

### 构建时间
- 首次构建：约2-3分钟
- 后续构建：约30秒（利用缓存）

## 📋 系统要求

- macOS 10.15+ (Catalina)
- Docker Desktop 4.0+
- 至少4GB内存
- 至少2GB可用磁盘空间

## 🐛 故障排除

### 常见问题
1. **Docker未启动**: 启动Docker Desktop
2. **权限不足**: 确保脚本有执行权限 `chmod +x docker_build.sh`
3. **磁盘空间不足**: 清理Docker缓存 `docker system prune -f`

### 清理命令
```bash
# 清理Docker缓存
docker system prune -f

# 清理构建产物
rm -f ../FileRenamer
```
