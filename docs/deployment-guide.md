# 🚀 PDF转换工具 - 完整部署指南

本指南将帮助您将PDF转换工具部署到生产环境。

---

## 📋 部署前检查清单

在开始部署之前，请确保：

- [ ] Python 3.10+ 已安装
- [ ] Git 已安装
- [ ] GitHub 账号（或使用其他Git服务）
- [ ] Railway/Vercel 账号（或使用其他部署平台）
- [ ] CPAgrip 账户（可选，用于变现）

---

## 🎯 推荐部署方案

### 方案A: Railway + Vercel (最推荐) ⭐⭐⭐⭐⭐

**Railway** - 后端API服务
**Vercel** - 前端静态文件

**优点**：
- ✅ 完全免费起步
- ✅ 自动HTTPS
- ✅ GitHub集成
- ✅ 零配置部署

---

## 📦 方案A: Railway (后端) + Vercel (前端)

### 第1步: 准备代码仓库

```bash
# 初始化Git仓库（如果还没有）
cd C:\Users\ADMIN\PycharmProjects\alliance
git init

# 创建.gitignore
cat > .gitignore << 'EOF'
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST
.venv/
venv/
ENV/
env/
.ENV/
*.db
*.sqlite3
temp/
tmp/
*.log
.DS_Store
Thumbs.db
EOF

# 提交代码
git add .
git commit -m "Initial commit: PDF to Word converter"
```

### 第2步: 推送到GitHub

#### 方式1: 使用GitHub网页

1. 访问 https://github.com/new
2. 仓库名称：`pdf-converter-tool`
3. 设为私有仓库（推荐）
4. 不要初始化README
5. 点击"Create repository"

```bash
# 添加远程仓库
git remote add origin https://github.com/your-username/pdf-converter-tool.git

# 推送代码
git branch -M main
git push -u origin main
```

#### 方式2: 使用GitHub CLI (gh)

```bash
# 如果安装了gh CLI
gh repo create pdf-converter-tool --private --source=.
```

### 第3步: 部署后端到Railway

#### 方式1: 通过Railway网站部署

1. 访问 https://railway.app/
2. 点击"Sign Up"或"Login"
3. 使用GitHub账号登录
4. 点击"New Project" → "Deploy from GitHub repo"
5. 选择 `pdf-converter-tool` 仓库
6. Railway会自动检测到Python项目

7. **配置Root Directory**:
   - 在Railway项目设置中
   - 设置Root Directory为 `backend`
   - 因为我们只需要部署backend目录

8. **添加环境变量**（如果需要）:
   ```env
   PYTHON_VERSION=3.10
   PORT=8000
   ```

9. 点击"Deploy"
10. Railway会自动部署并分配一个URL: `https://your-app.up.railway.app`

#### 方式2: 使用Railway CLI (高级)

```bash
# 安装Railway CLI
npm install -g @railway/cli

# 登录
railway login

# 初始化项目
railway init

# 部署
railway up
```

### 第4步: 更新前端配置

部署后端后，Railway会提供一个URL，例如：
```
https://pdf-converter-production.up.railway.app
```

需要更新前端代码中的API_BASE_URL。

**选项1: 动态配置（推荐）**

前端已经配置为自动检测环境：
```javascript
API_BASE_URL: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:8000'  // 开发环境
    : ''  // 生产环境 - 使用相对路径
```

**选项2: 硬编码生产URL**

更新 `frontend/index.html`:
```javascript
API_BASE_URL: window.location.hostname === 'localhost'
    ? 'http://localhost:8000'
    : 'https://pdf-converter-production.up.railway.app'  // 替换为你的Railway URL
```

提交更新：
```bash
git add frontend/index.html
git commit -m "Update API URL for production"
git push
```

### 第5步: 部署前端到Vercel

1. 访问 https://vercel.com/
2. 使用GitHub账号登录
3. 点击"New Project"
4. 导入GitHub仓库：`pdf-converter-tool`
5. **配置项目设置**:
   - Framework Preset: "Other"
   - Root Directory: `frontend`
   - Build Command: (留空)
   - Output Directory: (留空)

6. 点击"Deploy"

7. Vercel会部署并提供一个URL: `https://pdf-converter-tool.vercel.app`

### 第6步: 配置自定义域名（可选）

#### Vercel配置自定义域名

1. 在Vercel项目设置中点击"Domains"
2. 添加您的域名（例如：`pdfconverterpro.com`）
3. Vercel会显示DNS记录
4. 在域名注册商（Namecheap/GoDaddy）添加以下记录：

```
类型: A
名称: @
值: 76.76.21.21

类型: CNAME
名称: www
值: cname.vercel-dns.com
```

#### Railway配置自定义域名（可选）

如果需要后端独立域名：
1. 在Railway项目设置中点击"Domains"
2. 添加域名并配置DNS

### 第7步: 测试部署

