# 🚀 PDF转换工具 - 完整部署指南

本指南将帮助您将PDF转换工具部署到生产环境。

---

## 📋 部署前检查清单

在开始部署之前，请确保：

- [ ] Python 3.10+ 已安装
- [ ] Git 已安装
- [ ] GitHub 账号
- [ ] Railway 账号
- [ ] CPAgrip 账户（可选，用于变现）

---

## 🎯 部署方案：只用 Railway（最简单）⭐⭐⭐⭐⭐

**Railway** - 前端 + 后端一体化部署

**优点**：
- ✅ 只需要一个平台
- ✅ 完全免费起步（$5/月额度）
- ✅ 自动HTTPS
- ✅ GitHub集成
- ✅ 零配置部署
- ✅ 无CORS问题

---

## 📦 部署步骤

### 第1步: 推送代码到GitHub

如果已经推送到GitHub，可以跳过此步骤。

```bash
cd C:\Users\ADMIN\PycharmProjects\alliance

# 添加所有文件
git add .

# 提交
git commit -m "Ready for Railway deployment"

# 推送
git push origin main
```

### 第2步: 部署到Railway

#### 方式1: 通过Railway网站部署（推荐）

1. 访问 https://railway.app/
2. 点击"Sign Up"或"Login"
3. 使用GitHub账号登录
4. 点击"New Project" → "Deploy from GitHub repo"
5. 选择 `PDFToolsPro` 仓库
6. Railway会自动检测到Python项目

7. **配置Root Directory**:
   - 在Railway项目设置中
   - 设置Root Directory为 `backend`
   - 因为我们只需要部署backend目录（前端已放在backend/static中）

8. **环境变量**（可选）:
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

### 第3步: 验证部署

1. **访问应用**:
   - 访问您的Railway URL
   - 应该看到PDF转换工具界面

2. **测试转换**:
   - 上传一个测试PDF文件
   - 检查是否成功转换
   - 确认可以下载转换后的文件

3. **测试API文档**:
   - 访问 `https://your-app.up.railway.app/docs`
   - 查看Swagger文档

### 第4步: 配置自定义域名（可选）

1. 在Railway项目设置中点击"Domains"
2. 添加您的域名（例如：`pdfconverterpro.com`）
3. Railway会显示DNS记录
4. 在域名注册商（Namecheap/GoDaddy/阿里云）添加以下记录：

```
类型: CNAME
名称: @
值: your-app.up.railway.app

类型: CNAME
名称: www
值: your-app.up.railway.app
```

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

### 问题2: 文件大小限制

**症状**: 大文件上传失败

**解决方案**:

Railway默认限制为25MB。如果需要支持更大的文件：

1. 修改 `backend/static/index.html` 中的限制
2. 修改 `backend/app/api/convert.py` 中的验证
3. 添加到Railway环境变量：`MAX_FILE_SIZE=10485760` (10MB)

### 问题3: PDF转换失败

**症状**: 转换时返回500错误

**解决方案**:

1. 检查Railway日志:
   - 在Railway项目中点击"Logs"
   - 查看错误信息

2. 常见问题:
   - 缺少依赖: 确保 `pdf2docx` 在 requirements.txt 中
   - 文件损坏: 确保上传的PDF文件有效
   - 内存不足: Railway免费额度512MB RAM

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

更新 `backend/static/index.html`:
```javascript
const CONFIG = {
    API_BASE_URL: '', // 同域名，留空
    CPA_LOCKER_ID: '12345', // 替换为实际的Locker ID
    ENABLE_CPA: true // 设置为true
};
```

### 步骤3: 提交并部署

```bash
git add backend/static/index.html
git commit -m "Enable CPA monetization"
git push
```

Railway会自动重新部署。

---

## 📊 监控和分析

### 查看日志

**Railway**:
- 项目 → Logs → 实时日志

### 添加Google Analytics

在 `backend/static/index.html` 的 `<head>` 中添加：

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

1. **添加速率限制** (使用slowapi):
   ```bash
   pip install slowapi
   ```

2. **验证文件内容**:
   - 检查文件大小
   - 检查文件类型
   - 扫描恶意内容

3. **使用HTTPS**:
   - Railway自动提供

4. **定期更新依赖**:
   ```bash
   pip install --upgrade pip
   pip install --upgrade -r requirements.txt
   ```

---

## 📈 成本估算

### 免费额度

| 平台 | 免费额度 | 月费用 |
|------|----------|--------|
| Railway | $5/月 | $0 |
| GitHub | 私有仓库 | $0 |
| **总计** | - | **$0** |

### 付费计划（如果需要扩展）

**Railway** (超出免费额度后):
- $5/月起
- 更多资源: $20-$50/月

---

## ✅ 部署成功检查清单

部署完成后，检查以下项目：

- [ ] 应用可访问
- [ ] 可以成功上传PDF
- [ ] 转换功能正常工作
- [ ] 下载功能正常
- [ ] HTTPS正常（小锁图标）
- [ ] 移动端显示正常
- [ ] Google Analytics已安装
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
- **文档**: [项目README](../README.md)

---

**最后更新**: 2026-01-21
**状态**: 准备就绪
