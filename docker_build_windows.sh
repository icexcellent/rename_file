#!/usr/bin/env bash
set -euo pipefail

# 基于 Docker 的 Windows 交叉编译
# 依赖: 已安装 Docker（桌面版/CLI）
# 用法:
#   1) 赋予执行权限: chmod +x docker_build_windows.sh
#   2) 运行(自动尝试多镜像): ./docker_build_windows.sh
#   3) 指定镜像前缀(可选): DOCKER_REGISTRY_MIRROR=https://mirror.ccs.tencentyun.com ./docker_build_windows.sh
#   4) 指定自定义镜像(可选): IMAGE_OVERRIDE=your.registry/cdrx/pyinstaller-windows:latest ./docker_build_windows.sh
# 生成的 exe 位于: dist/windows/FileRenamer.exe 或 dist/FileRenamer.exe

IMAGE_BASE="cdrx/pyinstaller-windows:latest"
# 常用镜像前缀(按优先级尝试)
DEFAULT_MIRRORS=(
  ""                                   # 官方
  "dockerproxy.com/"                   # dockerproxy 镜像
  "registry.docker-cn.com/"           # 旧的官方中国镜像(不一定可用)
  "hub-mirror.c.163.com/"             # 网易
  "mirror.ccs.tencentyun.com/"        # 腾讯云
  "docker.mirrors.ustc.edu.cn/"       # 中科大
  "docker.m.daocloud.io/"             # DaoCloud
)

APP_NAME="FileRenamer"
PYINSTALLER_VERSION="6.15.0"

# 进入脚本所在目录（项目根）
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
cd "$SCRIPT_DIR"

# 参数&环境变量
REGISTRY_MIRROR_PREFIX=${DOCKER_REGISTRY_MIRROR:-}
IMAGE_OVERRIDE=${IMAGE_OVERRIDE:-}

pull_with_retry() {
  local img="$1"
  local tries=${2:-3}
  local delay=${3:-5}
  for ((i=1;i<=tries;i++)); do
    echo "尝试拉取镜像($i/$tries): $img"
    # 直接拉取，输出原始进度(不加任何管道)
    if docker pull "$img"; then
      echo "镜像拉取成功: $img"
      return 0
    fi
    echo "拉取失败，$delay 秒后重试..."
    sleep "$delay"
  done
  return 1
}

resolve_and_pull_image() {
  # 1) 如果指定了完整覆盖镜像，优先使用
  if [[ -n "$IMAGE_OVERRIDE" ]]; then
    pull_with_retry "$IMAGE_OVERRIDE" 2 5 && echo "$IMAGE_OVERRIDE" && return 0
    echo "IMAGE_OVERRIDE 拉取失败: $IMAGE_OVERRIDE"
  fi

  # 2) 如果指定了镜像前缀，先尝试该前缀
  if [[ -n "$REGISTRY_MIRROR_PREFIX" ]]; then
    local img="${REGISTRY_MIRROR_PREFIX}${IMAGE_BASE}"
    pull_with_retry "$img" 2 5 && echo "$img" && return 0
    echo "指定 DOCKER_REGISTRY_MIRROR 拉取失败: $img"
  fi

  # 3) 遍历默认镜像前缀
  for prefix in "${DEFAULT_MIRRORS[@]}"; do
    local candidate
    if [[ -z "$prefix" ]]; then
      candidate="$IMAGE_BASE"
    else
      candidate="${prefix}${IMAGE_BASE}"
    fi
    pull_with_retry "$candidate" 2 5 && echo "$candidate" && return 0
  done

  return 1
}

# 确认 Docker 可用
if ! docker info >/dev/null 2>&1; then
  echo "Docker 未就绪，请先启动 Docker Desktop 后重试。"
  exit 1
fi

# 解析并拉取镜像
echo "开始解析与拉取镜像..."
if ! RESOLVED_IMAGE=$(resolve_and_pull_image); then
  echo "所有镜像源均拉取失败，请检查网络或配置 Docker 加速器。"
  exit 1
fi

echo "已选择镜像: $RESOLVED_IMAGE"

# 清理旧构建
rm -rf dist/ build/ *.spec || true

# 在容器中执行: 安装依赖并打包
# 说明:
# - /src 为项目挂载目录
# - 输出默认位于 /src/dist
# - 使用 --windowed 生成 GUI 程序

DOCKER_CMD="python -m pip install -U pip && \
    pip install -r requirements.txt && \
    pip install -r requirements_gui.txt && \
    pip install pyinstaller==${PYINSTALLER_VERSION} && \
    pyinstaller \
      --onefile \
      --windowed \
      --name=${APP_NAME} \
      --hidden-import=PyQt6.QtCore \
      --hidden-import=PyQt6.QtWidgets \
      --hidden-import=PyQt6.QtGui \
      --hidden-import=pytesseract \
      --hidden-import=pypdf \
      --hidden-import=docx \
      --hidden-import=chardet \
      --hidden-import=requests \
      --hidden-import=json \
      --hidden-import=pathlib \
      --hidden-import=shutil \
      --hidden-import=datetime \
      --hidden-import=re \
      --hidden-import=base64 \
      --hidden-import=PIL \
      --hidden-import=PIL.Image \
      --hidden-import=pdfplumber \
      file_renamer_gui.py"

echo "开始 Docker 交叉编译 Windows 可执行文件..."
# 不使用任何管道，完整展示构建过程与进度
docker run --rm \
  -v "$PWD":/src \
  -w /src \
  "$RESOLVED_IMAGE" \
  bash -lc "$DOCKER_CMD"

# 结果提示
if [ -f "dist/${APP_NAME}.exe" ]; then
  OUT_PATH="dist/${APP_NAME}.exe"
elif [ -f "dist/windows/${APP_NAME}.exe" ]; then
  OUT_PATH="dist/windows/${APP_NAME}.exe"
else
  OUT_PATH=""
fi

if [ -n "$OUT_PATH" ]; then
  echo "\n✅ 构建成功: $OUT_PATH"
else
  echo "\n❌ 未找到生成的 exe，请查看上方日志排查。"
  exit 1
fi
