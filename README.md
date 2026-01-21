# PDFToolsPro - 在线PDF转换工具

## 项目概述

这是一个现代化的在线PDF转换工具，支持PDF转换为Word/Excel/PPT。项目采用FastAPI后端 + HTML前端的一体化架构，部署简单快捷。

### 核心功能
- **PDF 转 Word** - 保持格式、提取图片、支持多页文档
- **PDF 转 Excel** - 提取表格数据，支持多页表格
- **PDF 转 PPT** - 每页PDF转换为PPT幻灯片
- **拖拽上传** - 现代化的文件上传体验
- **实时进度** - 上传、处理、下载状态展示
- **CPA变现** - 集成Content Locker实现下载锁定

## 技术栈

### 后端
- **FastAPI** - 现代化的 Python Web 框架
- **pdf2docx** - PDF 转 Word 核心库
- **pdfplumber + pandas** - PDF 转 Excel
- **python-pptx** - PDF 转 PPT
- **PyPDF2** - PDF 文件验证

### 前端
- **HTML5** - 单页应用
- **TailwindCSS** - 现代化UI框架（CDN）
- **原生JavaScript** - 无需构建工具

### 部署
- **Railway** - 一体化部署（推荐）
- 单平台部署，无需配置CORS

## 项目结构

```
alliance/
├── backend/                 # 后端服务 + 前端
│   ├── app/
│   │   ├── main.py         # 应用入口 + 静态文件服务
│   │   ├── api/
│   │   │   └── convert.py  # PDF转换接口（Word/Excel/PPT）
│   │   └── core/
│   │       └── pdf_converter.py
│   ├── static/
│   │   └── index.html      # 前端单页应用
│   └── requirements.txt    # Python依赖
│
├── landing-page/          # CPA账户审批用着陆页
│   ├── index.html
│   ├── privacy.html
│   └── terms.html
│
├── docs/                  # 项目文档
│   ├── deployment-guide.md          # 部署指南
│   ├── cpagrip-registration-guide.md
│   ├── keyword-research-guide.md
│   └── domain-purchase-guide.md
│
└── railway.toml           # Railway配置
```

## 快速开始

### 本地开发

```bash
# 1. 进入后端目录
cd backend

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动服务器
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

访问：
- 前端页面: http://localhost:8000
- API文档: http://localhost:8000/docs

### 部署到生产环境

详细步骤请参考 [部署指南](docs/deployment-guide.md)

**快速部署（只需Railway）：**

1. **推送到GitHub**
```bash
git add .
git commit -m "Ready for deployment"
git push
```

2. **部署到Railway**
- 访问 https://railway.app/
- 使用GitHub登录
- 选择 `PDFToolsPro` 仓库
- 设置 Root Directory 为 `backend`
- 点击 Deploy

完成！Railway会自动部署并分配URL。

## API 端点

### POST /api/convert/pdf-to-word
转换PDF为Word文档

**请求：**
- Content-Type: multipart/form-data
- Body: file (PDF文件, 最大10MB)

**响应：**
- Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document
- Body: Word文档二进制

### POST /api/convert/pdf-to-excel
转换PDF为Excel文档

**请求：**
- Content-Type: multipart/form-data
- Body: file (PDF文件, 最大10MB)

**响应：**
- Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
- Body: Excel文档二进制

### POST /api/convert/pdf-to-ppt
转换PDF为PowerPoint演示文稿

**请求：**
- Content-Type: multipart/form-data
- Body: file (PDF文件, 最大10MB)

**响应：**
- Content-Type: application/vnd.openxmlformats-officedocument.presentationml.presentation
- Body: PPT文档二进制

### POST /api/convert/validate-pdf
验证PDF文件（不转换）

### GET /health
健康检查端点

## 配置

### 前端配置

编辑 `backend/static/index.html` 中的 `CONFIG`：

```javascript
const CONFIG = {
    // API地址（自动检测环境）
    API_BASE_URL: '',  // 生产环境使用相对路径（同域名）

    // CPA配置
    CPA_LOCKER_ID: 'your_locker_id',
    ENABLE_CPA: false  // 设为true启用CPA锁定
};
```

### 环境变量（可选）

```env
# Railway环境变量
PYTHON_VERSION=3.10
PORT=8000
```

## 功能特性

### ✅ 已实现
- [x] PDF 转 Word 核心转换功能
- [x] PDF 转 Excel（表格提取）
- [x] PDF 转 PPT（每页转幻灯片）
- [x] 文件上传和验证
- [x] 拖拽上传UI
- [x] 实时进度状态
- [x] 错误处理和日志
- [x] API文档自动生成
- [x] 中文文件名支持
- [x] CPA Content Locker集成框架
- [x] 一体化部署配置

### 📋 后续扩展
- [ ] 批量转换
- [ ] OCR文字识别
- [ ] 文件压缩
- [ ] 更多输出格式

## 成本估算

### 免费额度

| 平台 | 免费额度 | 月费用 |
|------|----------|--------|
| Railway | $5/月 | $0 |
| GitHub | 私有仓库 | $0 |
| **总计** | - | **$0** |

### 付费计划（如需扩展）

- Railway: $5/月起（超出免费额度后）

## 变现策略

### CPA Content Locker
1. 注册CPAgrip账户
2. 创建Content Locker
3. 获取Locker ID
4. 在前端配置 `ENABLE_CPA: true`

详细指南参考 [CPAgrip注册指南](docs/cpagrip-registration-guide.md)

## 常见问题

### Q: 转换失败怎么办？
A: 检查Railway日志，常见原因：
- PDF文件损坏
- 文件加密（需要密码）
- 文件过大（限制10MB）

### Q: 如何增加文件大小限制？
A: 修改后端 `convert.py` 中的验证逻辑和前端配置

### Q: 支持哪些文件格式？
A:
- 输入：PDF
- 输出：Word (.docx), Excel (.xlsx), PowerPoint (.pptx)

## 许可证

MIT License

---

**当前状态**: 可部署
**最后更新**: 2026-01-21
**仓库**: https://github.com/xiaoshiling1234/PDFToolsPro
