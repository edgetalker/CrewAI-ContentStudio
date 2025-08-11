"""
CrewAI-ContentStudio Streamlit Web界面
现代化的AI内容创作平台用户界面
"""
import streamlit as st
import sys
import os
from pathlib import Path
import time
import json
from datetime import datetime
import pandas as pd
from typing import Dict, Any, Optional
import io

# 设置页面配置
st.set_page_config(
    page_title="CrewAI ContentStudio",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-repo/CrewAI-ContentStudio',
        'Report a bug': 'https://github.com/your-repo/CrewAI-ContentStudio/issues',
        'About': '''
        # CrewAI ContentStudio
        基于多智能体协作的AI内容创作平台

        **版本**: 1.0.0  
        **技术栈**: CrewAI + OpenAI GPT-4 + Streamlit
        '''
    }
)


# 添加项目路径
@st.cache_resource
def setup_project_path():
    """设置项目路径"""
    current_dir = Path(__file__).parent
    project_root = current_dir.parent.parent
    crew_dir = project_root / 'src' / 'crew'

    if str(crew_dir) not in sys.path:
        sys.path.append(str(crew_dir))

    return project_root


# 导入ContentCrew
@st.cache_resource
def load_content_crew():
    """加载ContentCrew系统"""
    try:
        project_root = setup_project_path()
        from src.crew.ContentCrew import ContentCrew
        return ContentCrew(), None
    except Exception as e:
        return None, str(e)


# 自定义CSS样式
def load_custom_css():
    """加载自定义CSS样式"""
    st.markdown("""
    <style>
    /* 主题色彩系统 */
    :root {
        --primary-color: #2E86AB;
        --secondary-color: #A23B72;
        --accent-color: #F18F01;
        --success-color: #06D6A0;
        --warning-color: #FFD23F;
        --background-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    /* 主容器样式 */
    .main-header {
        background: var(--background-gradient);
        padding: 2rem 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }

    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-bottom: 0;
    }

    /* 功能卡片样式 */
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid var(--primary-color);
        margin-bottom: 1rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }

    .feature-card h3 {
        color: var(--primary-color);
        margin-bottom: 0.5rem;
        font-weight: 600;
    }

    /* 进度条样式 */
    .progress-container {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid #e9ecef;
    }

    .progress-step {
        display: flex;
        align-items: center;
        margin: 0.5rem 0;
        padding: 0.5rem;
        border-radius: 5px;
        transition: background-color 0.3s ease;
    }

    .progress-step.active {
        background-color: var(--primary-color);
        color: white;
    }

    .progress-step.completed {
        background-color: var(--success-color);
        color: white;
    }

    .progress-step.pending {
        background-color: #f8f9fa;
        color: #6c757d;
    }

    /* 结果展示区样式 */
    .result-container {
        background: white;
        border-radius: 10px;
        padding: 2rem;
        box-shadow: 0 2px 15px rgba(0,0,0,0.1);
        margin-top: 2rem;
    }

    .result-header {
        border-bottom: 2px solid var(--primary-color);
        padding-bottom: 1rem;
        margin-bottom: 1.5rem;
    }

    .result-content {
        line-height: 1.8;
        font-size: 1.1rem;
    }

    /* 侧边栏样式 */
    .sidebar-header {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        text-align: center;
    }

    /* 状态徽章 */
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        text-align: center;
    }

    .status-success {
        background-color: var(--success-color);
        color: white;
    }

    .status-warning {
        background-color: var(--warning-color);
        color: #333;
    }

    .status-info {
        background-color: var(--primary-color);
        color: white;
    }

    /* 动画效果 */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .fade-in-up {
        animation: fadeInUp 0.6s ease-out;
    }

    /* 响应式设计 */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        .main-header p {
            font-size: 1rem;
        }
    }

    /* 隐藏Streamlit默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 自定义滚动条 */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb {
        background: var(--primary-color);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--secondary-color);
    }
    </style>
    """, unsafe_allow_html=True)


# 初始化会话状态
def init_session_state():
    """初始化会话状态"""
    if 'content_crew' not in st.session_state:
        st.session_state.content_crew, st.session_state.crew_error = load_content_crew()

    if 'creation_history' not in st.session_state:
        st.session_state.creation_history = []

    if 'current_task' not in st.session_state:
        st.session_state.current_task = None

    if 'task_progress' not in st.session_state:
        st.session_state.task_progress = {}


# 主页面头部
def render_header():
    """渲染页面头部"""
    st.markdown("""
    <div class="main-header fade-in-up">
        <h1>🚀 CrewAI ContentStudio</h1>
        <p>基于多智能体协作的AI内容创作平台</p>
    </div>
    """, unsafe_allow_html=True)


