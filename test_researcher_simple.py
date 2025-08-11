"""
简单的研究员智能体测试脚本
在项目根目录运行: python test_researcher_simple.py
"""
import os
from pathlib import Path
from dotenv import load_dotenv


def main():
    print("🎯 CrewAI ResearcherAgent 测试")
    print("=" * 50)

    # 检查当前目录
    current_dir = Path.cwd()
    print(f"📁 当前目录: {current_dir}")

    # 检查 .env 文件
    env_file = current_dir / '.env'
    if env_file.exists():
        print(f"✅ 找到 .env 文件: {env_file}")
        load_dotenv(env_file)
    else:
        print(f"❌ 未找到 .env 文件: {env_file}")
        return

    # 检查 API Key
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print(f"✅ OPENAI_API_KEY: {api_key[:20]}...")
    else:
        print("❌ 未找到 OPENAI_API_KEY")
        return

    # 检查项目结构
    src_dir = current_dir / 'src' / 'agents'
    if src_dir.exists():
        print(f"✅ 找到 src/agents 目录")
    else:
        print(f"❌ 未找到 src/agents 目录")
        return

    # 测试导入研究员智能体
    try:
        import sys
        sys.path.append(str(current_dir / 'src' / 'agents'))

        print("\n🚀 导入 ResearcherAgent...")
        from researcher import test_researcher_agent

        print("🧪 运行测试...")
        success = test_researcher_agent()

        if success:
            print("\n🎉 测试完全成功！可以继续下一步开发")
        else:
            print("\n❌ 测试失败，请检查错误信息")

    except ImportError as e:
        print(f"❌ 导入失败: {e}")
    except Exception as e:
        print(f"❌ 运行测试失败: {e}")


if __name__ == "__main__":
    main()