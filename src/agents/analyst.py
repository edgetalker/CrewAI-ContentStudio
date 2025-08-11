"""
分析师智能体 - 负责研究数据分析和内容策略制定
"""
import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, Any, List
import re
import json

# 找到项目根目录并加载环境变量
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent
env_path = project_root / '.env'

if env_path.exists():
    load_dotenv(env_path)

from crewai import Agent

class AnalystAgent:
    """分析师智能体 - 专门负责研究数据分析和内容策略制定"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._check_environment()
        self._initialize_tools()

    def _check_environment(self):
        """检查环境变量配置"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("❌ 未找到 OPENAI_API_KEY，请检查 .env 文件配置")
        print("🔑 OpenAI API Key: 已设置")

    def _initialize_tools(self):
        """初始化分析工具"""
        try:
            # 分析师主要使用内置的LLM分析能力，暂不需要外部工具
            # 可以在后续版本中添加更复杂的分析工具
            print("✅ 分析师工具初始化成功（使用内置分析能力）")

        except Exception as e:
            self.logger.error(f"❌ 工具初始化失败: {str(e)}")
            print(f"💡 调试信息: {str(e)}")
            raise

    def create_agent(self, config: Dict[str, Any]) -> Agent:
        """
        创建分析师智能体

        Args:
            config: 智能体配置字典

        Returns:
            Agent: 配置好的分析师智能体
        """
        try:
            # 分析师智能体主要使用LLM的内置分析能力
            # 不需要外部工具，专注于数据分析和策略制定

            # 创建Agent
            agent = Agent(
                role=config['role'],
                goal=config['goal'],
                backstory=config['backstory'],
                tools=[],  # 暂时不使用外部工具
                max_iter=config.get('max_iter', 2),
                max_execution_time=config.get('max_execution_time', 200),
                verbose=config.get('verbose', True),
                allow_delegation=config.get('allow_delegation', False),
                memory=True
            )

            self.logger.info("✅ 分析师智能体创建成功")
            print(f"📊 分析师智能体已创建 - {agent.role}")
            return agent

        except Exception as e:
            self.logger.error(f"❌ 创建分析师智能体失败: {str(e)}")
            raise

    def analyze_research_data(self, research_data: str) -> Dict[str, Any]:
        """
        分析研究数据，提取关键洞察

        Args:
            research_data: 研究员提供的研究数据

        Returns:
            Dict: 分析结果
        """
        try:
            analysis_result = {
                'key_themes': self._extract_key_themes(research_data),
                'data_points': self._extract_data_points(research_data),
                'expert_opinions': self._extract_expert_opinions(research_data),
                'trends': self._identify_trends(research_data),
                'audience_insights': self._analyze_audience_relevance(research_data),
                'content_gaps': self._identify_content_gaps(research_data)
            }

            return analysis_result

        except Exception as e:
            self.logger.error(f"❌ 研究数据分析失败: {str(e)}")
            raise

    def _extract_key_themes(self, data: str) -> List[str]:
        """提取关键主题"""
        # 简单的关键词提取逻辑
        # 在实际项目中可以使用更复杂的NLP技术
        themes = []

        # 查找常见的主题标识词
        theme_patterns = [
            r'人工智能|AI|机器学习|深度学习',
            r'数字化转型|数字化|智能化',
            r'自动化|智能制造|工业4\.0',
            r'大数据|数据分析|数据科学',
            r'云计算|边缘计算|分布式',
            r'区块链|加密货币|Web3',
        ]

        for pattern in theme_patterns:
            if re.search(pattern, data, re.IGNORECASE):
                themes.append(pattern.split('|')[0])

        return themes[:5]  # 返回前5个主题

    def _extract_data_points(self, data: str) -> List[Dict[str, Any]]:
        """提取数据点和统计信息"""
        data_points = []

        # 查找数字和百分比
        number_patterns = [
            r'(\d+(?:\.\d+)?%)',  # 百分比
            r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(?:亿|万|千|百)',  # 中文数字单位
            r'(\$\d+(?:,\d{3})*(?:\.\d+)?)\s*(?:billion|million|thousand|万|亿)',  # 货币
        ]

        for pattern in number_patterns:
            matches = re.findall(pattern, data, re.IGNORECASE)
            for match in matches[:3]:  # 限制数量
                data_points.append({
                    'value': match,
                    'context': self._get_context_around_match(data, match)
                })

        return data_points

    def _extract_expert_opinions(self, data: str) -> List[str]:
        """提取专家观点"""
        opinions = []

        # 查找引用和观点标识
        opinion_patterns = [
            r'专家(?:认为|表示|指出)[^。！？]*[。！？]',
            r'研究(?:显示|表明|发现)[^。！？]*[。！？]',
            r'分析师(?:认为|预测|指出)[^。！？]*[。！？]',
        ]

        for pattern in opinion_patterns:
            matches = re.findall(pattern, data)
            opinions.extend(matches[:2])  # 每种类型最多2个

        return opinions[:5]  # 总共最多5个观点

    def _identify_trends(self, data: str) -> List[str]:
        """识别趋势"""
        trends = []

        # 查找趋势相关词汇
        trend_patterns = [
            r'(?:上升|增长|提高|增加)[^。！？]*[。！？]',
            r'(?:下降|减少|降低|衰减)[^。！？]*[。！？]',
            r'(?:趋势|发展|变化|演进)[^。！？]*[。！？]',
        ]

        for pattern in trend_patterns:
            matches = re.findall(pattern, data)
            trends.extend(matches[:2])

        return trends[:5]

    def _analyze_audience_relevance(self, data: str) -> Dict[str, Any]:
        """分析目标受众相关性"""
        return {
            'target_groups': ['技术专业人士', '企业决策者', '创业者'],
            'interest_level': 'high',
            'complexity_level': 'medium_to_high',
            'key_concerns': ['技术发展', '市场机会', '投资价值']
        }

    def _identify_content_gaps(self, data: str) -> List[str]:
        """识别内容空白点"""
        gaps = [
            '缺少具体实施案例',
            '需要更多数据支撑',
            '应该包含风险分析',
            '可以增加对比分析'
        ]
        return gaps[:3]

    def _get_context_around_match(self, text: str, match: str, context_length: int = 50) -> str:
        """获取匹配词周围的上下文"""
        try:
            index = text.find(match)
            if index != -1:
                start = max(0, index - context_length)
                end = min(len(text), index + len(match) + context_length)
                return text[start:end].strip()
            return match
        except:
            return match

    def generate_content_outline(self, analysis_result: Dict[str, Any], content_type: str = "blog_post") -> Dict[str, Any]:
        """
        基于分析结果生成内容大纲

        Args:
            analysis_result: 分析结果
            content_type: 内容类型

        Returns:
            Dict: 内容大纲
        """
        outline = {
            'title_suggestions': [
                f"深度解析：{analysis_result['key_themes'][0] if analysis_result['key_themes'] else '主题'}的最新发展",
                f"2025年{analysis_result['key_themes'][0] if analysis_result['key_themes'] else '技术'}趋势全解读",
                f"专家观点：{analysis_result['key_themes'][0] if analysis_result['key_themes'] else '行业'}的机遇与挑战"
            ],
            'structure': {
                '引言': '介绍主题背景和重要性',
                '现状分析': '基于研究数据的现状解读',
                '趋势洞察': '未来发展趋势预测',
                '专家观点': '行业专家的深度见解',
                '实际应用': '具体案例和应用场景',
                '结论建议': '总结和行动建议'
            },
            'key_points': analysis_result.get('key_themes', []),
            'data_support': analysis_result.get('data_points', []),
            'seo_keywords': self._generate_seo_keywords(analysis_result),
            'target_audience': analysis_result.get('audience_insights', {}),
            'estimated_length': self._estimate_content_length(content_type)
        }

        return outline

    def _generate_seo_keywords(self, analysis_result: Dict[str, Any]) -> List[str]:
        """生成SEO关键词"""
        keywords = []

        # 从主题中提取关键词
        themes = analysis_result.get('key_themes', [])
        keywords.extend(themes)

        # 添加通用SEO词汇
        common_keywords = ['2025年', '最新趋势', '深度分析', '专家观点', '发展前景']
        keywords.extend(common_keywords)

        return keywords[:10]  # 返回前10个关键词

    def _estimate_content_length(self, content_type: str) -> int:
        """估算内容长度"""
        length_map = {
            'blog_post': 1200,
            'article': 1500,
            'report': 2500,
            'news': 800,
            'tutorial': 2000
        }
        return length_map.get(content_type, 1200)


