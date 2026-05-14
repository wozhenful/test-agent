# 智能自适应能力测评系统 - 部署指南

## 📋 目录

- [快速开始](#快速开始)
- [本地开发](#本地开发)
- [云服务器部署](#云服务器部署)
- [Docker部署](#docker部署)
- [配置说明](#配置说明)
- [常见问题](#常见问题)

---

## 🚀 快速开始

### 环境要求

- Python 3.10+
- uv 包管理器
- 网络连接（用于调用LLM API）

### 安装步骤

```bash
# 1. 克隆项目
git clone https://github.com/wozhenful/test-agent.git
cd test-agent

# 2. 安装依赖
pip install uv
uv sync

# 3. 启动服务
uv run python src/main.py
```

服务将在 **http://localhost:9000** 启动

---

## 🖥️ 本地开发

### 使用Web界面

```bash
# 启动Web服务
uv run python src/web_main.py
```

访问 **http://localhost:9000** 查看Web界面

### 使用API

```bash
# 测试聊天API
curl -X POST http://localhost:9000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "我想做逻辑推理测评"}'

# 测试语音识别
curl -X POST http://localhost:9000/api/asr \
  -F "audio=@audio.mp3"
```

---

## ☁️ 云服务器部署

### 推荐配置

| 配置项 | 最低要求 | 推荐配置 |
|--------|----------|----------|
| CPU | 1核 | 2核 |
| 内存 | 1GB | 2GB |
| 带宽 | 1Mbps | 3Mbps |
| 系统 | Ubuntu 22.04 LTS | Ubuntu 22.04 LTS |

### 部署步骤

#### 1. 服务器环境准备

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装Python
sudo apt install python3.11 python3.11-venv python3-pip -y

# 安装Git
sudo apt install git -y

# 安装Nginx
sudo apt install nginx -y
```

#### 2. 部署代码

```bash
# 克隆项目
cd /var/www
sudo git clone https://github.com/wozhenful/test-agent.git
cd test-agent

# 安装依赖
sudo pip3 install uv
sudo uv sync

# 设置权限
sudo chown -R www-data:www-data /var/www/test-agent
```

#### 3. 配置Systemd服务

```bash
sudo nano /etc/systemd/system/assessment-agent.service
```

添加以下内容：

```ini
[Unit]
Description=Assessment Agent Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/test-agent
ExecStart=/var/www/test-agent/.venv/bin/python src/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl start assessment-agent
sudo systemctl enable assessment-agent
```

#### 4. 配置Nginx反向代理

```bash
sudo nano /etc/nginx/sites-available/assessment-agent
```

添加以下内容：

```nginx
server {
    listen 80;
    server_name your-domain.com;  # 替换为您的域名或IP

    location / {
        proxy_pass http://127.0.0.1:9000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_buffering off;
    }
}
```

启用配置：

```bash
sudo ln -s /etc/nginx/sites-available/assessment-agent /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 5. 配置HTTPS（推荐）

使用Let's Encrypt免费证书：

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

---

## 🐳 Docker部署

### 构建Docker镜像

```bash
# 构建镜像
docker build -t assessment-agent .

# 运行容器
docker run -d \
  --name assessment-agent \
  -p 9000:9000 \
  -e COZE_WORKLOAD_IDENTITY_API_KEY=your_api_key \
  assessment-agent
```

### 使用Docker Compose

创建 `docker-compose.yml`：

```yaml
version: '3.8'

services:
  assessment-agent:
    build: .
    ports:
      - "9000:9000"
    environment:
      - COZE_WORKLOAD_IDENTITY_API_KEY=${COZE_API_KEY}
    restart: always
```

启动：

```bash
docker-compose up -d
```

---

## ⚙️ 配置说明

### 环境变量

| 变量名 | 必填 | 说明 |
|--------|------|------|
| `COZE_WORKLOAD_IDENTITY_API_KEY` | 是 | API密钥 |
| `COZE_INTEGRATION_MODEL_BASE_URL` | 否 | 模型API地址 |
| `COZE_WORKSPACE_PATH` | 否 | 工作目录路径 |

### 配置文件

- `config/agent_llm_config.json` - Agent配置和系统提示词
- `.coze` - Coze平台配置

---

## ❓ 常见问题

### 1. 依赖安装失败

**问题**: `uv sync` 报错

**解决**:
```bash
# 清理并重新安装
rm -rf .venv
uv sync --refresh
```

### 2. 端口被占用

**问题**: `Port 9000 is already in use`

**解决**:
```bash
# 查找占用进程
lsof -i :9000
# 杀死进程
kill -9 <PID>
```

### 3. 语音功能无法使用

**问题**: 麦克风权限被拒绝

**解决**:
- 确保使用HTTPS访问
- 浏览器需要麦克风权限

### 4. Agent响应慢

**问题**: 首次响应时间过长

**解决**:
- 检查网络连接
- 增加服务器配置
- 启用模型缓存

---

## 📞 技术支持

如有问题，请提交Issue或联系开发者。

---

## 📄 许可证

MIT License