1. **测试前端**:
   - 访问您的Vercel URL
   - 上传一个测试PDF文件
   - 检查是否成功转换

2. **测试API**:
   - 访问 `https://your-railway-url.railway.app/docs`
   - 测试API文档中的端点

3. **检查CORS**:
   - 如果遇到CORS错误，检查Railway的后端CORS配置

---

## 🔧 故障排除

### 问题1: 后端部署失败

**症状**: Railway部署失败

**解决方案**:
```bash
# 检查requirements.txt是否包含所有依赖
cat backend/requirements.txt

# 确保包含python-multipart
# 确保pdf2docx等库都在列表中
```

### 问题2: CORS错误

**症状**: 前端无法连接到后端API

**解决方案**:

在Railway项目的环境变量中添加：
```
ALLOWED_ORIGINS=https://your-vercel-url.vercel.app,https://your-custom-domain.com
```

然后更新 `backend/app/main.py`:
```python
import os

allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 问题3: 文件大小限制

**症状**: 大文件上传失败

**解决方案**:

Railway默认限制为25MB。如果需要支持更大的文件：

1. 修改 `frontend/index.html` 中的限制
2. 修改 `backend/app/api/convert.py` 中的验证
3. 添加到Railway环境变量：`MAX_FILE_SIZE=10485760` (10MB)

### 问题4: PDF转换失败

**症状**: 转换时返回500错误

**解决方案**:

1. 检查Railway日志:
   - 在Railway项目中点击"Logs"
   - 查看错误信息

2. 常见问题:
   - 缺少依赖: 确保 `pdf2docx` 在 requirements.txt 中
   - 文件损坏: 确保上传的PDF文件有效

---

## 📊 监控和分析

### 查看日志

**Railway**:
- 项目 → Logs → 实时日志

**Vercel**:
- 项目 → Deployments → 点击部署 → Logs

### 添加Google Analytics

在 `frontend/index.html` 的 `<head>` 中添加：

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

---

## 🔒 安全建议

### 生产环境必做:

1. **限制CORS origins**:
   ```python
   allow_origins=["https://yourdomain.com"]
   ```

2. **添加速率限制** (使用slowapi):
   ```bash
   pip install slowapi
   ```

3. **验证文件内容**:
   - 检查文件大小
   - 检查文件类型
   - 扫描恶意内容

4. **使用HTTPS**:
   - Railway和Vercel都自动提供

5. **定期更新依赖**:
   ```bash
   pip install --upgrade pip
   pip install --upgrade -r requirements.txt
   ```

---

## 💰 激活CPA变现

### 步骤1: 获取CPAgrip Content Locker ID

1. 登录 CPAgrip: https://www.cpagrip.com/
2. 进入 "Monetize" → "Content Lockers"
3. 点击 "Create Content Locker"
4. 配置:
   - 名称: PDF Converter Download
   - 锁定类型: File Download
   - 允许的国家: US, UK, CA, AU (高价值)
   - 移动端优化: 启用
5. 创建后，复制Locker ID

### 步骤2: 集成到前端

更新 `frontend/index.html`:
```javascript
const CONFIG = {
    API_BASE_URL: '...',
    CPA_LOCKER_ID: '12345', // 替换为实际的Locker ID
    ENABLE_CPA: true // 设置为true
};
```

### 步骤3: 提交并部署

```bash
git add frontend/index.html
git commit -m "Enable CPA monetization"
git push
```

Vercel会自动重新部署。

---

## 📈 成本估算

### 免费额度

| 平台 | 免费额度 | 月费用 |
|------|----------|--------|
| Railway | $5/月 | $0 |
| Vercel | 无限 | $0 |
| GitHub | 私有仓库 | $0 |
| **总计** | - | **$0** |

### 付费计划（如果需要扩展）

**Railway** (超出免费额度后):
- $5/月起
- 更多资源: $20-$50/月

**Vercel** (Pro计划):
- $20/月
- 更多带宽、分析

---

## ✅ 部署成功检查清单

部署完成后，检查以下项目：

- [ ] 前端可访问
- [ ] 后端API可访问
- [ ] 可以成功上传PDF
- [ ] 转换功能正常工作
- [ ] 下载功能正常
- [ ] HTTPS正常（小锁图标）
- [ ] 移动端显示正常
- [ ] Google Analytics已安装
- [ ] 隐私政策页面可访问
- [ ] 服务条款页面可访问
- [ ] CPA locker已集成（可选）

---

## 🎉 完成！

您的PDF转换工具现在已经上线！

**下一步**:
1. 在社交媒体分享
2. 提交到工具目录站
3. 创建SEO内容
4. 监控分析数据
5. 根据数据优化

---

## 📞 需要帮助？

如果遇到问题：

- **Railway支持**: https://railway.app/contact
- **Vercel支持**: support@vercel.com
- **文档**: [项目README](../README.md)

---

**最后更新**: 2026-01-20
**状态**: 准备就绪
