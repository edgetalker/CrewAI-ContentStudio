#!/usr/bin/env python3
"""
CrewAI-ContentStudio 智能启动脚本
自动检测环境并选择合适的应用版本
"""
import os
import sys
import subprocess
from pathlib import Path
import argparse


def check_environment():
    """检查运行环境"""
    print("🔍 正在检查运行环境...")

    issues = []

    # 检查Python版本
    if sys.version_info < (3, 10):
        issues.append("❌ Python版本需要3.10或更高")
    else:
        print(f"✅ Python版本: {sys.version_info.major}.{sys.version_info.minor}")

    # 检查必要的包
    required_packages = ['streamlit', 'crewai', 'openai', 'python-dotenv']
    missing_packages = []

    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} 已安装")
        except ImportError:
            missing_packages.append(package)
            issues.append(f"❌ 缺少依赖: {package}")

    # 检查.env文件
    env_file = Path('.env')
    if env_file.exists():
        print("✅ .env 文件存在")

        # 检查关键配置
        with open(env_file, 'r') as f:
            env_content = f.read()
            if 'OPENAI_API_KEY' in env_content:
                print("✅ OPENAI_API_KEY 已配置")
            else:
                issues.append("❌ .env文件中缺少OPENAI_API_KEY")
    else:
        issues.append("❌ .env文件不存在")

    # 检查项目结构
    required_dirs = ['src/crew', 'src/agents', 'src/config']
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"✅ {dir_path} 目录存在")
        else:
            issues.append(f"❌ 缺少目录: {dir_path}")

    return issues, missing_packages


def install_requirements():
    """安装缺失的依赖"""
    print("\n📦 正在安装依赖...")

    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ 依赖安装完成")
        return True
    except subprocess.CalledProcessError:
        print("❌ 依赖安装失败")
        return False
    except FileNotFoundError:
        print("❌ requirements.txt 文件未找到")
        return False


def create_env_template():
    """创建.env模板文件"""
    env_template = """# CrewAI-ContentStudio 环境配置

# 必需：OpenAI API密钥
OPENAI_API_KEY=sk-your-openai-api-key-here

# 可选：Serper搜索API（增强研究功能）
SERPER_API_KEY=your-serper-api-key-here

# 模型配置
DEFAULT_MODEL=gpt-4o-mini
TEMPERATURE=0.7

# 应用设置
APP_NAME=CrewAI ContentStudio
DEBUG=True
"""

    with open('.env', 'w') as f:
        f.write(env_template)

    print("✅ .env 模板文件已创建")
    print("📝 请编辑 .env 文件，添加您的 OPENAI_API_KEY")


def check_content_crew():
    """检查ContentCrew系统是否可用"""
    try:
        sys.path.append('src/crew')
        from src.crew.ContentCrew import ContentCrew

        # 尝试创建ContentCrew实例
        crew = ContentCrew()
        print("✅ ContentCrew 系统可用")
        return True
    except Exception as e:
        print(f"❌ ContentCrew 系统不可用: {str(e)}")
        return False


def run_app(app_type='auto', port=8501, host='localhost'):
    """运行应用"""
    ui_dir = Path('src/ui')

    if app_type == 'auto':
        # 自动选择应用版本
        if check_content_crew():
            app_file = ui_dir / 'streamlit_app.py'
            print("🚀 启动完整版应用...")
        else:
            app_file = ui_dir / 'demo_app.py'
            print("🎭 启动演示版应用...")
    elif app_type == 'full':
        app_file = ui_dir / 'streamlit_app.py'
        print("🚀 启动完整版应用...")
    elif app_type == 'demo':
        app_file = ui_dir / 'demo_app.py'
        print("🎭 启动演示版应用...")
    else:
        print("❌ 无效的应用类型")
        return

    if not app_file.exists():
        print(f"❌ 应用文件不存在: {app_file}")
        return

    # 设置Streamlit配置
    config_dir = Path('.streamlit')
    config_dir.mkdir(exist_ok=True)

    config_content = f"""[server]
port = {port}
address = "{host}"

[theme]
primaryColor = "#2E86AB"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
"""

    with open(config_dir / 'config.toml', 'w') as f:
        f.write(config_content)

    # 启动Streamlit
    cmd = [
        'streamlit', 'run', str(app_file),
        '--server.port', str(port),
        '--server.address', host
    ]

    try:
        print(f"\n🌐 应用将在 http://{host}:{port} 启动")
        print("按 Ctrl+C 停止应用")
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n👋 应用已停止")
    except FileNotFoundError:
        print("❌ Streamlit 未安装，请运行: pip install streamlit")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='CrewAI-ContentStudio 启动脚本')
    parser.add_argument('--type', choices=['auto', 'full', 'demo'], default='auto',
                        help='应用类型 (auto: 自动选择, full: 完整版, demo: 演示版)')
    parser.add_argument('--port', type=int, default=8501, help='端口号')
    parser.add_argument('--host', default='localhost', help='主机地址')
    parser.add_argument('--check-only', action='store_true', help='仅检查环境，不启动应用')
    parser.add_argument('--install', action='store_true', help='安装缺失的依赖')

    args = parser.parse_args()

    print("🎯 CrewAI-ContentStudio 启动器")
    print("=" * 50)

    # 检查环境
    issues, missing_packages = check_environment()

    if issues:
        print(f"\n⚠️  发现 {len(issues)} 个问题:")
        for issue in issues:
            print(f"  {issue}")

        if args.install and missing_packages:
            if install_requirements():
                print("\n🔄 重新检查环境...")
                issues, _ = check_environment()

        if '.env文件不存在' in str(issues):
            create_env_template()

        if issues and not args.check_only:
            print("\n💡 建议:")
            print("1. 修复上述问题")
            print("2. 使用 --install 参数自动安装依赖")
            print("3. 使用 --type demo 运行演示版")

            if input("\n是否仍要继续启动？(y/N): ").lower() != 'y':
                return

    if args.check_only:
        if not issues:
            print("\n✅ 环境检查通过，可以启动应用")
        return

    print("\n" + "=" * 50)
    run_app(args.type, args.port, args.host)


if __name__ == "__main__":
    main()