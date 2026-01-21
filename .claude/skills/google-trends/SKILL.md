---
name: google-trends
description: Google Trends API集成工具，用于SEO关键词研究和市场趋势分析。提供关键词搜索量查询、相关话题发现、竞争词对比、地区热度分析等功能。使用场景：(1)分析单个关键词的搜索趋势和热度变化，(2)挖掘相关长尾关键词和热门话题，(3)对比多个关键词的市场需求，(4)分析关键词在不同地区的表现，(5)为联盟营销/内容创作/SEO优化提供数据支持。注意：需要代理(localhost:7890)访问Google服务。
---

# Google Trends 关键词研究工具

通过Python脚本调用Google Trends API进行关键词研究，适用于SEO优化、联盟营销、内容创作等场景。

## 快速开始

### 安装依赖

```bash
pip install -r scripts/requirements.txt
```

### 基本用法

**单个关键词完整分析**（最常用）：
```bash
python scripts/trends_query.py "pdf to word"
```

**比较多个关键词**：
```bash
python scripts/trends_query.py "pdf converter" --compare "pdf to word" "pdf editor"
```

**自定义时间范围**：
```bash
python scripts/trends_query.py "chatgpt" --timeframe "today 3-m"
```

**保存结果到文件**：
```bash
python scripts/trends_query.py "ai tools" --output results.json
```

## 核心功能

### 1. 关键词趋势分析

获取关键词过去12个月的搜索兴趣变化：

```python
from scripts.trends_query import GoogleTrendsQuery

qt = GoogleTrendsQuery()
result = qt.get_interest_over_time("pdf to word", timeframe="today 12-m")
```

返回数据包括：
- `max_interest`: 峰值搜索量（0-100）
- `avg_interest`: 平均搜索量
- `trend`: 趋势判断（rising/declining）
- `data`: 每日/每周的详细数据

### 2. 相关关键词挖掘（SEO核心功能）

找出长尾关键词和用户搜索意图：

```python
result = qt.get_related_queries("pdf converter")
# rising_queries: 上升趋势的关键词（机会词）
# top_queries: 热门相关搜索（竞争词）
```

**SEO价值**：
- `rising_queries`: 新兴关键词，竞争小，机会大
- `top_queries`: 稳定需求词，需评估竞争程度

### 3. 关键词对比分析

对比多个关键词的市场需求：

```python
result = qt.compare_keywords(["pdf to word", "pdf to excel", "pdf to ppt"])
# 返回每个关键词的平均搜索量，选出winner
```

用于工具矩阵优先级排序。

### 4. 地区热度分析

了解关键词在不同国家的表现：

```python
result = qt.get_regional_interest("chatgpt", geo="")  # 空字符串=全球
result = qt.get_regional_interest("chatgpt", geo="US")  # 美国
```

高热度地区=高CPA单价市场（美国/英国/加拿大/澳大利亚）

### 5. 综合SEO分析（一键全功能）

```python
result = qt.analyze_keyword_for_seo("pdf to word")
```

返回完整的SEO报告，包括：
- 时间趋势
- 相关查询（rising + top）
- 相关主题
- 关键词建议
- 地区分布
- **SEO建议**（自动生成的机会词列表）

## 常见使用场景

### 场景1: 为新工具选关键词

```bash
python scripts/trends_query.py "pdf to word"
```

查看输出中的：
1. `avg_interest`: 平均搜索量（>50为高需求）
2. `rising_queries`: 找长尾变体（如"convert pdf to word free"）
3. `seo_recommendations.keyword_opportunities`: 新兴机会词

### 场景2: 工具矩阵优先级排序

```bash
python scripts/trends_query.py "pdf to word" --compare "pdf to excel" "pdf to ppt" "pdf merger"
```

对比后选择需求量最高的先开发。

### 场景3: 挖掘长尾内容主题

```bash
python scripts/trends_query.py "pdf editor" | jq ".analysis.related_queries.top_queries"
```

用这些查询作为博客文章标题。

### 场景4: 评估目标市场

```bash
python scripts/trends_query.py "pdf converter" | jq ".analysis.regional.top_regions"
```

优先针对美国、英国、加拿大等高CPA单价国家。

## 时间范围选项

| 参数 | 说明 | 用途 |
|------|------|------|
| `today 12-m` | 过去12个月 | 默认，查看年度趋势 |
| `today 3-m` | 过去3个月 | 近期热点 |
| `today 1-m` | 过去1个月 | 最新趋势 |
| `today 5-y` | 过去5年 | 长期趋势分析 |

## 代理配置

脚本默认使用 `http://localhost:7890` 代理。如果使用其他代理：

```bash
python scripts/trends_query.py "keyword" --proxy http://127.0.0.1:7890
```

或修改脚本中的默认值：
```python
qt = GoogleTrendsQuery(proxy="http://your-proxy:port")
```

## 输出数据结构

### 完整分析输出

```json
{
  "keyword": "pdf to word",
  "analysis": {
    "interest_over_time": {
      "max_interest": 100,
      "avg_interest": 68.5,
      "trend": "rising"
    },
    "related_queries": {
      "rising_queries": [
        {"query": "convert pdf to word free online", "value": 450}
      ],
      "top_queries": [
        {"query": "pdf to word converter", "value": 100}
      ]
    },
    "seo_recommendations": {
      "keyword_opportunities": ["新兴关键词1", "新兴关键词2"],
      "content_ideas": ["内容主题1", "内容主题2"],
      "target_regions": ["US", "UK", "CA"]
    }
  }
}
```

## SEO决策框架

使用本工具的数据进行决策：

### 1. 关键词选择标准

✅ **优先开发**：
- `avg_interest` > 50
- `trend` = "rising"
- 有大量 `rising_queries`

⚠️ **谨慎进入**：
- `avg_interest` < 30
- `trend` = "declining"
- `top_queries` 被大品牌垄断

### 2. 内容创作策略

从 `top_queries` 中提取：
- "How to" 查询 → 教程文章
- "vs" 查询 → 对比文章
- "best" 查询 → 评测文章
- "free" 查询 → 工具页面

### 3. 工具矩阵扩展

运行对比分析后，按需求量排序：
1. 先开发 `winner` 关键词对应的工具
2. 用 `rising_queries` 找下一个工具方向
3. 用 `suggestions` 发现相邻领域

## 故障排除

**错误：Connection timeout**
- 检查代理是否运行：`curl http://localhost:7890`
- 确认代理能访问Google

**错误：No data found**
- 关键词可能是品牌词，改用通用词
- 尝试调整 `timeframe` 参数

**错误：Too many requests**
- Google限制请求频率
- 等待1-2分钟后重试

## 高级用法示例

### 批量关键词分析

```bash
# 创建关键词列表
cat keywords.txt
pdf to word
pdf to excel
pdf merger
image compressor

# 批量分析
for kw in $(cat keywords.txt); do
    python scripts/trends_query.py "$kw" --output "results/${kw// /_}.json"
done
```

### 提取Rising Queries用于内容

```bash
python scripts/trends_query.py "your keyword" | \
jq -r '.analysis.related_queries.rising_queries[].query' > \
content_ideas.txt
```

### 与联盟营销结合

1. 分析目标关键词 → 找高需求低竞争词
2. 查看 `top_regions` → 确定目标市场
3. 用 `suggestions` → 发现相关工具机会
4. 开发工具 → 集成CPA offer → 获得收益

## 相关资源

- Google Trends官网：https://trends.google.com/
- pytrends文档：https://github.com/pat310/google-trends-api
- SEO关键词研究指南：见联盟营销设计文档