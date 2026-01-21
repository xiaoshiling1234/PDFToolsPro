# 着陆页部署指南

这个着陆页可以立即部署到免费的托管服务，用于CPA账户审核和初期展示。

## 📁 文件说明

- `index.html` - 主页（工具介绍和导航）
- `privacy.html` - 隐私政策页面（CPA审核必需）
- `terms.html` - 服务条款页面（CPA审核必需）

---

## 🚀 快速部署方法

### 方法1: Vercel（最推荐）⭐⭐⭐⭐⭐

**步骤**：
1. 访问 https://vercel.com/
2. 使用GitHub账号登录
3. 点击 "New Project"
4. 如果您有GitHub仓库，导入项目
5. 或选择 "Upload" 上传这些文件
6. 点击 "Deploy"
7. 等待部署完成（约1分钟）
8. 获得免费域名：`your-project.vercel.app`

**优点**：
- ✅ 完全免费
- ✅ 自动SSL证书
- ✅ 全球CDN
- ✅ 自定义域名支持
- ✅ 部署极快

---

### 方法2: Netlify ⭐⭐⭐⭐⭐

**步骤**：
1. 访问 https://www.netlify.com/
2. 注册账号
3. 将这3个文件拖拽到部署区域
4. 或连接GitHub仓库
5. 点击 "Deploy Site"
6. 获得免费域名：`your-site.netlify.app`

**优点**：
- ✅ 完全免费
- ✅ 拖拽部署（最简单）
- ✅ 自动SSL
- ✅ 表单处理（免费）

---

### 方法3: GitHub Pages ⭐⭐⭐⭐

**步骤**：
1. 创建GitHub仓库
2. 上传文件到仓库
3. 进入仓库 Settings → Pages
4. Source选择 "Deploy from a branch"
5. Branch选择 "main" 或 "master"
6. 点击 Save
7. 几分钟后访问：`https://your-username.github.io/your-repo/`

**优点**：
- ✅ 完全免费
- ✅ GitHub集成
- ✅ 版本控制

---

### 方法4: Cloudflare Pages ⭐⭐⭐⭐⭐

**步骤**：
1. 访问 https://pages.cloudflare.com/
2. 登录Cloudflare账号
3. 点击 "Create a project"
4. 连接GitHub或上传文件
5. 点击 "Save and Deploy"
6. 获得域名：`your-project.pages.dev`

**优点**：
- ✅ 完全免费
- ✅ 全球CDN最快
- ✅ 无限制带宽
- ✅ 自动部署

---

## 🎯 推荐方案对比

| 平台 | 难度 | 速度 | 域名形式 | 推荐度 |
|------|------|------|----------|--------|
| **Vercel** | ⭐⭐ | 极快 | `vercel.app` | ⭐⭐⭐⭐⭐ |
| **Netlify** | ⭐ | 极快 | `netlify.app` | ⭐⭐⭐⭐⭐ |
| **GitHub Pages** | ⭐⭐⭐ | 快 | `github.io` | ⭐⭐⭐⭐ |
| **Cloudflare Pages** | ⭐⭐ | 极快 | `pages.dev` | ⭐⭐⭐⭐⭐ |

**我的推荐**：Vercel 或 Netlify（最简单）

---

## 🔗 自定义域名配置

部署后，您可以绑定自己的域名（需要在域名注册商配置DNS）：

### Vercel配置：
1. 在Vercel项目设置中点击 "Domains"
2. 添加您的域名（如：pdfconverterpro.com）
3. Vercel会显示DNS记录
4. 在Namecheap/GoDaddy添加这些记录：
   ```
   类型: A记录
   名称: @
   值: 76.76.21.21

   类型: CNAME
   名称: www
   值: cname.vercel-dns.com
   ```

### Netlify配置：
1. 在Netlify项目设置中点击 "Domain management"
2. 点击 "Add custom domain"
3. 输入您的域名
4. Netlify会显示DNS配置
5. 在域名注册商添加DNS记录

---

## ✅ 部署检查清单

部署完成后，检查以下内容：

- [ ] 主页可以正常访问
- [ ] 所有链接正常工作（导航、按钮）
- [ ] 隐私政策页面可访问
- [ ] 服务条款页面可访问
- [ ] 移动端显示正常
- [ ] 页面加载速度快（<3秒）
- [ ] SSL证书正常（小锁图标）

---

## 📝 CPA账户审核用信息

**在CPA申请中填写**：

```
Website: [您的Vercel/Netlify域名]
       例如: https://pdf-tools-pro.vercel.app

Description:
"I run a free online PDF converter tools website.
Users can convert PDF to Word, Excel, and PowerPoint
files completely free with no registration required.

My tools are secure (SSL encrypted), fast, and work
on all devices including mobile. All files are
automatically deleted within 1 hour to protect privacy.

I plan to drive traffic through SEO and content marketing,
focusing on long-tail keywords like 'pdf to word converter free'

The website is currently live and functional at:
[您的域名]"
```

---

## 🎨 自定义品牌

### 更改网站名称：

在所有3个HTML文件中，将以下内容替换为您的品牌名：

1. `PDFToolsPro` → 您的品牌名
2. `support@pdftoolspro.com` → 您的邮箱
3. `https://pdftoolspro.com` → 您的域名

### 更改颜色：

在 `<style>` 标签中，可以自定义颜色：

```css
/* 主色调（紫色） */
.color-purple-600 → 改为您的颜色

/* 渐变背景 */
.gradient-bg → 修改渐变色

/* 按钮颜色 */
bg-purple-600 → 改为您的按钮颜色
```

---

## 📊 下一步

着陆页部署完成后：

1. [ ] 将URL添加到CPA申请中
2. [ ] 开始开发第一个转换工具
3. [ ] 工具开发完成后，集成到着陆页
4. [ ] 开始SEO优化和内容营销

---

**快速开始**：选择Vercel或Netlify，5分钟内即可完成部署！

---

**最后更新**: 2026-01-20
**状态**: 准备就绪