# 测试函数
def test_analyst_agent():
    """测试分析师智能体"""
    print("📊 测试分析师智能体...")
    print(f"📁 当前工作目录: {os.getcwd()}")
    print(f"🔑 OPENAI_API_KEY: {'已设置' if os.getenv('OPENAI_API_KEY') else '未设置'}")

    try:
        # 模拟配置
        config = {
            'role': '内容策略分析师',
            'goal': '分析研究数据并制定内容策略',
            'backstory': '你是一位资深的内容策略专家',
            'max_iter': 2,
            'verbose': True
        }

        # 创建分析师
        print("🚀 正在创建分析师智能体...")
        analyst = AnalystAgent()
        agent = analyst.create_agent(config)

        print("✅ 分析师智能体创建成功")
        print(f"📋 Agent角色: {agent.role}")
        print(f"🎯 Agent目标: {agent.goal}")
        print(f"🛠️  工具数量: {len(agent.tools) if agent.tools else 0} (使用内置分析能力)")

        # 测试分析功能
        sample_research = """
        人工智能技术在2024年取得了重大突破，市场规模达到1840亿美元，同比增长37%。
        专家认为AI将在未来5年内彻底改变制造业。研究显示85%的企业正在考虑AI投资。
        """

        print("\n🔍 测试研究数据分析...")
        analysis_result = analyst.analyze_research_data(sample_research)

        print("📈 分析结果:")
        print(f"  - 关键主题: {analysis_result['key_themes']}")
        print(f"  - 数据点: {len(analysis_result['data_points'])} 个")
        print(f"  - 专家观点: {len(analysis_result['expert_opinions'])} 个")

        print("\n📝 测试内容大纲生成...")
        outline = analyst.generate_content_outline(analysis_result, "blog_post")
        print(f"  - 标题建议: {len(outline['title_suggestions'])} 个")
        print(f"  - 内容结构: {len(outline['structure'])} 个部分")
        print(f"  - SEO关键词: {outline['seo_keywords'][:5]}")

        print("\n🎉 所有测试通过！")
        return True

    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        print("\n🔧 故障排除建议:")
        print("1. 检查 .env 文件配置")
        print("2. 确认 OPENAI_API_KEY 有效")
        print("3. 检查网络连接")
        return False


if __name__ == "__main__":
    # 设置日志
    logging.basicConfig(level=logging.INFO)

    # 运行测试
    test_analyst_agent()