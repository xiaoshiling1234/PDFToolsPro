#!/usr/bin/env python3
"""
Google Trends API 查询脚本
用于SEO关键词研究，支持代理配置
"""

import pytrends
from pytrends.request import TrendReq
import json
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Optional


class GoogleTrendsQuery:
    """Google Trends查询类"""

    def __init__(self, proxy: str = "http://localhost:7890", timeout: tuple = (10, 25)):
        """
        初始化Google Trends连接

        Args:
            proxy: 代理地址，默认localhost:7890
            timeout: 超时设置(连接超时, 读取超时)
        """
        # pytrends需要列表格式或None
        proxies_list = [proxy] if proxy else None

        self.pytrends = TrendReq(
            proxies=proxies_list,
            retries=2,
            backoff_factor=0.1,
            timeout=timeout
        )

    def get_interest_over_time(self, keyword: str, timeframe: str = "today 12-m") -> Dict:
        """
        获取关键词随时间变化的搜索兴趣

        Args:
            keyword: 关键词
            timeframe: 时间范围
                - "today 12-m": 过去12个月
                - "today 3-m": 过去3个月
                - "today 1-m": 过去1个月
                - "today 5-y": 过去5年

        Returns:
            包含时间序列数据的字典
        """
        try:
            self.pytrends.build_payload([keyword], timeframe=timeframe)
            data = self.pytrends.interest_over_time()

            if data.empty:
                return {"error": "No data found for this keyword"}

            # 重置索引，将日期转换为字符串
            data = data.reset_index()
            data['date'] = data['date'].dt.strftime('%Y-%m-%d')

            return {
                "keyword": keyword,
                "timeframe": timeframe,
                "data": data.to_dict(orient='records'),
                "max_interest": int(data[keyword].max()),
                "avg_interest": round(data[keyword].mean(), 2),
                "trend": "rising" if data[keyword].iloc[-5:].mean() > data[keyword].iloc[:5].mean() else "declining"
            }
        except Exception as e:
            return {"error": str(e)}

    def get_related_topics(self, keyword: str) -> Dict:
        """
        获取相关主题（rising和top）

        Args:
            keyword: 关键词

        Returns:
            相关主题数据
        """
        try:
            self.pytrends.build_payload([keyword])
            rising = self.pytrends.related_topics()[keyword]['rising']
            top = self.pytrends.related_topics()[keyword]['top']

            return {
                "keyword": keyword,
                "rising_topics": rising.head(10).to_dict(orient='records') if rising is not None else [],
                "top_topics": top.head(10).to_dict(orient='records') if top is not None else []
            }
        except Exception as e:
            return {"error": str(e)}

    def get_related_queries(self, keyword: str) -> Dict:
        """
        获取相关查询（rising和top）

        Args:
            keyword: 关键词

        Returns:
            相关查询数据
        """
        try:
            self.pytrends.build_payload([keyword])
            rising = self.pytrends.related_queries()[keyword]['rising']
            top = self.pytrends.related_queries()[keyword]['top']

            return {
                "keyword": keyword,
                "rising_queries": rising.head(20).to_dict(orient='records') if rising is not None else [],
                "top_queries": top.head(20).to_dict(orient='records') if top is not None else []
            }
        except Exception as e:
            return {"error": str(e)}

    def compare_keywords(self, keywords: List[str], timeframe: str = "today 12-m") -> Dict:
        """
        比较多个关键词的搜索趋势

        Args:
            keywords: 关键词列表（最多5个）
            timeframe: 时间范围

        Returns:
            比较结果
        """
        if len(keywords) > 5:
            return {"error": "Maximum 5 keywords allowed for comparison"}

        try:
            self.pytrends.build_payload(keywords, timeframe=timeframe)
            data = self.pytrends.interest_over_time()

            if data.empty:
                return {"error": "No data found"}

            data = data.reset_index()
            data['date'] = data['date'].dt.strftime('%Y-%m-%d')

            # 计算每个关键词的平均搜索量
            avg_interests = {}
            for kw in keywords:
                if kw in data.columns:
                    avg_interests[kw] = round(data[kw].mean(), 2)

            return {
                "keywords": keywords,
                "timeframe": timeframe,
                "data": data.to_dict(orient='records'),
                "avg_interests": avg_interests,
                "winner": max(avg_interests, key=avg_interests.get)
            }
        except Exception as e:
            return {"error": str(e)}

    def get_regional_interest(self, keyword: str, geo: str = "") -> Dict:
        """
        获取关键词在不同地区的搜索热度

        Args:
            keyword: 关键词
            geo: 地区代码（空=全球, "US"=美国, "CN"=中国等）

        Returns:
            地区热度数据
        """
        try:
            self.pytrends.build_payload([keyword], geo=geo)
            data = self.pytrends.interest_by_region(resolution='COUNTRY')

            if data.empty:
                return {"error": "No regional data found"}

            return {
                "keyword": keyword,
                "region": geo if geo else "Global",
                "top_regions": data.head(20).to_dict()
            }
        except Exception as e:
            return {"error": str(e)}

    def get_suggestions(self, keyword: str) -> Dict:
        """
        获取关键词建议（自动补全）

        Args:
            keyword: 关键词

        Returns:
            建议的关键词列表
        """
        try:
            suggestions = self.pytrends.suggestions(keyword)

            return {
                "keyword": keyword,
                "suggestions": [
                    {
                        "term": s['title'],
                        "type": s['type'],
                        "mid": s['mid']
                    }
                    for s in suggestions
                ]
            }
        except Exception as e:
            return {"error": str(e)}

    def analyze_keyword_for_seo(self, keyword: str) -> Dict:
        """
        综合SEO分析一个关键词

        Args:
            keyword: 关键词

        Returns:
            完整的SEO分析报告
        """
        print(f"Analyzing keyword: {keyword}...", file=sys.stderr)

        result = {"keyword": keyword, "analysis": {}}

        # 1. 时间趋势
        print("  - Getting interest over time...", file=sys.stderr)
        result["analysis"]["interest_over_time"] = self.get_interest_over_time(keyword)

        # 2. 相关查询（最重要的SEO信息）
        print("  - Getting related queries...", file=sys.stderr)
        result["analysis"]["related_queries"] = self.get_related_queries(keyword)

        # 3. 相关主题
        print("  - Getting related topics...", file=sys.stderr)
        result["analysis"]["related_topics"] = self.get_related_topics(keyword)

        # 4. 关键词建议
        print("  - Getting keyword suggestions...", file=sys.stderr)
        result["analysis"]["suggestions"] = self.get_suggestions(keyword)

        # 5. 地区分布
        print("  - Getting regional interest...", file=sys.stderr)
        result["analysis"]["regional"] = self.get_regional_interest(keyword)

        # SEO建议
        result["seo_recommendations"] = self._generate_seo_recommendations(result)

        return result

    def _generate_seo_recommendations(self, analysis: Dict) -> Dict:
        """生成SEO建议"""
        recommendations = {
            "keyword_opportunities": [],
            "content_ideas": [],
            "target_regions": []
        }

        # 从rising queries中提取机会
        if "related_queries" in analysis["analysis"]:
            rq = analysis["analysis"]["related_queries"]
            if "rising_queries" in rq and rq["rising_queries"]:
                recommendations["keyword_opportunities"] = [
                    q['query'] for q in rq["rising_queries"][:5]
                ]

            if "top_queries" in rq and rq["top_queries"]:
                recommendations["content_ideas"] = [
                    q['query'] for q in rq["top_queries"][:10]
                ]

        # 从地区数据中提取目标市场
        if "regional" in analysis["analysis"]:
            reg = analysis["analysis"]["regional"]
            if "top_regions" in reg and not reg.get("error"):
                recommendations["target_regions"] = list(reg["top_regions"].keys())[:5]

        return recommendations


def main():
    """命令行接口"""
    import argparse

    parser = argparse.ArgumentParser(description="Google Trends SEO Research Tool")
    parser.add_argument("keyword", help="Keyword to analyze")
    parser.add_argument("--compare", nargs="+", help="Additional keywords to compare")
    parser.add_argument("--timeframe", default="today 12-m",
                       help="Timeframe (today 12-m, today 3-m, today 1-m)")
    parser.add_argument("--proxy", default="http://localhost:7890",
                       help="Proxy address (default: localhost:7890)")
    parser.add_argument("--output", help="Output JSON file path")

    args = parser.parse_args()

    # 初始化查询器
    qt = GoogleTrendsQuery(proxy=args.proxy)

    if args.compare:
        # 比较模式
        keywords = [args.keyword] + args.compare
        result = qt.compare_keywords(keywords, args.timeframe)
    else:
        # 完整分析模式
        result = qt.analyze_keyword_for_seo(args.keyword)

    # 输出结果
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"Results saved to {args.output}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()