# 阿里云服务器部署指南

## 📋 服务器信息

| 配置项 | 信息 |
|--------|------|
| **公网IP** | `62.234.185.67` |
| **用户名** | `ubuntu` |
| **密码** | `M!^6WZtYj~5g$+4[` |
| **系统** | Ubuntu 22.04 LTS |

---

## 🚀 部署步骤

### 第一阶段：连接服务器

#### Windows 用户
1. 按 `Win + R`，输入 `cmd`，回车
2. 在命令行中输入：
```bash
ssh ubuntu@62.234.185.67
```

#### Mac/Linux 用户
1. 打开「终端」
2. 输入：
```bash
ssh ubuntu@62.234.185.67
```

#### 输入密码
当提示 `password:` 时，输入：`M!^6WZtYj~5g$+4[`
（输入时屏幕不会显示字符，正常现象，输入完按回车）

---

### 第二阶段：服务器初始化

连接成功后，依次执行以下命令：

```bash
# 1. 更新系统包
sudo apt update && sudo apt upgrade -y

# 2. 安装Python和必要工具
sudo apt install -y python3.11 python3.11-venv python3-pip git nginx

# 3. 创建项目目录并克隆代码
cd ~
git clone https://github.com/wozhenful/test-agent.git
cd test-agent

# 4. 安装项目依赖
pip install uv
uv sync
```

---

### 第三阶段：配置防火墙

```bash
# 开放端口
sudo ufw allow 9000/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

---

### 第四阶段：测试运行

```bash
# 进入项目目录
cd ~/test-agent

# 测试运行
uv run python src/web_main.py
```

如果看到类似输出表示成功：
```
Uvicorn running on http://0.0.0.0:9000
```

按 `Ctrl + C` 停止测试。

---

### 第五阶段：配置后台运行

创建systemd服务，让程序在后台持续运行：

```bash
# 创建服务文件
sudo nano /etc/systemd/system/assessment-agent.service
```

复制以下内容粘贴进去：

```ini
[Unit]
Description=Assessment Agent Web Service
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/test-agent
ExecStart=/home/ubuntu/.local/bin/uv run python src/web_main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

按 `Ctrl + O` 保存，`Ctrl + X` 退出。

```bash
# 启用并启动服务
sudo systemctl daemon-reload
sudo systemctl enable assessment-agent
sudo systemctl start assessment-agent

# 检查服务状态
sudo systemctl status assessment-agent
```

---

### 第六阶段：配置Nginx反向代理（可选，用于HTTPS）

```bash
# 创建Nginx配置
sudo nano /etc/nginx/sites-available/assessment-agent
```

复制以下内容：

```nginx
server {
    listen 80;
    server_name 62.234.185.67;

    location / {
        proxy_pass http://127.0.0.1:9000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

```bash
# 启用配置
sudo ln -s /etc/nginx/sites-available/assessment-agent /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## ✅ 访问测试

部署完成后，访问：

```
http://62.234.185.67:9000
```

---

## 🔧 常用命令

```bash
# 查看服务状态
sudo systemctl status assessment-agent

# 重启服务
sudo systemctl restart assessment-agent

# 查看日志
sudo journalctl -u assessment-agent -f

# 停止服务
sudo systemctl stop assessment-agent

# 重新部署（更新代码后）
cd ~/test-agent
git pull
sudo systemctl restart assessment-agent
```

---

## 🆘 故障排查

### 1. 服务启动失败
```bash
# 查看详细错误
sudo journalctl -u assessment-agent -n 50
```

### 2. 端口被占用
```bash
# 查看端口占用
sudo lsof -i :9000

# 杀死进程
sudo kill -9 <PID>
```

### 3. 权限问题
```bash
# 修复权限
sudo chown -R ubuntu:ubuntu ~/test-agent
```

---

## 🌐 后续配置（可选）

### 配置域名访问
1. 购买域名（如阿里云、腾讯云）
2. 添加域名解析，指向 `62.234.185.67`
3. 配置SSL证书（Let's Encrypt免费）

### 配置HTTPS
```bash
# 安装Certbot
sudo apt install -y certbot python3-certbot-nginx

# 自动配置HTTPS
sudo certbot --nginx -d yourdomain.com
```

---

## 📞 需要帮助？

如果在部署过程中遇到任何问题，请：
1. 截图错误信息
2. 描述你执行到哪一步
3. 发给我，我会帮您解决！

---

**祝部署顺利！🎉**