# 侧边栏
def render_sidebar():
    """渲染侧边栏"""
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-header">
            <h2>🛠️ 控制面板</h2>
        </div>
        """, unsafe_allow_html=True)

        # 系统状态
        st.subheader("📊 系统状态")

        if st.session_state.content_crew:
            st.markdown('<span class="status-badge status-success">✅ 系统就绪</span>', unsafe_allow_html=True)
            st.success("ContentCrew 已加载")
        else:
            st.markdown('<span class="status-badge status-warning">⚠️ 系统错误</span>', unsafe_allow_html=True)
            st.error(f"系统初始化失败: {st.session_state.crew_error}")

        st.divider()

        # 快速统计
        st.subheader("📈 使用统计")
        col1, col2 = st.columns(2)

        with col1:
            st.metric("总创作数", len(st.session_state.creation_history))

        with col2:
            successful_creations = sum(1 for item in st.session_state.creation_history
                                       if item.get('status') == 'completed')
            st.metric("成功率", f"{successful_creations / len(st.session_state.creation_history) * 100:.0f}%"
            if st.session_state.creation_history else "0%")

        st.divider()

        # 历史记录
        st.subheader("📚 创作历史")

        if st.session_state.creation_history:
            for i, item in enumerate(reversed(st.session_state.creation_history[-5:])):
                with st.expander(f"📝 {item['topic'][:20]}..."):
                    st.write(f"**类型**: {item['content_type']}")
                    st.write(f"**时间**: {item['timestamp']}")
                    st.write(f"**状态**: {item['status']}")
                    if item['status'] == 'completed':
                        st.write(f"**字数**: {item.get('word_count', 'N/A')}")
        else:
            st.info("暂无创作历史")

        st.divider()

        # 帮助和信息
        st.subheader("❓ 帮助信息")

        with st.expander("🤖 智能体介绍"):
            st.markdown("""
            **🔍 研究员**: 收集最新信息和权威数据  
            **📊 分析师**: 制定内容策略和结构  
            **✍️ 写作者**: 创作高质量原创内容  
            **📝 编辑员**: 质量控制和SEO优化
            """)

        with st.expander("📋 内容类型说明"):
            st.markdown("""
            **博客文章**: 1200字，适合技术分享  
            **技术报告**: 2500字，深度分析  
            **新闻稿**: 800字，快速传播  
            **教程指南**: 2000字，操作说明  
            **营销文案**: 1000字，推广宣传
            """)


# 主要内容区域
def render_main_content():
    """渲染主要内容区域"""

    # 检查系统状态
    if not st.session_state.content_crew:
        st.error("⚠️ 系统未正确初始化，请检查配置文件和依赖项")
        st.info("💡 请确保 .env 文件配置正确，且所有依赖项已安装")
        return

    # 创建选项卡
    tab1, tab2, tab3 = st.tabs(["🎯 创建内容", "📊 实时监控", "📁 结果管理"])

    with tab1:
        render_content_creation_tab()

    with tab2:
        render_monitoring_tab()

    with tab3:
        render_results_tab()


def render_content_creation_tab():
    """渲染内容创建选项卡"""
    st.markdown("## 🎯 AI内容创作")

    # 创建两列布局
    col1, col2 = st.columns([2, 1])

    with col1:
        # 内容参数设置
        st.markdown("### 📝 内容参数设置")

        with st.form("content_creation_form"):
            # 基础参数
            topic = st.text_input(
                "📋 内容主题",
                placeholder="例如：人工智能在2025年的发展趋势",
                help="请输入您想要创作的内容主题"
            )

            content_type = st.selectbox(
                "📄 内容类型",
                options=["blog_post", "article", "report", "news", "tutorial", "marketing"],
                format_func=lambda x: {
                    "blog_post": "📝 博客文章",
                    "article": "📰 技术文章",
                    "report": "📊 研究报告",
                    "news": "📢 新闻稿",
                    "tutorial": "🎓 教程指南",
                    "marketing": "🎯 营销文案"
                }[x],
                help="选择最适合您需求的内容类型"
            )

            target_audience = st.selectbox(
                "👥 目标受众",
                options=["技术专业人士", "企业决策者", "技术爱好者", "普通消费者", "学生群体", "投资者"],
                help="选择您的目标读者群体"
            )

            word_count = st.slider(
                "📏 目标字数",
                min_value=300,
                max_value=3000,
                value=1200,
                step=100,
                help="设置期望的内容长度"
            )

            # 高级选项
            with st.expander("🔧 高级选项"):
                additional_requirements = st.text_area(
                    "额外要求",
                    placeholder="例如：重点关注实用性、包含具体案例、面向初学者等",
                    help="描述任何特殊要求或偏好"
                )

                priority_keywords = st.text_input(
                    "优先关键词",
                    placeholder="例如：机器学习, 深度学习, 神经网络",
                    help="用逗号分隔多个关键词"
                )

            # 提交按钮
            submitted = st.form_submit_button(
                "🚀 开始创作",
                type="primary",
                use_container_width=True
            )

            if submitted:
                if not topic.strip():
                    st.error("请输入内容主题")
                else:
                    # 启动内容创作
                    start_content_creation(
                        topic=topic,
                        content_type=content_type,
                        target_audience=target_audience,
                        word_count=word_count,
                        additional_requirements=additional_requirements
                    )

    with col2:
        # 实时预览和建议
        st.markdown("### 💡 智能建议")

        # 根据选择的参数提供建议
        st.markdown("""
        <div class="feature-card">
            <h4>🎯 创作建议</h4>
            <p>基于您的选择，我们推荐以下最佳实践：</p>
        </div>
        """, unsafe_allow_html=True)

        if 'content_type' in locals():
            suggestions = get_content_suggestions(content_type,
                                                  target_audience if 'target_audience' in locals() else "技术专业人士")
            for suggestion in suggestions:
                st.info(suggestion)


def render_monitoring_tab():
    """渲染实时监控选项卡"""
    st.markdown("## 📊 实时工作流监控")

    if st.session_state.current_task:
        # 显示当前任务信息
        st.markdown("### 🔄 当前任务")

        task_info = st.session_state.current_task

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("主题", task_info['topic'])
        with col2:
            st.metric("类型", task_info['content_type'])
        with col3:
            st.metric("进度", f"{task_info.get('progress', 0)}%")

        # 智能体进度追踪
        st.markdown("### 🤖 智能体协作进度")

        agents = [
            {"name": "🔍 研究员", "status": "completed", "description": "收集信息和数据"},
            {"name": "📊 分析师", "status": "active", "description": "分析策略制定"},
            {"name": "✍️ 写作者", "status": "pending", "description": "内容创作"},
            {"name": "📝 编辑员", "status": "pending", "description": "质量控制"}
        ]

        for agent in agents:
            render_agent_progress(agent)

        # 实时日志
        st.markdown("### 📝 执行日志")
        log_container = st.container()

        with log_container:
            if 'logs' in st.session_state.current_task:
                for log in st.session_state.current_task['logs']:
                    st.text(f"[{log['timestamp']}] {log['message']}")

    else:
        st.info("当前没有正在执行的任务")
        st.markdown("""
        <div class="feature-card">
            <h3>🚀 开始您的第一个内容创作任务</h3>
            <p>在"创建内容"选项卡中输入主题和参数，即可开始AI智能体协作创作。</p>
        </div>
        """, unsafe_allow_html=True)


def render_results_tab():
    """渲染结果管理选项卡"""
    st.markdown("## 📁 创作结果管理")

    if st.session_state.creation_history:
        st.markdown("### 📚 历史创作记录")

        # 创建数据框
        df_data = []
        for item in st.session_state.creation_history:
            df_data.append({
                "主题": item['topic'][:30] + "..." if len(item['topic']) > 30 else item['topic'],
                "类型": item['content_type'],
                "受众": item.get('target_audience', 'N/A'),
                "字数": item.get('word_count', 'N/A'),
                "状态": item['status'],
                "创建时间": item['timestamp']
            })

        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True)

        # 选择查看详细结果
        st.markdown("### 🔍 查看详细结果")

        selected_index = st.selectbox(
            "选择要查看的创作结果",
            options=range(len(st.session_state.creation_history)),
            format_func=lambda
                x: f"{st.session_state.creation_history[x]['topic'][:50]}... ({st.session_state.creation_history[x]['timestamp']})"
        )

        if selected_index is not None:
            selected_item = st.session_state.creation_history[selected_index]
            render_detailed_result(selected_item)

    else:
        st.info("暂无创作历史记录")
        st.markdown("""
        <div class="feature-card">
            <h3>📝 开始创作</h3>
            <p>完成第一个内容创作后，结果将显示在这里。</p>
        </div>
        """, unsafe_allow_html=True)


def render_agent_progress(agent):
    """渲染智能体进度"""
    status_colors = {
        "completed": "success",
        "active": "info",
        "pending": "secondary"
    }

    status_icons = {
        "completed": "✅",
        "active": "🔄",
        "pending": "⏳"
    }

    with st.container():
        col1, col2, col3 = st.columns([1, 3, 1])

        with col1:
            st.markdown(f"### {status_icons[agent['status']]}")

        with col2:
            st.markdown(f"**{agent['name']}**")
            st.caption(agent['description'])

        with col3:
            if agent['status'] == 'active':
                st.spinner("处理中...")


def render_detailed_result(item):
    """渲染详细结果"""
    st.markdown("#### 📄 内容详情")

    # 元信息
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("内容类型", item['content_type'])
    with col2:
        st.metric("目标受众", item.get('target_audience', 'N/A'))
    with col3:
        st.metric("执行时间", item.get('execution_time', 'N/A'))

    # 内容预览
    if 'content' in item:
        st.markdown("#### 📝 生成内容")

        # 添加复制按钮和下载按钮
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📋 复制到剪贴板", key=f"copy_{item['timestamp']}"):
                st.write("内容已复制到剪贴板")

        with col2:
            # 准备下载文件
            content_str = item['content']
            st.download_button(
                label="📥 下载内容",
                data=content_str,
                file_name=f"{item['topic'][:20]}_{item['timestamp']}.txt",
                mime="text/plain",
                key=f"download_{item['timestamp']}"
            )

        # 显示内容
        st.markdown("---")
        st.markdown(item['content'])

    # 质量指标
    if 'quality_metrics' in item:
        st.markdown("#### 📊 质量指标")
        metrics = item['quality_metrics']

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("内容质量", f"{metrics.get('overall_score', 'N/A')}/100")
        with col2:
            st.metric("长度匹配", "✅" if metrics.get('content_length_match', False) else "❌")
        with col3:
            st.metric("工作流完整", "✅" if metrics.get('workflow_completed', False) else "❌")


def get_content_suggestions(content_type, target_audience):
    """获取内容建议"""
    suggestions_map = {
        "blog_post": [
            "💡 使用吸引人的标题和副标题",
            "📊 包含数据和统计信息增强可信度",
            "🔗 添加相关链接和参考资料"
        ],
        "article": [
            "📚 确保内容具有权威性和深度",
            "🎯 提供独特的观点和洞察",
            "📈 使用图表和数据支撑论点"
        ],
        "report": [
            "📋 使用结构化的格式和清晰的章节",
            "📊 包含执行摘要和关键发现",
            "📈 提供可操作的建议和结论"
        ]
    }

    return suggestions_map.get(content_type, ["💡 保持内容清晰、有价值、易读"])


def start_content_creation(topic, content_type, target_audience, word_count, additional_requirements):
    """启动内容创作流程"""
    try:
        # 显示开始创作的提示
        with st.spinner("🚀 正在启动AI智能体协作..."):
            time.sleep(1)  # 给用户一些视觉反馈

        # 更新会话状态
        st.session_state.current_task = {
            'topic': topic,
            'content_type': content_type,
            'target_audience': target_audience,
            'word_count': word_count,
            'status': 'running',
            'progress': 0,
            'logs': []
        }

        # 调用ContentCrew
        progress_placeholder = st.empty()
        status_placeholder = st.empty()

        with progress_placeholder.container():
            st.info("🔍 研究员智能体：正在收集信息...")

        # 执行内容创作
        result = st.session_state.content_crew.create_content(
            topic=topic,
            content_type=content_type,
            target_audience=target_audience,
            word_count=word_count,
            additional_requirements=additional_requirements
        )

        # 更新进度
        with progress_placeholder.container():
            st.success("✅ 内容创作完成！")

        # 保存结果到历史记录
        creation_record = {
            'topic': topic,
            'content_type': content_type,
            'target_audience': target_audience,
            'word_count': word_count,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'status': 'completed',
            'content': result['content'],
            'execution_time': result['execution_info']['total_time'],
            'quality_metrics': result['quality_metrics']
        }

        st.session_state.creation_history.append(creation_record)
        st.session_state.current_task = None

        # 显示成功消息
        st.success(f"🎉 内容创作成功完成！耗时：{result['execution_info']['total_time']}")

        # 显示快速预览
        with st.expander("📄 快速预览", expanded=True):
            st.markdown(result['content'][:500] + "..." if len(result['content']) > 500 else result['content'])

        # 提供下载选项
        st.download_button(
            label="📥 下载完整内容",
            data=result['content'],
            file_name=f"{topic[:20]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )

    except Exception as e:
        st.error(f"❌ 创作过程中发生错误: {str(e)}")
        st.session_state.current_task = None


# 主函数
def main():
    """主函数"""
    # 加载自定义样式
    load_custom_css()

    # 初始化会话状态
    init_session_state()

    # 渲染页面
    render_header()
    render_sidebar()
    render_main_content()

    # 页脚
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 2rem;">
        <p>🚀 CrewAI ContentStudio v1.0.0 | 基于多智能体协作的AI内容创作平台</p>
        <p>💡 用 ❤️ 为AI和内容创作社区而构建</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()