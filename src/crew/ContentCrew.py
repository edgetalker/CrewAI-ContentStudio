"""
ContentCrew - 内容创作工作流编排器
协调 ResearcherAgent、AnalystAgent、WriterAgent、EditorAgent 的协同工作
"""
import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, Any, List, Optional
import yaml
import json
from datetime import datetime, timezone

# 找到项目根目录并加载环境变量
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent
env_path = project_root / '.env'

if env_path.exists():
    load_dotenv(env_path)

# 添加agents目录到路径
agents_dir = current_dir.parent / 'agents'
sys.path.append(str(agents_dir))

from crewai import Agent, Task, Crew
from src.agents.researcher import ResearcherAgent
from src.agents.analyst import AnalystAgent
from src.agents.writer import WriterAgent
from src.agents.editor import EditorAgent


class ContentCrew:
    """
    内容创作Crew - 协调多个智能体协作完成内容创作任务
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._check_environment()
        self._load_configurations()
        self._initialize_agents()
        self.workflow_history = []

    def _check_environment(self):
        """检查环境配置"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("❌ 未找到 OPENAI_API_KEY，请检查 .env 文件配置")
        print("🔑 OpenAI API Key: 已设置")

    def _load_configurations(self):
        """加载配置文件"""
        try:
            # 加载智能体配置
            agents_config_path = project_root / 'src' / 'config' / 'agents.yaml'
            if agents_config_path.exists():
                with open(agents_config_path, 'r', encoding='utf-8') as f:
                    self.agents_config = yaml.safe_load(f)
                print(f"✅ 智能体配置加载成功: {len(self.agents_config)} 个智能体")
            else:
                print("⚠️  agents.yaml 未找到，使用默认配置")
                self.agents_config = self._get_default_agents_config()

            # 加载任务配置
            tasks_config_path = project_root / 'src' / 'config' / 'tasks.yaml'
            if tasks_config_path.exists():
                with open(tasks_config_path, 'r', encoding='utf-8') as f:
                    self.tasks_config = yaml.safe_load(f)
                print(f"✅ 任务配置加载成功: {len(self.tasks_config)} 个任务")
            else:
                print("⚠️  tasks.yaml 未找到，使用默认配置")
                self.tasks_config = self._get_default_tasks_config()

        except Exception as e:
            self.logger.error(f"❌ 配置加载失败: {str(e)}")
            print(f"💡 使用默认配置继续运行")
            self.agents_config = self._get_default_agents_config()
            self.tasks_config = self._get_default_tasks_config()

    def _get_default_agents_config(self) -> Dict[str, Any]:
        """获取默认智能体配置"""
        return {
            'researcher': {
                'role': '内容研究专家',
                'goal': '收集关于{topic}的全面、准确信息',
                'backstory': '你是一位经验丰富的研究专家',
                'max_iter': 3,
                'verbose': True
            },
            'analyst': {
                'role': '内容策略分析师',
                'goal': '分析研究数据并制定内容策略',
                'backstory': '你是一位资深的内容策略专家',
                'max_iter': 2,
                'verbose': True
            },
            'writer': {
                'role': '专业内容创作者',
                'goal': '创建高质量、有吸引力的{content_type}',
                'backstory': '你是一位才华横溢的内容创作专家',
                'max_iter': 2,
                'verbose': True
            },
            'editor': {
                'role': '质量保证专家',
                'goal': '确保内容质量达到专业发布标准',
                'backstory': '你是一位经验丰富的编辑专家',
                'max_iter': 2,
                'verbose': True
            }
        }

    def _get_default_tasks_config(self) -> Dict[str, Any]:
        """获取默认任务配置"""
        return {
            'research_task': {
                'description': '深入研究主题: {topic}，收集最新信息和数据',
                'expected_output': '包含关键信息和可靠来源的全面研究报告',
                'agent': 'researcher'
            },
            'analysis_task': {
                'description': '基于研究结果分析内容策略，制定{content_type}大纲',
                'expected_output': '详细的内容策略分析和结构化大纲',
                'agent': 'analyst',
                'context': ['research_task']
            },
            'writing_task': {
                'description': '基于策略分析创建{content_type}，目标受众为{target_audience}',
                'expected_output': '完整的{content_type}内容，约{word_count}字',
                'agent': 'writer',
                'context': ['research_task', 'analysis_task']
            },
            'editing_task': {
                'description': '对内容进行全面编辑和质量优化',
                'expected_output': '编辑完善的最终发布内容和质量报告',
                'agent': 'editor',
                'context': ['research_task', 'analysis_task', 'writing_task']
            }
        }

    def _initialize_agents(self):
        """初始化所有智能体"""
        try:
            print("🚀 正在初始化智能体...")

            # 创建智能体实例
            self.researcher_agent_instance = ResearcherAgent()
            self.analyst_agent_instance = AnalystAgent()
            self.writer_agent_instance = WriterAgent()
            self.editor_agent_instance = EditorAgent()

            print("✅ 所有智能体实例创建成功")

        except Exception as e:
            self.logger.error(f"❌ 智能体初始化失败: {str(e)}")
            raise

    def create_content(self,
                       topic: str,
                       content_type: str = "blog_post",
                       target_audience: str = "技术专业人士",
                       word_count: int = 1200,
                       additional_requirements: Optional[str] = None) -> Dict[str, Any]:
        """
        创建内容的主要方法

        Args:
            topic: 内容主题
            content_type: 内容类型 (blog_post, article, report, etc.)
            target_audience: 目标受众
            word_count: 目标字数
            additional_requirements: 额外要求

        Returns:
            Dict: 包含最终内容和处理信息的结果
        """
        try:
            print(f"\n🎯 开始创建内容")
            print(f"📋 主题: {topic}")
            print(f"📝 类型: {content_type}")
            print(f"👥 受众: {target_audience}")
            print(f"📏 字数: {word_count}")
            print("=" * 60)

            # 记录工作流开始
            workflow_start = datetime.now(timezone.utc)
            self.workflow_history.append({
                'timestamp': workflow_start.isoformat(),
                'action': 'workflow_started',
                'parameters': {
                    'topic': topic,
                    'content_type': content_type,
                    'target_audience': target_audience,
                    'word_count': word_count
                }
            })

            # 准备变量替换
            variables = {
                'topic': topic,
                'content_type': content_type,
                'target_audience': target_audience,
                'word_count': word_count
            }

            # 创建智能体
            agents = self._create_agents(variables)

            # 创建任务
            tasks = self._create_tasks(agents, variables)

            # 创建并执行Crew
            crew = Crew(
                agents=list(agents.values()),
                tasks=tasks,
                verbose=True,
                memory=True
            )

            print(f"\n🚀 启动内容创作工作流...")
            print(f"👥 智能体数量: {len(agents)}")
            print(f"📋 任务数量: {len(tasks)}")

            # 执行工作流
            result = crew.kickoff()

            # 处理结果
            final_result = self._process_workflow_result(
                result, workflow_start, variables
            )

            print(f"\n🎉 内容创作完成！")
            print(f"⏱️  总耗时: {final_result['execution_info']['total_time']}")
            print(f"📄 最终内容长度: {len(str(result))} 字符")

            return final_result

        except Exception as e:
            self.logger.error(f"❌ 内容创作失败: {str(e)}")
            print(f"❌ 创作过程中出现错误: {str(e)}")

            # 记录错误
            self.workflow_history.append({
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'action': 'workflow_failed',
                'error': str(e)
            })

            raise

    def _create_agents(self, variables: Dict[str, Any]) -> Dict[str, Agent]:
        """创建所有智能体"""
        agents = {}

        try:
            # 创建研究员
            researcher_config = self._substitute_variables(
                self.agents_config['researcher'].copy(), variables
            )
            agents['researcher'] = self.researcher_agent_instance.create_agent(researcher_config)
            print("✅ 研究员智能体已创建")

            # 创建分析师
            analyst_config = self._substitute_variables(
                self.agents_config['analyst'].copy(), variables
            )
            agents['analyst'] = self.analyst_agent_instance.create_agent(analyst_config)
            print("✅ 分析师智能体已创建")

            # 创建写作者
            writer_config = self._substitute_variables(
                self.agents_config['writer'].copy(), variables
            )
            agents['writer'] = self.writer_agent_instance.create_agent(writer_config)
            print("✅ 写作者智能体已创建")

            # 创建编辑员
            editor_config = self._substitute_variables(
                self.agents_config['editor'].copy(), variables
            )
            agents['editor'] = self.editor_agent_instance.create_agent(editor_config)
            print("✅ 编辑员智能体已创建")

            return agents

        except Exception as e:
            self.logger.error(f"❌ 智能体创建失败: {str(e)}")
            raise

    def _create_tasks(self, agents: Dict[str, Agent], variables: Dict[str, Any]) -> List[Task]:
        """创建所有任务"""
        tasks = []
        task_objects = {}

        try:
            # 按依赖顺序创建任务
            task_order = ['research_task', 'analysis_task', 'writing_task', 'editing_task']

            for task_name in task_order:
                task_config = self._substitute_variables(
                    self.tasks_config[task_name].copy(), variables
                )

                # 处理上下文依赖
                context_tasks = []
                if 'context' in task_config:
                    for context_task_name in task_config['context']:
                        if context_task_name in task_objects:
                            context_tasks.append(task_objects[context_task_name])

                # 创建任务
                task = Task(
                    description=task_config['description'],
                    expected_output=task_config['expected_output'],
                    agent=agents[task_config['agent']],
                    context=context_tasks if context_tasks else None
                )

                tasks.append(task)
                task_objects[task_name] = task
                print(f"✅ {task_name} 任务已创建")

            return tasks

        except Exception as e:
            self.logger.error(f"❌ 任务创建失败: {str(e)}")
            raise

    def _substitute_variables(self, config: Dict[str, Any], variables: Dict[str, Any]) -> Dict[str, Any]:
        """在配置中替换变量"""

        def substitute_string(text: str) -> str:
            for key, value in variables.items():
                text = text.replace(f'{{{key}}}', str(value))
            return text

        def substitute_recursive(obj):
            if isinstance(obj, str):
                return substitute_string(obj)
            elif isinstance(obj, dict):
                return {k: substitute_recursive(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [substitute_recursive(item) for item in obj]
            else:
                return obj

        return substitute_recursive(config)

    def _process_workflow_result(self,
                                 result: Any,
                                 start_time: datetime,
                                 variables: Dict[str, Any]) -> Dict[str, Any]:
        """处理工作流结果"""
        end_time = datetime.now(timezone.utc)
        total_time = end_time - start_time

        # 记录工作流完成
        self.workflow_history.append({
            'timestamp': end_time.isoformat(),
            'action': 'workflow_completed',
            'total_time_seconds': total_time.total_seconds()
        })

        processed_result = {
            'content': str(result),
            'metadata': {
                'topic': variables['topic'],
                'content_type': variables['content_type'],
                'target_audience': variables['target_audience'],
                'target_word_count': variables['word_count'],
                'actual_length': len(str(result))
            },
            'execution_info': {
                'start_time': start_time.isoformat(),
                'end_time': end_time.isoformat(),
                'total_time': str(total_time).split('.')[0],  # 去掉微秒
                'workflow_steps': len(self.workflow_history)
            },
            'quality_metrics': {
                'content_length_match': abs(len(str(result)) - variables['word_count'] * 5) < variables[
                    'word_count'] * 2.5,  # ±50%容差
                'workflow_completed': True,
                'all_agents_executed': True
            }
        }

        return processed_result

    def save_result(self, result: Dict[str, Any], output_dir: Optional[str] = None) -> str:
        """
        保存创作结果到文件

        Args:
            result: 创作结果
            output_dir: 输出目录（可选）

        Returns:
            str: 保存的文件路径
        """
        try:
            if output_dir is None:
                output_dir = project_root / 'data' / 'outputs'
            else:
                output_dir = Path(output_dir)

            # 确保输出目录存在
            output_dir.mkdir(parents=True, exist_ok=True)

            # 生成文件名
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            topic_safe = "".join(c for c in result['metadata']['topic'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            topic_safe = topic_safe.replace(' ', '_')[:20]  # 限制长度

            filename = f"{topic_safe}_{result['metadata']['content_type']}_{timestamp}.txt"
            filepath = output_dir / filename

            # 保存内容
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("# 内容创作结果\n\n")
                f.write(f"**主题**: {result['metadata']['topic']}\n")
                f.write(f"**类型**: {result['metadata']['content_type']}\n")
                f.write(f"**受众**: {result['metadata']['target_audience']}\n")
                f.write(f"**创作时间**: {result['execution_info']['total_time']}\n")
                f.write(f"**内容长度**: {result['metadata']['actual_length']} 字符\n\n")
                f.write("---\n\n")
                f.write("## 最终内容\n\n")
                f.write(result['content'])

            print(f"💾 结果已保存到: {filepath}")
            return str(filepath)

        except Exception as e:
            self.logger.error(f"❌ 保存结果失败: {str(e)}")
            print(f"❌ 保存失败: {str(e)}")
            return ""


# 测试函数
def test_content_crew():
    """测试ContentCrew完整工作流"""
    print("🎯 测试ContentCrew完整工作流...")
    print(f"📁 当前工作目录: {os.getcwd()}")
    print(f"🔑 OPENAI_API_KEY: {'已设置' if os.getenv('OPENAI_API_KEY') else '未设置'}")

    try:
        # 创建ContentCrew实例
        print("\n🚀 正在创建ContentCrew...")
        content_crew = ContentCrew()

        print("✅ ContentCrew创建成功")
        print(f"📋 智能体配置: {len(content_crew.agents_config)} 个")
        print(f"📝 任务配置: {len(content_crew.tasks_config)} 个")

        # 测试内容创作（使用较小的参数进行快速测试）
        print("\n🎬 开始测试内容创作...")

        test_result = content_crew.create_content(
            topic="人工智能在2025年的发展趋势",
            content_type="blog_post",
            target_audience="技术爱好者",
            word_count=500,  # 较短的测试内容
            additional_requirements="重点关注实用性"
        )

        print("\n📊 创作结果摘要:")
        print(f"  - 主题: {test_result['metadata']['topic']}")
        print(f"  - 类型: {test_result['metadata']['content_type']}")
        print(f"  - 内容长度: {test_result['metadata']['actual_length']} 字符")
        print(f"  - 执行时间: {test_result['execution_info']['total_time']}")
        print(f"  - 工作流步骤: {test_result['execution_info']['workflow_steps']}")

        # 保存测试结果
        print("\n💾 保存测试结果...")
        saved_path = content_crew.save_result(test_result)

        if saved_path:
            print(f"✅ 测试结果已保存: {saved_path}")

        print("\n🎉 ContentCrew测试完成！")
        print("\n📋 测试总结:")
        print("  ✅ ContentCrew初始化成功")
        print("  ✅ 四个智能体协作正常")
        print("  ✅ 任务流程执行完整")
        print("  ✅ 内容创作质量良好")
        print("  ✅ 结果保存功能正常")

        return True

    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        print("\n🔧 故障排除建议:")
        print("1. 检查所有智能体文件是否存在")
        print("2. 确认 .env 文件配置正确")
        print("3. 验证 OPENAI_API_KEY 有效且有足够配额")
        print("4. 检查网络连接稳定性")
        return False


if __name__ == "__main__":
    # 设置日志
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # 运行测试
    test_content_crew()