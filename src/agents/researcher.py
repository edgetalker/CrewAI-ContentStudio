"""
研究员智能体 - 负责信息收集和研究
"""
import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, Any, List

# 找到项目根目录并加载环境变量
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent  # 向上两级到项目根目录
env_path = project_root / '.env'

print(f"🔍 查找 .env 文件: {env_path}")
if env_path.exists():
    load_dotenv(env_path)
    print("✅ .env 文件加载成功")
else:
    print("⚠️  .env 文件未找到，尝试当前目录")
    load_dotenv()

# 现在才导入需要API key的模块
from crewai import Agent
from crewai_tools import SerperDevTool, WebsiteSearchTool

class ResearcherAgent:
    """研究员智能体 - 专门负责信息收集和验证"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._initialize_tools()

    def _initialize_tools(self):
        """初始化研究工具"""
        # 首先检查 OpenAI API Key
        openai_key = os.getenv("OPENAI_API_KEY")
        print(f"🔑 OpenAI API Key 状态: {'已设置' if openai_key else '未设置'}")

        if not openai_key:
            raise ValueError("❌ 未找到 OPENAI_API_KEY，请检查 .env 文件配置")

        try:
            # 检查是否有SERPER API KEY
            serper_key = os.getenv("SERPER_API_KEY")
            if serper_key:
                self.search_tool = SerperDevTool()
                self.logger.info("✅ SerperDevTool 初始化成功")
            else:
                self.search_tool = None
                self.logger.warning("⚠️  未找到SERPER_API_KEY，将使用基础搜索功能")

            # 网站搜索工具 - 需要 OpenAI API Key
            print("🔧 正在初始化 WebsiteSearchTool...")
            self.website_tool = WebsiteSearchTool()
            self.logger.info("✅ WebsiteSearchTool 初始化成功")

        except Exception as e:
            self.logger.error(f"❌ 工具初始化失败: {str(e)}")
            print(f"💡 调试信息: {str(e)}")
            raise

    def create_agent(self, config: Dict[str, Any]) -> Agent:
        """
        创建研究员智能体

        Args:
            config: 智能体配置字典

        Returns:
            Agent: 配置好的研究员智能体
        """
        try:
            # 准备工具列表
            tools = []
            if self.search_tool:
                tools.append(self.search_tool)
            tools.append(self.website_tool)

            # 创建Agent
            agent = Agent(
                role=config['role'],
                goal=config['goal'],
                backstory=config['backstory'],
                tools=tools,
                max_iter=config.get('max_iter', 3),
                max_execution_time=config.get('max_execution_time', 300),
                verbose=config.get('verbose', True),
                allow_delegation=config.get('allow_delegation', False),
                memory=True
            )

            self.logger.info("✅ 研究员智能体创建成功")
            return agent

        except Exception as e:
            self.logger.error(f"❌ 创建研究员智能体失败: {str(e)}")
            raise

    def validate_sources(self, sources: List[str]) -> List[Dict[str, Any]]:
        """
        验证信息源的可靠性

        Args:
            sources: 信息源URL列表

        Returns:
            List[Dict]: 验证后的源信息
        """
        validated_sources = []

        # 可信域名列表
        trusted_domains = [
            'gov.cn', 'edu.cn', 'org.cn', 'gov', 'edu', 'org',
            'ieee.org', 'nature.com', 'science.org',
            'cnki.net', 'wanfangdata.com.cn',
            'baidu.com', 'tencent.com', 'alibaba.com'
        ]

        for source in sources:
            try:
                # 基础URL验证
                if not source.startswith(('http://', 'https://')):
                    continue

                # 检查是否为可信域名
                is_trusted = any(domain in source.lower() for domain in trusted_domains)

                source_info = {
                    'url': source,
                    'is_trusted': is_trusted,
                    'domain': self._extract_domain(source),
                    'validation_score': self._calculate_trust_score(source)
                }

                validated_sources.append(source_info)

            except Exception as e:
                self.logger.warning(f"⚠️  源验证失败: {source}, 错误: {str(e)}")
                continue

        return validated_sources

    def _extract_domain(self, url: str) -> str:
        """提取域名"""
        try:
            from urllib.parse import urlparse
            return urlparse(url).netloc
        except:
            return "unknown"

    def _calculate_trust_score(self, url: str) -> float:
        """
        计算信任度评分 (0-1)
        """
        score = 0.5  # 基础分数

        # 政府和教育机构加分
        if any(domain in url.lower() for domain in ['.gov', '.edu', '.org']):
            score += 0.3

        # 知名媒体和平台加分
        if any(domain in url.lower() for domain in ['baidu', 'tencent', 'alibaba', 'xinhua', 'people']):
            score += 0.2

        # HTTPS加分
        if url.startswith('https://'):
            score += 0.1

        return min(score, 1.0)

    def extract_key_information(self, research_text: str) -> Dict[str, Any]:
        """
        从研究文本中提取关键信息

        Args:
            research_text: 研究文本

        Returns:
            Dict: 提取的关键信息
        """
        # 这里可以集成NLP工具进行更智能的信息提取
        # 暂时返回基础结构
        return {
            'word_count': len(research_text.split()),
            'key_topics': [],  # 可以添加关键词提取
            'data_points': [],  # 可以添加数据点识别
            'sources_count': research_text.count('http'),
            'last_updated': None
        }


# 用于单独测试的函数
def test_researcher_agent():
    """测试研究员智能体"""
    print("🔍 测试研究员智能体...")
    print(f"📁 当前工作目录: {os.getcwd()}")
    print(f"🔑 OPENAI_API_KEY: {'已设置' if os.getenv('OPENAI_API_KEY') else '未设置'}")

    try:
        # 模拟配置
        config = {
            'role': '内容研究专家',
            'goal': '收集关于AI发展的最新信息',
            'backstory': '你是一位经验丰富的研究专家',
            'max_iter': 2,
            'verbose': True
        }

        # 创建研究员
        print("🚀 正在创建研究员智能体...")
        researcher = ResearcherAgent()
        agent = researcher.create_agent(config)

        print("✅ 研究员智能体创建成功")
        print(f"📋 Agent角色: {agent.role}")
        print(f"🎯 Agent目标: {agent.goal}")
        print(f"🛠️  工具数量: {len(agent.tools) if agent.tools else 0}")

        # 测试源验证
        test_sources = [
            'https://www.gov.cn/test',
            'https://baidu.com/news',
            'http://unknown-site.com'
        ]

        validated = researcher.validate_sources(test_sources)
        print(f"\n📊 源验证结果: {len(validated)} 个源")
        for source in validated:
            print(f"  - {source['domain']}: 信任度 {source['validation_score']:.2f}")

        print("\n🎉 所有测试通过！")
        return True

    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        print("\n🔧 故障排除建议:")
        print("1. 检查 .env 文件是否在项目根目录")
        print("2. 确认 OPENAI_API_KEY 格式正确")
        print("3. 验证 API Key 是否有效")
        print("4. 检查网络连接")
        return False


if __name__ == "__main__":
    # 设置日志
    logging.basicConfig(level=logging.INFO)

    # 运行测试
    test_researcher_agent()