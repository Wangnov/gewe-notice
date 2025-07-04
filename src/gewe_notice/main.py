import typer
import os

# 从 server.py 导入 mcp 实例和 config 字典
from .server import mcp, config

# 创建一个 Typer 应用
app = typer.Typer(add_completion=False, rich_markup_mode="markdown")


@app.command()
def main():
    """
    启动 **gewe-notice** MCP 服务器。

    一个通过微信机器人发送AI任务状态通知的轻量级工具。
    所有配置均通过环境变量进行设置。
    """
    print("🚀 正在启动 gewe-notice MCP 服务器...")

    # 从环境变量读取配置
    base_url = os.getenv("GEWE_NOTICE_BASE_URL", "http://api.geweapi.com")
    token = os.getenv("GEWE_NOTICE_TOKEN")
    app_id = os.getenv("GEWE_NOTICE_APP_ID")
    wxid = os.getenv("GEWE_NOTICE_WXID")
    at_list_str = os.getenv("GEWE_NOTICE_AT_LIST", "")
    at_list = at_list_str.split() if at_list_str else []

    # 验证必要的参数是否已提供
    if not all([token, app_id, wxid]):
        print("\n❌ **错误**: 缺少必要的环境变量: `GEWE_NOTICE_TOKEN`, `GEWE_NOTICE_APP_ID`, `GEWE_NOTICE_WXID`")
        print("💡 请检查您的 MCP 配置文件。")
        raise typer.Exit(code=1)

    # 将从环境变量接收到的参数存入全局 config 字典
    config["base_url"] = base_url
    config["token"] = token
    config["app_id"] = app_id
    config["wxid"] = wxid
    config["at_list"] = at_list

    print("🔧 配置加载成功 (来自环境变量):")
    print(f"   - Base URL: {config['base_url']}")
    print(f"   - App ID:   {config['app_id']}")
    print(f"   - WXID:     {config['wxid']}")
    if config["at_list"]:
        print(f"   - At List:  {', '.join(config['at_list'])}")
    print("-" * 20)

    # 运行 MCP 服务器
    mcp.run()


if __name__ == "__main__":
    app()
