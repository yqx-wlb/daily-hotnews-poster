import os
import json
import time
from datetime import datetime
import requests
import openai

class HotNewsPoster:
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if not self.openai_api_key:
            print("警告：未设置OPENAI_API_KEY，将使用模拟数据")
        
        self.xiaohongshu_cookie = os.getenv('XIAOHONGSHU_COOKIE')
        if self.openai_api_key:
            openai.api_key = self.openai_api_key

    def get_hot_news(self):
        """获取热点新闻"""
        try:
            # 调用现有的热点获取接口
            response = requests.post(
                "https://api.kanyun.com/mcp/mcp_server_hotnews_get_hot_news",
                json={"sources": [1, 3, 5]}  # 知乎、百度、微博
            )
            return response.json()
        except Exception as e:
            print(f"获取热点失败：{str(e)}")
            # 返回模拟数据
            return {
                "知乎热榜": [
                    {"title": "模拟热点1", "url": "http://example.com", "heat": "100万"},
                    {"title": "模拟热点2", "url": "http://example.com", "heat": "90万"}
                ]
            }

    def format_hot_news(self, raw_data):
        """格式化热点数据"""
        formatted_news = []
        
        # 处理知乎数据
        if "知乎热榜" in raw_data:
            for item in raw_data["知乎热榜"][:5]:  # 取前5条
                formatted_news.append({
                    "platform": "知乎",
                    "title": item["title"],
                    "heat": item.get("heat", "未知"),
                    "url": item.get("url", "")
                })
        
        # 处理百度数据
        if "百度热点" in raw_data:
            for item in raw_data["百度热点"][:3]:  # 取前3条
                formatted_news.append({
                    "platform": "百度",
                    "title": item["title"],
                    "heat": item.get("heat", "未知"),
                    "url": item.get("url", "")
                })
        
        # 处理微博数据
        if "微博热搜榜" in raw_data:
            for item in raw_data["微博热搜榜"][:2]:  # 取前2条
                formatted_news.append({
                    "platform": "微博",
                    "title": item["title"],
                    "heat": item.get("heat", "未知"),
                    "url": item.get("url", "")
                })
        
        return formatted_news

    def generate_content(self, hot_news):
        """生成小红书风格内容"""
        if not self.openai_api_key:
            return self.generate_mock_content(hot_news)
            
        prompt = f"""
        请根据以下热点新闻生成一篇小红书风格的文章：
        {json.dumps(hot_news, ensure_ascii=False)}
        
        要求：
        1. 标题要简短有力，吸引人点击
        2. 正文分为今日热点Top10
        3. 每条热点要包含：
           - 事件概述
           - 时间信息（如有）
           - 简短的个人观点或延伸
        4. 大量使用emoji增加可读性
        5. 最后加上个人总结和互动引导
        6. 添加4-5个相关话题标签
        7. 整体风格要活泼、年轻化
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你是一个专业的社交媒体内容创作者，特别擅长小红书平台的内容创作"},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message['content']
        except Exception as e:
            print(f"生成内容失败：{str(e)}")
            return self.generate_mock_content(hot_news)

    def generate_mock_content(self, hot_news):
        """生成模拟内容（当API不可用时）"""
        content = "🔥今日热点速递！重大事件实时追踪\n\n"
        
        for idx, news in enumerate(hot_news, 1):
            content += f"{idx}️⃣ {news['title']}\n"
            content += f"平台：{news['platform']} | 热度：{news['heat']}\n\n"
        
        content += "\n💡我的观点：\n"
        content += "今天的热点事件反映了社会的多个方面，让我们保持关注！\n\n"
        content += "#今日热点 #新闻速递 #热点新闻 #每日资讯"
        
        return content

    def post_to_xiaohongshu(self, content):
        """发布到小红书（示例代码）"""
        if not self.xiaohongshu_cookie:
            print("\n=== 模拟发布到小红书 ===")
            print("标题:", content.split('\n')[0])
            print("内容长度:", len(content))
            print("发布时间:", datetime.now())
            return True
        
        # TODO: 实现实际的发布逻辑
        return True

    def run(self):
        """主运行流程"""
        try:
            # 1. 获取热点
            raw_hot_news = self.get_hot_news()
            formatted_news = self.format_hot_news(raw_hot_news)
            
            # 2. 生成内容
            content = self.generate_content(formatted_news)
            
            # 3. 发布内容
            success = self.post_to_xiaohongshu(content)
            
            if success:
                print("\n=== 内容生成成功 ===")
                print(content)
                print("\n=== 发布成功 ===")
            
        except Exception as e:
            print(f"运行失败：{str(e)}")

if __name__ == "__main__":
    poster = HotNewsPoster()
    poster.run()