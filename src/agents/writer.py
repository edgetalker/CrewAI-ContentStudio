"""
写作者智能体 - 负责高质量内容创作
"""
import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, Any, List

# 找到项目根目录并加载环境变量
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent
env_path = project_root / '.env'

if env_path.exists():
    load_dotenv(env_path)

from crewai import Agent


class WriterAgent:
    """写作者智能体 - 专门负责高质量内容创作"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._check_environment()
        self._initialize_tools()
        self._load_writing_templates()

    def _check_environment(self):
        """检查环境变量配置"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("❌ 未找到 OPENAI_API_KEY，请检查 .env 文件配置")
        print("🔑 OpenAI API Key: 已设置")

    def _initialize_tools(self):
        """初始化写作工具"""
        try:
            # 写作者主要使用LLM的内置创作能力
            # 专注于内容生成、语言表达和结构组织
            print("✅ 写作工具初始化成功（使用内置创作能力）")

        except Exception as e:
            self.logger.error(f"❌ 工具初始化失败: {str(e)}")
            print(f"💡 调试信息: {str(e)}")
            raise

    def _load_writing_templates(self):
        """加载写作模板"""
        self.content_templates = {
            'blog_post': {
                'structure': ['引言', '主体内容', '实例分析', '总结建议'],
                'style': 'informative_engaging',
                'target_length': 1200
            },
            'article': {
                'structure': ['背景介绍', '现状分析', '深度解读', '趋势预测', '结论'],
                'style': 'professional_analytical',
                'target_length': 1500
            },
            'report': {
                'structure': ['执行摘要', '研究背景', '详细分析', '关键发现', '建议措施'],
                'style': 'formal_comprehensive',
                'target_length': 2500
            },
            'news': {
                'structure': ['导语', '背景', '详情', '影响', '展望'],
                'style': 'objective_concise',
                'target_length': 800
            },
            'tutorial': {
                'structure': ['概述', '准备工作', '步骤详解', '常见问题', '总结'],
                'style': 'instructional_clear',
                'target_length': 2000
            },
            'marketing': {
                'structure': ['吸引注意', '建立兴趣', '展示价值', '行动呼吁'],
                'style': 'persuasive_engaging',
                'target_length': 1000
            }
        }
        print(f"📚 加载了 {len(self.content_templates)} 种内容模板")

    def create_agent(self, config: Dict[str, Any]) -> Agent:
        """
        创建写作者智能体

        Args:
            config: 智能体配置字典

        Returns:
            Agent: 配置好的写作者智能体
        """
        try:
            # 写作者智能体专注于内容创作，使用LLM的内置写作能力

            # 创建Agent
            agent = Agent(
                role=config['role'],
                goal=config['goal'],
                backstory=config['backstory'],
                tools=[],  # 使用内置写作能力
                max_iter=config.get('max_iter', 2),
                max_execution_time=config.get('max_execution_time', 400),
                verbose=config.get('verbose', True),
                allow_delegation=config.get('allow_delegation', False),
                memory=True
            )

            self.logger.info("✅ 写作者智能体创建成功")
            print(f"✍️  写作者智能体已创建 - {agent.role}")
            return agent

        except Exception as e:
            self.logger.error(f"❌ 创建写作者智能体失败: {str(e)}")
            raise

    def analyze_writing_requirements(self, content_outline: Dict[str, Any], content_type: str = "blog_post") -> Dict[
        str, Any]:
        """
        分析写作要求

        Args:
            content_outline: 分析师提供的内容大纲
            content_type: 内容类型

        Returns:
            Dict: 写作要求分析
        """
        try:
            # 获取模板信息
            template = self.content_templates.get(content_type, self.content_templates['blog_post'])

            # 分析写作要求
            requirements = {
                'content_type': content_type,
                'structure_template': template['structure'],
                'writing_style': template['style'],
                'target_length': template['target_length'],
                'key_points': content_outline.get('key_points', []),
                'target_audience': content_outline.get('target_audience', {}),
                'seo_keywords': content_outline.get('seo_keywords', []),
                'tone_guidelines': self._determine_tone(content_type, content_outline),
                'format_requirements': self._get_format_requirements(content_type)
            }

            return requirements

        except Exception as e:
            self.logger.error(f"❌ 写作要求分析失败: {str(e)}")
            raise

    def _determine_tone(self, content_type: str, outline: Dict[str, Any]) -> Dict[str, str]:
        """确定写作语调"""
        tone_map = {
            'blog_post': {
                'primary': 'friendly_professional',
                'secondary': 'informative',
                'avoid': 'overly_technical'
            },
            'article': {
                'primary': 'authoritative',
                'secondary': 'analytical',
                'avoid': 'casual_colloquial'
            },
            'report': {
                'primary': 'formal_objective',
                'secondary': 'data_driven',
                'avoid': 'emotional_subjective'
            },
            'news': {
                'primary': 'neutral_factual',
                'secondary': 'clear_concise',
                'avoid': 'opinion_based'
            },
            'tutorial': {
                'primary': 'helpful_clear',
                'secondary': 'step_by_step',
                'avoid': 'complex_jargon'
            },
            'marketing': {
                'primary': 'engaging_persuasive',
                'secondary': 'benefit_focused',
                'avoid': 'pushy_aggressive'
            }
        }

        return tone_map.get(content_type, tone_map['blog_post'])

    def _get_format_requirements(self, content_type: str) -> Dict[str, Any]:
        """获取格式要求"""
        format_map = {
            'blog_post': {
                'use_subheadings': True,
                'include_intro_conclusion': True,
                'paragraph_length': 'medium',
                'use_bullet_points': True,
                'include_examples': True
            },
            'article': {
                'use_subheadings': True,
                'include_intro_conclusion': True,
                'paragraph_length': 'long',
                'use_bullet_points': False,
                'include_examples': True
            },
            'report': {
                'use_subheadings': True,
                'include_intro_conclusion': True,
                'paragraph_length': 'long',
                'use_bullet_points': True,
                'include_examples': True
            },
            'news': {
                'use_subheadings': False,
                'include_intro_conclusion': False,
                'paragraph_length': 'short',
                'use_bullet_points': False,
                'include_examples': True
            },
            'tutorial': {
                'use_subheadings': True,
                'include_intro_conclusion': True,
                'paragraph_length': 'medium',
                'use_bullet_points': True,
                'include_examples': True
            },
            'marketing': {
                'use_subheadings': True,
                'include_intro_conclusion': True,
                'paragraph_length': 'short',
                'use_bullet_points': True,
                'include_examples': True
            }
        }

        return format_map.get(content_type, format_map['blog_post'])

    def generate_title_suggestions(self, outline: Dict[str, Any], content_type: str) -> List[str]:
        """
        生成标题建议

        Args:
            outline: 内容大纲
            content_type: 内容类型

        Returns:
            List[str]: 标题建议列表
        """
        key_themes = outline.get('key_points', ['技术发展'])
        main_theme = key_themes[0] if key_themes else '技术趋势'

        title_templates = {
            'blog_post': [
                f"深度解析：{main_theme}的最新发展趋势",
                f"2025年{main_theme}全景解读：机遇与挑战并存",
                f"专业视角：{main_theme}如何重塑行业格局",
                f"{main_theme}实战指南：从理论到应用",
                f"揭秘{main_theme}：你需要知道的关键信息"
            ],
            'article': [
                f"{main_theme}发展现状与未来展望",
                f"深入研究：{main_theme}的技术突破与应用前景",
                f"{main_theme}产业分析：市场格局与投资机会",
                f"权威解读：{main_theme}的战略价值与实施路径"
            ],
            'report': [
                f"{main_theme}行业研究报告（2025年度）",
                f"{main_theme}技术发展白皮书",
                f"{main_theme}市场分析与战略建议报告",
                f"{main_theme}应用现状与趋势分析"
            ],
            'news': [
                f"{main_theme}领域迎来重大突破",
                f"最新：{main_theme}技术获得新进展",
                f"{main_theme}市场出现新动向",
                f"关注：{main_theme}发展的最新消息"
            ],
            'tutorial': [
                f"{main_theme}入门完全指南",
                f"如何快速掌握{main_theme}：实用教程",
                f"{main_theme}实操手册：从零到精通",
                f"学会{main_theme}：分步骤详细教程"
            ],
            'marketing': [
                f"为什么{main_theme}是您的最佳选择？",
                f"发现{main_theme}的无限可能",
                f"领先一步：选择{main_theme}的理由",
                f"改变游戏规则的{main_theme}解决方案"
            ]
        }

        return title_templates.get(content_type, title_templates['blog_post'])[:3]

    def estimate_writing_time(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        估算写作时间和资源需求

        Args:
            requirements: 写作要求

        Returns:
            Dict: 时间估算信息
        """
        target_length = requirements.get('target_length', 1200)
        content_type = requirements.get('content_type', 'blog_post')

        # 基于内容长度和类型的时间估算
        time_factors = {
            'blog_post': 1.0,
            'article': 1.2,
            'report': 1.5,
            'news': 0.8,
            'tutorial': 1.3,
            'marketing': 0.9
        }

        base_time = target_length / 200  # 每200字约需1分钟
        type_factor = time_factors.get(content_type, 1.0)
        estimated_time = base_time * type_factor

        return {
            'estimated_minutes': round(estimated_time, 1),
            'complexity_level': self._assess_complexity(requirements),
            'recommended_iterations': self._get_iteration_count(content_type),
            'quality_factors': self._identify_quality_factors(requirements)
        }

    def _assess_complexity(self, requirements: Dict[str, Any]) -> str:
        """评估写作复杂度"""
        target_length = requirements.get('target_length', 1200)
        key_points_count = len(requirements.get('key_points', []))

        if target_length > 2000 or key_points_count > 8:
            return 'high'
        elif target_length > 1000 or key_points_count > 5:
            return 'medium'
        else:
            return 'low'

    def _get_iteration_count(self, content_type: str) -> int:
        """获取建议迭代次数"""
        iteration_map = {
            'blog_post': 2,
            'article': 2,
            'report': 3,
            'news': 1,
            'tutorial': 2,
            'marketing': 2
        }
        return iteration_map.get(content_type, 2)

    def _identify_quality_factors(self, requirements: Dict[str, Any]) -> List[str]:
        """识别质量关键因素"""
        factors = ['内容原创性', '逻辑清晰度', '语言流畅性']

        if requirements.get('seo_keywords'):
            factors.append('SEO优化')

        if requirements.get('target_audience'):
            factors.append('受众匹配度')

        return factors


# 测试函数
def test_writer_agent():
    """测试写作者智能体"""
    print("✍️  测试写作者智能体...")
    print(f"📁 当前工作目录: {os.getcwd()}")
    print(f"🔑 OPENAI_API_KEY: {'已设置' if os.getenv('OPENAI_API_KEY') else '未设置'}")

    try:
        # 模拟配置
        config = {
            'role': '专业内容创作者',
            'goal': '创建高质量、有吸引力的原创内容',
            'backstory': '你是一位才华横溢的内容创作专家',
            'max_iter': 2,
            'verbose': True
        }

        # 创建写作者
        print("🚀 正在创建写作者智能体...")
        writer = WriterAgent()
        agent = writer.create_agent(config)

        print("✅ 写作者智能体创建成功")
        print(f"📋 Agent角色: {agent.role}")
        print(f"🎯 Agent目标: {agent.goal}")
        print(f"🛠️  工具数量: {len(agent.tools) if agent.tools else 0} (使用内置创作能力)")

        # 模拟分析师提供的内容大纲
        sample_outline = {
            'key_points': ['人工智能', '机器学习', '深度学习'],
            'target_audience': {'groups': ['技术专业人士', '企业决策者']},
            'seo_keywords': ['AI发展', '2025年趋势', '人工智能应用'],
            'structure': {
                '引言': '介绍AI发展背景',
                '现状分析': '当前AI技术现状',
                '趋势预测': '未来发展趋势',
                '结论': '总结和建议'
            }
        }

        # 测试写作要求分析
        print("\n📝 测试写作要求分析...")
        requirements = writer.analyze_writing_requirements(sample_outline, "blog_post")
        print(f"  - 内容类型: {requirements['content_type']}")
        print(f"  - 写作风格: {requirements['writing_style']}")
        print(f"  - 目标长度: {requirements['target_length']} 字")
        print(f"  - 结构模板: {requirements['structure_template']}")

        # 测试标题生成
        print("\n🎯 测试标题生成...")
        titles = writer.generate_title_suggestions(sample_outline, "blog_post")
        print(f"  - 生成标题数量: {len(titles)}")
        for i, title in enumerate(titles, 1):
            print(f"    {i}. {title}")

        # 测试时间估算
        print("\n⏱️  测试时间估算...")
        time_estimate = writer.estimate_writing_time(requirements)
        print(f"  - 预计写作时间: {time_estimate['estimated_minutes']} 分钟")
        print(f"  - 复杂度级别: {time_estimate['complexity_level']}")
        print(f"  - 建议迭代次数: {time_estimate['recommended_iterations']}")
        print(f"  - 质量关键因素: {', '.join(time_estimate['quality_factors'])}")

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
    test_writer_agent()