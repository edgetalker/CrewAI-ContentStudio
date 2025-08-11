"""
基础环境测试 - 验证CrewAI是否正常工作
"""
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool

# 加载环境变量
load_dotenv()


def test_environment():
    """测试基础环境配置"""
    print("🔍 检查环境配置...")

    # 检查API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ 未找到OPENAI_API_KEY，请检查.env文件")
        return False
    elif not api_key.startswith("sk-"):
        print("❌ API key格式不正确")
        return False
    else:
        print("✅ API key配置正确")

    return True


def test_simple_agent():
    """测试创建简单Agent"""
    print("\n🤖 测试创建Agent...")

    try:
        # 创建一个简单的Agent
        test_agent = Agent(
            role='测试助手',
            goal='验证系统是否正常工作',
            backstory='你是一个用来测试系统的助手',
            verbose=True,
            allow_delegation=False
        )

        # 创建简单任务
        test_task = Task(
            description='请简单介绍一下人工智能，不超过100字',
            expected_output='关于人工智能的简短介绍',
            agent=test_agent
        )

        # 创建Crew
        test_crew = Crew(
            agents=[test_agent],
            tasks=[test_task],
            verbose=True
        )

        print("✅ Agent和Crew创建成功")
        return test_crew

    except Exception as e:
        print(f"❌ 创建Agent失败: {str(e)}")
        return None


def run_simple_test():
    """运行简单测试"""
    print("\n🚀 运行简单测试...")

    try:
        # 环境检查
        if not test_environment():
            return

        # 创建Agent
        crew = test_simple_agent()
        if not crew:
            return

        # 执行任务
        print("\n📝 执行任务中...")
        result = crew.kickoff()

        print("\n🎉 测试成功完成！")
        print("📄 生成结果:")
        print("-" * 50)
        print(result)
        print("-" * 50)

        # 保存结果
        with open("data/outputs/test_result.txt", "w", encoding="utf-8") as f:
            f.write(str(result))
        print("\n💾 结果已保存到 data/outputs/test_result.txt")

    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        print("\n🔧 常见解决方案:")
        print("1. 检查API key是否正确")
        print("2. 确认网络连接正常")
        print("3. 验证API账户有足够配额")


if __name__ == "__main__":
    print("🎯 CrewAI-ContentStudio 基础测试")
    print("=" * 50)
    run_simple_test()