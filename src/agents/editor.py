"""
编辑员智能体 - 负责内容质量控制和优化
"""
import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, Any, List, Tuple
import re
import json
from datetime import datetime

# 找到项目根目录并加载环境变量
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent
env_path = project_root / '.env'

if env_path.exists():
    load_dotenv(env_path)

from crewai import Agent


class EditorAgent:
    """编辑员智能体 - 专门负责内容质量控制和优化"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._check_environment()
        self._initialize_tools()
        self._load_editing_rules()

    def _check_environment(self):
        """检查环境变量配置"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("❌ 未找到 OPENAI_API_KEY，请检查 .env 文件配置")
        print("🔑 OpenAI API Key: 已设置")

    def _initialize_tools(self):
        """初始化编辑工具"""
        try:
            # 编辑者使用LLM的内置语言处理和分析能力
            # 专注于质量控制、语言优化和格式规范
            print("✅ 编辑工具初始化成功（使用内置语言处理能力）")

        except Exception as e:
            self.logger.error(f"❌ 工具初始化失败: {str(e)}")
            print(f"💡 调试信息: {str(e)}")
            raise

    def _load_editing_rules(self):
        """加载编辑规则和质量标准"""
        self.editing_rules = {
            'grammar_rules': {
                'punctuation_check': True,
                'sentence_structure': True,
                'word_choice': True,
                'tense_consistency': True
            },
            'style_rules': {
                'tone_consistency': True,
                'voice_active_preferred': True,
                'paragraph_length_optimal': True,
                'transition_smooth': True
            },
            'seo_rules': {
                'keyword_density': {'min': 1, 'max': 3},  # 1-3%
                'title_optimization': True,
                'meta_description': True,
                'heading_structure': True
            },
            'readability_rules': {
                'sentence_length_avg': 20,  # 平均20字以下
                'paragraph_length_max': 150,  # 最多150字
                'complex_words_ratio': 0.15,  # 复杂词汇不超过15%
                'passive_voice_ratio': 0.1  # 被动语态不超过10%
            },
            'format_rules': {
                'heading_hierarchy': True,
                'list_formatting': True,
                'emphasis_appropriate': True,
                'link_formatting': True
            }
        }

        # 常见错误模式
        self.common_errors = {
            'grammar': [
                r'的的',  # 重复的"的"
                r'了了',  # 重复的"了"
                r'在在',  # 重复介词
                r'是是',  # 重复系动词
            ],
            'punctuation': [
                r'，，',  # 重复逗号
                r'。。',  # 重复句号
                r'？？',  # 重复问号
                r'！！',  # 重复感叹号
            ],
            'spacing': [
                r'\s+',  # 多余空格
                r'\n\n\n+',  # 多余换行
            ]
        }

        print(f"📋 加载了 {len(self.editing_rules)} 类编辑规则")

    def create_agent(self, config: Dict[str, Any]) -> Agent:
        """
        创建编辑员智能体

        Args:
            config: 智能体配置字典

        Returns:
            Agent: 配置好的编辑员智能体
        """
        try:
            # 编辑员智能体专注于质量控制，使用LLM的内置语言处理能力

            # 创建Agent
            agent = Agent(
                role=config['role'],
                goal=config['goal'],
                backstory=config['backstory'],
                tools=[],  # 使用内置编辑能力
                max_iter=config.get('max_iter', 2),
                max_execution_time=config.get('max_execution_time', 250),
                verbose=config.get('verbose', True),
                allow_delegation=config.get('allow_delegation', False),
                memory=True
            )

            self.logger.info("✅ 编辑员智能体创建成功")
            print(f"📝 编辑员智能体已创建 - {agent.role}")
            return agent

        except Exception as e:
            self.logger.error(f"❌ 创建编辑员智能体失败: {str(e)}")
            raise

    def analyze_content_quality(self, content: str, content_type: str = "blog_post") -> Dict[str, Any]:
        """
        分析内容质量

        Args:
            content: 待分析的内容
            content_type: 内容类型

        Returns:
            Dict: 质量分析结果
        """
        try:
            quality_analysis = {
                'overall_score': 0,
                'grammar_analysis': self._check_grammar(content),
                'readability_analysis': self._check_readability(content),
                'seo_analysis': self._check_seo_optimization(content),
                'structure_analysis': self._check_structure(content, content_type),
                'style_analysis': self._check_style_consistency(content),
                'improvement_suggestions': []
            }

            # 计算总体评分
            quality_analysis['overall_score'] = self._calculate_overall_score(quality_analysis)

            # 生成改进建议
            quality_analysis['improvement_suggestions'] = self._generate_improvement_suggestions(quality_analysis)

            return quality_analysis

        except Exception as e:
            self.logger.error(f"❌ 内容质量分析失败: {str(e)}")
            raise

    def _check_grammar(self, content: str) -> Dict[str, Any]:
        """检查语法质量"""
        grammar_issues = []

        # 检查常见语法错误
        for error_type, patterns in self.common_errors.items():
            for pattern in patterns:
                matches = re.findall(pattern, content)
                if matches:
                    grammar_issues.append({
                        'type': error_type,
                        'pattern': pattern,
                        'count': len(matches),
                        'examples': matches[:3]  # 最多显示3个例子
                    })

        # 基础语法检查
        sentence_count = len(re.findall(r'[。！？]', content))
        word_count = len(content.replace(' ', '').replace('\n', ''))
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0

        grammar_score = max(0, 100 - len(grammar_issues) * 10)

        return {
            'score': grammar_score,
            'issues_found': len(grammar_issues),
            'issues_detail': grammar_issues,
            'avg_sentence_length': round(avg_sentence_length, 1),
            'total_sentences': sentence_count,
            'total_words': word_count
        }

    def _check_readability(self, content: str) -> Dict[str, Any]:
        """检查可读性"""
        # 段落分析
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        paragraph_lengths = [len(p) for p in paragraphs]
        avg_paragraph_length = sum(paragraph_lengths) / len(paragraph_lengths) if paragraph_lengths else 0

        # 句子分析
        sentences = re.split(r'[。！？]', content)
        sentences = [s.strip() for s in sentences if s.strip()]
        sentence_lengths = [len(s) for s in sentences]
        avg_sentence_length = sum(sentence_lengths) / len(sentence_lengths) if sentence_lengths else 0

        # 可读性评分 (简化版)
        readability_score = 100

        # 段落长度扣分
        if avg_paragraph_length > 200:
            readability_score -= 20
        elif avg_paragraph_length > 150:
            readability_score -= 10

        # 句子长度扣分
        if avg_sentence_length > 30:
            readability_score -= 20
        elif avg_sentence_length > 25:
            readability_score -= 10

        return {
            'score': max(0, readability_score),
            'avg_paragraph_length': round(avg_paragraph_length, 1),
            'avg_sentence_length': round(avg_sentence_length, 1),
            'total_paragraphs': len(paragraphs),
            'total_sentences': len(sentences),
            'readability_level': self._get_readability_level(readability_score)
        }

    def _check_seo_optimization(self, content: str) -> Dict[str, Any]:
        """检查SEO优化"""
        # 标题检查
        titles = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)
        h1_titles = re.findall(r'^#\s+(.+)$', content, re.MULTILINE)

        # 关键词密度分析 (示例)
        # 在实际应用中，这里需要传入实际的目标关键词
        sample_keywords = ['人工智能', 'AI', '技术', '发展']
        keyword_analysis = {}

        total_words = len(content.replace(' ', '').replace('\n', ''))

        for keyword in sample_keywords:
            count = content.count(keyword)
            density = (count * len(keyword) / total_words * 100) if total_words > 0 else 0
            keyword_analysis[keyword] = {
                'count': count,
                'density': round(density, 2)
            }

        seo_score = 80  # 基础分

        # 标题结构检查
        if not h1_titles:
            seo_score -= 20
        elif len(h1_titles) > 1:
            seo_score -= 10

        if len(titles) < 3:
            seo_score -= 10

        return {
            'score': max(0, seo_score),
            'title_analysis': {
                'h1_count': len(h1_titles),
                'total_headings': len(titles),
                'heading_hierarchy': len(titles) >= 3
            },
            'keyword_analysis': keyword_analysis,
            'meta_elements': {
                'title_optimized': len(h1_titles) == 1,
                'headings_present': len(titles) > 0
            }
        }

    def _check_structure(self, content: str, content_type: str) -> Dict[str, Any]:
        """检查内容结构"""
        # 基本结构元素检查
        has_introduction = bool(re.search(r'(引言|介绍|概述|背景)', content[:200]))
        has_conclusion = bool(re.search(r'(结论|总结|展望|建议)', content[-200:]))
        has_headings = bool(re.findall(r'^#+\s+', content, re.MULTILINE))

        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]

        structure_score = 70  # 基础分

        if has_introduction:
            structure_score += 10
        if has_conclusion:
            structure_score += 10
        if has_headings:
            structure_score += 10
        if len(paragraphs) >= 5:
            structure_score += 10

        return {
            'score': min(100, structure_score),
            'has_introduction': has_introduction,
            'has_conclusion': has_conclusion,
            'has_headings': has_headings,
            'paragraph_count': len(paragraphs),
            'logical_flow': len(paragraphs) >= 3
        }

    def _check_style_consistency(self, content: str) -> Dict[str, Any]:
        """检查风格一致性"""
        # 语调一致性检查 (简化)
        formal_indicators = len(re.findall(r'(因此|然而|此外|综上所述|根据)', content))
        casual_indicators = len(re.findall(r'(其实|不过|当然|说实话)', content))

        # 时态一致性检查
        past_tense = len(re.findall(r'(了|过|曾|已)', content))
        present_tense = len(re.findall(r'(正在|目前|现在|当前)', content))

        style_score = 85  # 基础分

        # 语调不一致扣分
        if formal_indicators > 0 and casual_indicators > 0:
            if abs(formal_indicators - casual_indicators) > 2:
                style_score -= 15

        return {
            'score': max(0, style_score),
            'tone_analysis': {
                'formal_indicators': formal_indicators,
                'casual_indicators': casual_indicators,
                'tone_consistency': abs(formal_indicators - casual_indicators) <= 2
            },
            'tense_analysis': {
                'past_tense_usage': past_tense,
                'present_tense_usage': present_tense
            }
        }

    def _get_readability_level(self, score: int) -> str:
        """获取可读性级别"""
        if score >= 90:
            return 'excellent'
        elif score >= 80:
            return 'good'
        elif score >= 70:
            return 'fair'
        elif score >= 60:
            return 'difficult'
        else:
            return 'very_difficult'

    def _calculate_overall_score(self, analysis: Dict[str, Any]) -> int:
        """计算总体质量评分"""
        scores = []

        # 收集各项评分
        if 'grammar_analysis' in analysis:
            scores.append(analysis['grammar_analysis']['score'])
        if 'readability_analysis' in analysis:
            scores.append(analysis['readability_analysis']['score'])
        if 'seo_analysis' in analysis:
            scores.append(analysis['seo_analysis']['score'])
        if 'structure_analysis' in analysis:
            scores.append(analysis['structure_analysis']['score'])
        if 'style_analysis' in analysis:
            scores.append(analysis['style_analysis']['score'])

        # 计算加权平均分
        if scores:
            overall_score = sum(scores) / len(scores)
            return round(overall_score)

        return 0

    def _generate_improvement_suggestions(self, analysis: Dict[str, Any]) -> List[str]:
        """生成改进建议"""
        suggestions = []

        # 语法建议
        grammar_score = analysis.get('grammar_analysis', {}).get('score', 100)
        if grammar_score < 80:
            suggestions.append("语法检查：发现多处语法错误，建议仔细校对")

        # 可读性建议
        readability = analysis.get('readability_analysis', {})
        if readability.get('avg_sentence_length', 0) > 25:
            suggestions.append("句子长度：建议将长句拆分为更短的句子，提高可读性")

        if readability.get('avg_paragraph_length', 0) > 150:
            suggestions.append("段落长度：建议缩短段落长度，增加换行和分段")

        # SEO建议
        seo_analysis = analysis.get('seo_analysis', {})
        if seo_analysis.get('title_analysis', {}).get('h1_count', 0) != 1:
            suggestions.append("SEO优化：确保有且仅有一个主标题(H1)")

        # 结构建议
        structure = analysis.get('structure_analysis', {})
        if not structure.get('has_introduction'):
            suggestions.append("内容结构：建议添加引言部分")

        if not structure.get('has_conclusion'):
            suggestions.append("内容结构：建议添加结论或总结部分")

        return suggestions[:5]  # 最多返回5个建议

    def generate_editing_report(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成编辑报告

        Args:
            analysis: 质量分析结果

        Returns:
            Dict: 编辑报告
        """
        overall_score = analysis.get('overall_score', 0)

        # 确定质量等级
        if overall_score >= 90:
            quality_grade = 'A+'
            status = 'excellent'
        elif overall_score >= 80:
            quality_grade = 'A'
            status = 'good'
        elif overall_score >= 70:
            quality_grade = 'B'
            status = 'acceptable'
        elif overall_score >= 60:
            quality_grade = 'C'
            status = 'needs_improvement'
        else:
            quality_grade = 'D'
            status = 'major_revision_needed'

        report = {
            'overall_assessment': {
                'score': overall_score,
                'grade': quality_grade,
                'status': status,
                'recommendation': self._get_recommendation(status)
            },
            'detailed_scores': {
                'grammar': analysis.get('grammar_analysis', {}).get('score', 0),
                'readability': analysis.get('readability_analysis', {}).get('score', 0),
                'seo': analysis.get('seo_analysis', {}).get('score', 0),
                'structure': analysis.get('structure_analysis', {}).get('score', 0),
                'style': analysis.get('style_analysis', {}).get('score', 0)
            },
            'priority_improvements': analysis.get('improvement_suggestions', []),
            'editing_checklist': self._generate_editing_checklist(analysis),
            'publication_readiness': overall_score >= 80,
            'estimated_revision_time': self._estimate_revision_time(analysis)
        }

        return report

    def _get_recommendation(self, status: str) -> str:
        """获取推荐行动"""
        recommendations = {
            'excellent': '内容质量优秀，可以直接发布',
            'good': '内容质量良好，建议微调后发布',
            'acceptable': '内容基本合格，建议适度修改后发布',
            'needs_improvement': '内容需要改进，建议修改后重新审核',
            'major_revision_needed': '内容需要大幅修改，建议重写关键部分'
        }
        return recommendations.get(status, '需要进一步评估')

    def _generate_editing_checklist(self, analysis: Dict[str, Any]) -> List[str]:
        """生成编辑检查清单"""
        checklist = []

        # 基础检查项
        checklist.extend([
            '检查语法和拼写错误',
            '确认标点符号使用正确',
            '验证段落长度适中',
            '检查逻辑流畅性'
        ])

        # 根据分析结果添加特定检查项
        if analysis.get('seo_analysis', {}).get('score', 100) < 80:
            checklist.append('优化SEO元素（标题、关键词）')

        if analysis.get('structure_analysis', {}).get('score', 100) < 80:
            checklist.append('完善内容结构（引言、结论）')

        return checklist

    def _estimate_revision_time(self, analysis: Dict[str, Any]) -> str:
        """估算修改时间"""
        overall_score = analysis.get('overall_score', 100)

        if overall_score >= 90:
            return '5-10分钟'
        elif overall_score >= 80:
            return '15-20分钟'
        elif overall_score >= 70:
            return '30-45分钟'
        elif overall_score >= 60:
            return '1-2小时'
        else:
            return '2小时以上'


# 测试函数
def test_editor_agent():
    """测试编辑员智能体"""
    print("📝 测试编辑员智能体...")
    print(f"📁 当前工作目录: {os.getcwd()}")
    print(f"🔑 OPENAI_API_KEY: {'已设置' if os.getenv('OPENAI_API_KEY') else '未设置'}")

    try:
        # 模拟配置
        config = {
            'role': '质量保证专家',
            'goal': '确保内容质量达到专业发布标准',
            'backstory': '你是一位经验丰富的编辑专家',
            'max_iter': 2,
            'verbose': True
        }

        # 创建编辑员
        print("🚀 正在创建编辑员智能体...")
        editor = EditorAgent()
        agent = editor.create_agent(config)

        print("✅ 编辑员智能体创建成功")
        print(f"📋 Agent角色: {agent.role}")
        print(f"🎯 Agent目标: {agent.goal}")
        print(f"🛠️  工具数量: {len(agent.tools) if agent.tools else 0} (使用内置编辑能力)")

        # 模拟需要编辑的内容
        sample_content = """
# 人工智能的发展趋势

人工智能技术在近年来取得了飞速发展。据统计，2024年全球AI市场规模达到1840亿美元。

## 技术突破

机器学习和深度学习技术不断进步，在图像识别、自然语言处理等领域表现突出。专家认为AI将在未来5年内彻底改变制造业的格局。

## 应用场景

目前AI技术已经广泛应用于医疗、金融、教育等多个行业。企业对AI投资的兴趣日益增长，85%的企业正在考虑AI相关投资。

总的来说，人工智能的发展前景非常广阔，值得持续关注。
        """

        # 测试内容质量分析
        print("\n🔍 测试内容质量分析...")
        quality_analysis = editor.analyze_content_quality(sample_content, "blog_post")

        print(f"  - 总体评分: {quality_analysis['overall_score']}/100")
        print(f"  - 语法评分: {quality_analysis['grammar_analysis']['score']}/100")
        print(f"  - 可读性评分: {quality_analysis['readability_analysis']['score']}/100")
        print(f"  - SEO评分: {quality_analysis['seo_analysis']['score']}/100")
        print(f"  - 结构评分: {quality_analysis['structure_analysis']['score']}/100")
        print(f"  - 风格评分: {quality_analysis['style_analysis']['score']}/100")

        # 测试编辑报告生成
        print("\n📊 测试编辑报告生成...")
        editing_report = editor.generate_editing_report(quality_analysis)

        print(f"  - 质量等级: {editing_report['overall_assessment']['grade']}")
        print(f"  - 发布状态: {editing_report['overall_assessment']['status']}")
        print(f"  - 发布就绪: {'是' if editing_report['publication_readiness'] else '否'}")
        print(f"  - 预计修改时间: {editing_report['estimated_revision_time']}")
        print(f"  - 改进建议: {len(editing_report['priority_improvements'])} 条")

        # 显示改进建议
        if editing_report['priority_improvements']:
            print("\n💡 主要改进建议:")
            for i, suggestion in enumerate(editing_report['priority_improvements'], 1):
                print(f"    {i}. {suggestion}")

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
    test_editor_agent()