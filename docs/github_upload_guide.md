# GitHub 上传指南

## 前提条件
1. 已安装 Git
2. 已注册 GitHub 账号
3. 已在本地配置 Git 用户名和邮箱

## 步骤 1：在 GitHub 上创建新仓库

### 方法 A：网页创建（推荐新手）

1. 登录 GitHub：https://github.com
2. 点击右上角 "+" → "New repository"
3. 填写信息：
   - **Repository name**: `assessment-agent`（或其他您喜欢的名称）
   - **Description**: `基于IRT自适应理论的智能测评智能体`
   - **Public/Private**: 选择 Public（公开）或 Private（私有）
   - ⚠️ **不要勾选** "Initialize this repository with a README"
4. 点击 "Create repository"
5. **复制仓库URL**（选择HTTPS或SSH）

### 方法 B：命令行创建

```bash
# 安装 GitHub CLI（可选）
# Ubuntu/Debian: sudo apt install gh
# Mac: brew install gh

# 登录 GitHub
gh auth login

# 创建仓库（交互式）
gh repo create assessment-agent --public --clone

# 或直接创建
gh repo create assessment-agent --public --source=. --push
```

## 步骤 2：添加远程仓库并推送

### 如果您使用网页创建的方法：

```bash
# 进入项目目录
cd /workspace/projects

# 添加远程仓库（将 <YOUR-USERNAME> 和 <REPO-NAME> 替换为您的信息）
git remote add origin https://github.com/<YOUR-USERNAME>/<REPO-NAME>.git

# 例如：
git remote add origin https://github.com/yourname/assessment-agent.git

# 推送代码到 GitHub
git push -u origin main
```

### 如果您遇到 "refusing to merge unrelated histories" 错误

```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

## 步骤 3：验证上传成功

1. 刷新 GitHub 仓库页面
2. 您应该能看到所有代码文件
3. 检查 README.md 是否正确显示

## 常见问题

### Q: 如何更新代码到 GitHub？

```bash
# 1. 添加或修改文件后
git add .

# 2. 提交更改
git commit -m "feat: 添加新功能"

# 3. 推送到 GitHub
git push
```

### Q: 如何保持 fork 的仓库与原仓库同步？

```bash
# 添加上游仓库
git remote add upstream https://github.com/original-owner/original-repo.git

# 获取上游更新
git fetch upstream

# 合并到主分支
git checkout main
git merge upstream/main

# 推送更新
git push
```

### Q: 如何查看 Git 状态？

```bash
# 查看状态
git status

# 查看提交历史
git log --oneline

# 查看远程仓库
git remote -v
```

### Q: 如何撤销更改？

```bash
# 撤销工作区的更改（未暂存）
git checkout -- <file>

# 撤销暂存（已 git add 但未 commit）
git reset HEAD <file>

# 撤销提交（未 push）
git reset --soft HEAD~1
```

## 推荐的 .gitignore 内容

已在项目中包含 `.gitignore`，排除了：
- Python 缓存文件 `__pycache__/`
- 虚拟环境 `venv/`
- IDE 配置 `.vscode/`
- 日志文件 `*.log`
- 环境变量文件 `.env`

## 权限设置

### 添加协作者（如果是私有仓库）
1. 进入仓库 Settings → Manage access
2. 点击 "Invite a collaborator"
3. 输入协作者的 GitHub 用户名或邮箱

### 创建组织（团队协作）
1. 点击右上角头像 → Your organizations
2. 点击 "New organization"
3. 选择合适的计划（Free/Team/Enterprise）
4. 创建后可创建团队并分配权限

## GitHub Pages 部署（可选）

如果您想为项目创建文档网站：

1. 进入仓库 Settings → Pages
2. Source: 选择 `main` 分支和 `/ (root)` 文件夹
3. 点击 Save
4. 等待几分钟，网站将发布在 `https://<username>.github.io/<repo-name>/`

## 备份建议

定期推送代码到 GitHub，确保代码安全：
```bash
# 养成好习惯：每天工作结束时
git add .
git commit -m "feat: 完成XX功能"
git push
```

---

如果遇到其他问题，请参考：
- GitHub 官方文档：https://docs.github.com
- Git 教程：https://git-scm.com/doc
